"""OpenCV-based aquarium test strip colour reader.

Expects an image containing both the test strip and the reference colour chart
photographed together.

Pipeline:
  1. Find all coloured rectangular cells in the image.
  2. K-means cluster cells into N_PADS horizontal row-bands by y-centre.
  3. Initial per-row pad/chart split by largest x-gap.
  4. Global x-consistency pass: if any pad x-centre deviates > 2σ from median,
     re-assign using the cell in that row closest to the median x. This prevents
     one noisy row from index-shifting the entire strip.
  5. Low-saturation pad (white/cream) → value 0 (skipped for pH).
  6. Otherwise: match pad HSV to reference cell HSV by weighted Euclidean distance.
     Uses cells detected from the chart if ≥ 2 found, else static fallback table.
  7. Annotate each result with out_of_range using the supplied safe-range dict.

Raises CVDetectionError when the pipeline cannot confidently identify pads.
"""
import io
import logging
import math

import cv2
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

N_PADS = 9
PAD_ORDER = [
    "copper", "nitrate", "nitrite", "free_chlorine",
    "gh", "total_alkalinity", "kh", "ph", "ammonia",
]
PARAM_VALUES = {
    "copper":           [0, 0.2, 0.5, 1, 2, 5],
    "nitrate":          [0, 10, 25, 50, 100, 250],
    "nitrite":          [0, 1, 5, 10],
    "free_chlorine":    [0, 0.5, 1, 3, 5, 10, 20],
    "gh":               [0, 25, 50, 125, 250, 425],
    "total_alkalinity": [0, 40, 80, 120, 180, 240],
    "kh":               [0, 40, 80, 120, 180, 300],
    "ph":               [6.2, 6.8, 7.2, 7.6, 7.8, 8.4],
    "ammonia":          [0, 0.5, 1, 3, 5, 10],
}

# Static HSV reference (H:0-180, S:0-255, V:0-255).
# Used only when reference chart cells cannot be detected in the image.
# Approximate — needs calibration from real strip photos with known values.
_STATIC_HSV_REF: dict[str, list[tuple]] = {
    "copper": [
        (0, 8, 240), (22, 55, 225), (22, 110, 215),
        (20, 160, 200), (18, 190, 185), (14, 210, 170),
    ],
    "nitrate": [
        (0, 8, 240), (172, 35, 225), (172, 75, 215),
        (170, 130, 200), (168, 185, 180), (162, 215, 160),
    ],
    "nitrite": [
        (0, 8, 240), (152, 55, 220), (150, 130, 200), (145, 200, 175),
    ],
    "free_chlorine": [
        (0, 8, 240), (100, 38, 228), (100, 75, 218), (100, 140, 200),
        (100, 185, 182), (100, 215, 165), (100, 240, 148),
    ],
    "gh": [
        (0, 8, 240), (18, 48, 232), (18, 95, 220),
        (22, 155, 200), (20, 200, 185), (16, 230, 162),
    ],
    "total_alkalinity": [
        (0, 8, 240), (62, 48, 232), (66, 95, 220),
        (72, 148, 204), (74, 200, 182), (78, 228, 158),
    ],
    "kh": [
        (0, 8, 240), (62, 38, 235), (66, 88, 222),
        (70, 148, 205), (72, 200, 185), (76, 228, 160),
    ],
    "ph": [
        (58, 185, 185), (22, 185, 200), (17, 185, 205),
        (12, 200, 200), (8, 210, 195), (122, 178, 182),
    ],
    "ammonia": [
        (52, 10, 242), (62, 58, 232), (68, 118, 218),
        (74, 178, 196), (78, 210, 180), (82, 240, 160),
    ],
}

WHITE_S_THRESH = 60   # raised: cream plastic + JPEG chroma bleed can push S to ~50
WHITE_V_MIN = 160     # must also be bright to count as white/zero
_NO_WHITE_ZERO = {"ph"}
MIN_AVG_CONFIDENCE = 0.35


class CVDetectionError(Exception):
    pass


# ── Helpers ───────────────────────────────────────────────────────────────────

def _to_bgr(image_bytes: bytes) -> np.ndarray:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def _hsv_dist(a: tuple, b: tuple) -> float:
    dh = min(abs(float(a[0]) - float(b[0])), 180 - abs(float(a[0]) - float(b[0])))
    ds = abs(float(a[1]) - float(b[1]))
    dv = abs(float(a[2]) - float(b[2]))
    return math.sqrt((dh * 2) ** 2 + ds ** 2 + (dv * 0.5) ** 2)


def _roi_median_hsv(hsv: np.ndarray, x: int, y: int, w: int, h: int) -> tuple:
    px, py = max(1, w // 5), max(1, h // 5)
    roi = hsv[y + py: y + h - py, x + px: x + w - px]
    if roi.size == 0:
        roi = hsv[y: y + h, x: x + w]
    return (
        float(np.median(roi[:, :, 0])),
        float(np.median(roi[:, :, 1])),
        float(np.median(roi[:, :, 2])),
    )


# ── Detection ─────────────────────────────────────────────────────────────────

def _find_cells(img_bgr: np.ndarray) -> list[tuple[int, int, int, int]]:
    h_img, w_img = img_bgr.shape[:2]
    min_a = max(40 * 40, int(h_img * w_img * 0.0004))
    max_a = int(h_img * w_img * 0.12)

    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 4
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(~thresh, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cells = []
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
        if len(approx) not in (4, 5, 6):
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        if not (min_a < w * h < max_a):
            continue
        if max(w, h) / min(w, h) > 6:
            continue
        cells.append((x, y, w, h))
    return cells


def _cluster_rows(cells: list, n: int) -> list[list]:
    if len(cells) < n:
        raise CVDetectionError(f"Only {len(cells)} cells detected, need ≥ {n}")
    y_cents = np.array([[c[1] + c[3] / 2.0] for c in cells], dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.5)
    _, labels, centers = cv2.kmeans(
        y_cents, n, None, criteria, 10, cv2.KMEANS_PP_CENTERS
    )
    center_order = np.argsort(centers.flatten())
    lbl_remap = {int(old): new for new, old in enumerate(center_order)}
    rows: list[list] = [[] for _ in range(n)]
    for cell, lbl in zip(cells, labels.flatten()):
        rows[lbl_remap[int(lbl)]].append(cell)
    return rows


def _split_pad_chart(row: list) -> tuple[tuple | None, list]:
    """Per-row initial split: pad = isolated cell, chart = tight group."""
    if not row:
        return None, []
    if len(row) == 1:
        return row[0], []
    row_s = sorted(row, key=lambda c: c[0])
    x_centers = [c[0] + c[2] / 2.0 for c in row_s]
    gaps = [x_centers[i + 1] - x_centers[i] for i in range(len(x_centers) - 1)]
    split = int(np.argmax(gaps))
    left = row_s[: split + 1]
    right = row_s[split + 1:]
    if len(left) <= len(right):
        return left[-1], right
    return right[0], left


def _enforce_pad_x_consistency(
    rows: list[list], splits: list[tuple]
) -> list[tuple]:
    """Global pass: all strip pads should share a consistent x-centre.

    If a row's identified pad deviates > 2σ from the median pad x-centre,
    re-assign it to the cell in that row closest to the median x.
    This corrects single-row index shifts caused by background noise cells.
    """
    pad_xs = []
    for pad_cell, _ in splits:
        if pad_cell is not None:
            pad_xs.append(pad_cell[0] + pad_cell[2] / 2.0)

    if len(pad_xs) < 5:
        return splits  # not enough data for meaningful correction

    median_x = float(np.median(pad_xs))
    std_x = float(np.std(pad_xs))
    threshold = max(2.0 * std_x, 60.0)  # at least 60px threshold

    corrected = []
    for i, (row_cells, (pad_cell, ref_cells)) in enumerate(zip(rows, splits)):
        if pad_cell is None or not row_cells:
            corrected.append((pad_cell, ref_cells))
            continue

        pad_x = pad_cell[0] + pad_cell[2] / 2.0
        if abs(pad_x - median_x) > threshold:
            best = min(row_cells, key=lambda c: abs(c[0] + c[2] / 2.0 - median_x))
            new_refs = [c for c in row_cells if c != best]
            logger.info(
                "strip_cv: row %d (%s) x-consistency fix: pad_x=%.0f → %.0f (median=%.0f σ=%.0f)",
                i, PAD_ORDER[i], pad_x, best[0] + best[2] / 2.0, median_x, std_x,
            )
            corrected.append((best, new_refs))
        else:
            corrected.append((pad_cell, ref_cells))

    return corrected


# ── Matching ──────────────────────────────────────────────────────────────────

def _match_to_ref(
    pad_hsv: tuple, ref_hsvs: list, values: list
) -> tuple[float, float]:
    best_val = values[0]
    best_dist = float("inf")
    second_dist = float("inf")
    for val, ref in zip(values, ref_hsvs):
        d = _hsv_dist(pad_hsv, ref)
        if d < best_dist:
            second_dist = best_dist
            best_dist = d
            best_val = val
        elif d < second_dist:
            second_dist = d
    gap = second_dist - best_dist
    confidence = min(1.0, gap / 35.0)
    return best_val, confidence


def _is_oor(value: float, param: dict) -> bool:
    mn = param.get("min_safe")
    mx = param.get("max_safe")
    if mn is not None and value < mn:
        return True
    if mx is not None and value > mx:
        return True
    return False


# ── Debug visualisation ───────────────────────────────────────────────────────

def debug_analyze_strip(image_bytes: bytes) -> tuple[bytes, list[dict]]:
    """Return (annotated_jpeg_bytes, per_row_debug_list).

    Annotated image:
      - All detected cells: thin blue outline
      - Identified pad cells: thick green outline + row label
      - Reference chart cells: thin orange outline

    Debug list per row: param, pad_bbox, pad_hsv (H/S/V), n_refs, white_check
    """
    img_bgr = _to_bgr(image_bytes)
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    debug_img = img_bgr.copy()
    row_debug: list[dict] = []

    try:
        cells = _find_cells(img_bgr)
        rows = _cluster_rows(cells, N_PADS)
    except CVDetectionError as e:
        cv2.putText(debug_img, str(e), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        _, jpeg = cv2.imencode(".jpg", debug_img, [cv2.IMWRITE_JPEG_QUALITY, 85])
        return jpeg.tobytes(), [{"error": str(e)}]

    # All cells: thin blue
    for x, y, w, h in cells:
        cv2.rectangle(debug_img, (x, y), (x + w, y + h), (200, 100, 0), 1)

    splits = [_split_pad_chart(row) for row in rows]
    splits = _enforce_pad_x_consistency(rows, splits)

    for row_idx, (param_key, row_cells, (pad_cell, ref_cells)) in enumerate(
        zip(PAD_ORDER, rows, splits)
    ):
        if not row_cells or pad_cell is None:
            row_debug.append({"row": row_idx, "param": param_key, "error": "no cells"})
            continue

        # Pad: thick green
        x, y, w, h = pad_cell
        cv2.rectangle(debug_img, (x, y), (x + w, y + h), (0, 230, 0), 2)
        cv2.putText(
            debug_img, f"{row_idx}:{param_key[:4]}",
            (x, max(y - 4, 12)), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 230, 0), 1,
        )

        # Ref cells: thin orange
        for rx, ry, rw, rh in ref_cells:
            cv2.rectangle(debug_img, (rx, ry), (rx + rw, ry + rh), (0, 165, 255), 1)

        pad_hsv = _roi_median_hsv(img_hsv, *pad_cell)
        white = param_key not in _NO_WHITE_ZERO and pad_hsv[1] < WHITE_S_THRESH and pad_hsv[2] > WHITE_V_MIN

        row_debug.append({
            "row": row_idx,
            "param": param_key,
            "pad_bbox": list(pad_cell),
            "pad_hsv": {"H": round(pad_hsv[0], 1), "S": round(pad_hsv[1], 1), "V": round(pad_hsv[2], 1)},
            "n_refs": len(ref_cells),
            "white_check": white,
        })

    _, jpeg = cv2.imencode(".jpg", debug_img, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return jpeg.tobytes(), row_debug


# ── Public API ────────────────────────────────────────────────────────────────

def analyze_strip(
    image_bytes: bytes,
    params_by_key: dict,
) -> dict[str, dict]:
    """Analyse a test strip photo.

    Returns:
        {param_key: {value: float|None, out_of_range: bool, confidence: float}}

    Raises:
        CVDetectionError: if strip cannot be detected or overall confidence is low.
    """
    img_bgr = _to_bgr(image_bytes)
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    cells = _find_cells(img_bgr)
    logger.info("strip_cv: %d candidate cells", len(cells))

    rows = _cluster_rows(cells, N_PADS)

    splits = [_split_pad_chart(row) for row in rows]
    splits = _enforce_pad_x_consistency(rows, splits)

    results: dict[str, dict] = {}
    confidences: list[float] = []

    for row_idx, (param_key, row_cells, (pad_cell, ref_cells)) in enumerate(
        zip(PAD_ORDER, rows, splits)
    ):
        values = PARAM_VALUES[param_key]
        param = params_by_key.get(param_key, {})

        if not row_cells or pad_cell is None:
            logger.warning("strip_cv: no cells in row %d (%s)", row_idx, param_key)
            results[param_key] = {"value": None, "out_of_range": False, "confidence": 0.0}
            continue

        pad_hsv = _roi_median_hsv(img_hsv, *pad_cell)

        logger.info(
            "strip_cv: row%d %-16s H=%3.0f S=%3.0f V=%3.0f refs=%d",
            row_idx, param_key, *pad_hsv, len(ref_cells),
        )

        if param_key not in _NO_WHITE_ZERO and pad_hsv[1] < WHITE_S_THRESH and pad_hsv[2] > WHITE_V_MIN:
            value, confidence = 0.0, 0.80
        else:
            if len(ref_cells) >= 2:
                ref_cells_s = sorted(ref_cells, key=lambda c: c[0])
                ref_hsvs = [_roi_median_hsv(img_hsv, *c) for c in ref_cells_s]
                ref_hsvs = ref_hsvs[:len(values)]
                # Chart direction: zero/lowest-value cell has lowest saturation.
                # If list is high→low saturation (reversed chart), flip to match values order.
                if len(ref_hsvs) >= 2 and ref_hsvs[0][1] > ref_hsvs[-1][1]:
                    ref_hsvs = ref_hsvs[::-1]
                using_static = False
            else:
                ref_hsvs = [tuple(v) for v in _STATIC_HSV_REF.get(param_key, [])]
                using_static = True

            if len(ref_hsvs) < 2:
                results[param_key] = {"value": None, "out_of_range": False, "confidence": 0.0}
                continue

            value, confidence = _match_to_ref(pad_hsv, ref_hsvs, values[:len(ref_hsvs)])
            if using_static:
                confidence *= 0.6

        oor = _is_oor(value, param) if value is not None else False
        results[param_key] = {"value": value, "out_of_range": oor, "confidence": confidence}
        confidences.append(confidence)

    if not confidences:
        raise CVDetectionError("No pads could be analysed")

    avg_conf = sum(confidences) / len(confidences)
    logger.info("strip_cv: avg_confidence=%.2f", avg_conf)
    if avg_conf < MIN_AVG_CONFIDENCE:
        raise CVDetectionError(f"Low overall confidence ({avg_conf:.2f} < {MIN_AVG_CONFIDENCE})")

    return results
