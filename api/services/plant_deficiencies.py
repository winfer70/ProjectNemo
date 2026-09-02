"""Static reference data for the plant-health deficiency diagram/legend.

Matches the "5 Min Guide: Freshwater Nutrient Deficiencies" chart (by
Aquathusiast) the diagram is drawn from - 8 leaves, 4 new-growth (top) and
4 old-growth (bottom). Keys are stable identifiers used everywhere a
deficiency is referenced (PlantHealthEvent.deficiency_key, the vision
model's classification output, Kamilo's read/write tools, and the
frontend diagram's leaf positions) - never rename a key without a
migration, existing rows reference these by key.
"""

DEFICIENCIES: list[dict] = [
    {
        "key": "iron",
        "growth_stage": "new_growth",
        "name_en": "Iron",
        "name_pl": "Żelazo",
        "symptom_en": "New growth is yellow and white. Old growth appears normal.",
        "symptom_pl": "Nowe przyrosty są żółte i białe. Stare liście wyglądają normalnie.",
        "treatment_en": "Dose a chelated iron/micronutrient fertilizer.",
        "treatment_pl": "Dawkuj chelatowane żelazo / nawóz mikroelementowy.",
    },
    {
        "key": "calcium",
        "growth_stage": "new_growth",
        "name_en": "Calcium",
        "name_pl": "Wapń",
        "symptom_en": "Stunted growth and misshapen leaves.",
        "symptom_pl": "Zahamowany wzrost i zniekształcone liście.",
        "treatment_en": "Check GH/calcium levels first; if calcium is low, dose a calcium supplement. If GH is fine, check you're not overdosing potassium or magnesium.",
        "treatment_pl": "Najpierw sprawdź GH/poziom wapnia; jeśli niski, dodaj suplement wapnia. Jeśli GH jest w normie, sprawdź czy nie przedawkowujesz potasu lub magnezu.",
    },
    {
        "key": "manganese",
        "growth_stage": "new_growth",
        "name_en": "Manganese",
        "name_pl": "Mangan",
        "symptom_en": "Spots and holes in the leaf.",
        "symptom_pl": "Plamy i dziury w liściu.",
        "treatment_en": "Dose a micronutrient fertilizer containing manganese.",
        "treatment_pl": "Dawkuj nawóz mikroelementowy zawierający mangan.",
    },
    {
        "key": "nitrogen",
        "growth_stage": "new_growth",
        "name_en": "Nitrogen",
        "name_pl": "Azot",
        "symptom_en": "Old growth yellow and wilted, new growth light green.",
        "symptom_pl": "Stare liście żółkną i więdną, nowe przyrosty są jasnozielone.",
        "treatment_en": "Increase nitrate dosing (e.g. KNO3 or an all-in-one fertilizer).",
        "treatment_pl": "Zwiększ dawkowanie azotanów (np. KNO3 lub nawóz all-in-one).",
    },
    {
        "key": "potassium",
        "growth_stage": "old_growth",
        "name_en": "Potassium",
        "name_pl": "Potas",
        "symptom_en": "Yellowing of the tips and edges.",
        "symptom_pl": "Żółknięcie końcówek i brzegów liścia.",
        "treatment_en": "Increase potassium dosing (e.g. K2SO4 or an all-in-one fertilizer).",
        "treatment_pl": "Zwiększ dawkowanie potasu (np. K2SO4 lub nawóz all-in-one).",
    },
    {
        "key": "magnesium",
        "growth_stage": "old_growth",
        "name_en": "Magnesium",
        "name_pl": "Magnez",
        "symptom_en": "Dark veins, light leaves.",
        "symptom_pl": "Ciemne żyłki, jasne liście.",
        "treatment_en": "Dose a magnesium supplement (e.g. Epsom salt / MgSO4) if GH is otherwise low.",
        "treatment_pl": "Dawkuj suplement magnezu (np. sól gorzka / MgSO4), jeśli GH jest ogólnie niskie.",
    },
    {
        "key": "phosphate",
        "growth_stage": "old_growth",
        "name_en": "Phosphate",
        "name_pl": "Fosforany",
        "symptom_en": "Loss of leaves, darker hue.",
        "symptom_pl": "Utrata liści, ciemniejszy odcień.",
        "treatment_en": "Increase phosphate dosing (e.g. KH2PO4 or an all-in-one fertilizer).",
        "treatment_pl": "Zwiększ dawkowanie fosforanów (np. KH2PO4 lub nawóz all-in-one).",
    },
    {
        "key": "co2",
        "growth_stage": "old_growth",
        "name_en": "CO2",
        "name_pl": "CO2",
        "symptom_en": "Leaves die, stunted growth.",
        "symptom_pl": "Liście obumierają, zahamowany wzrost.",
        "treatment_en": "Check/increase CO2 injection rate and distribution.",
        "treatment_pl": "Sprawdź/zwiększ dawkę i rozprowadzenie CO2.",
    },
    {
        # Not on the reference chart - kept so the AI vision classifier has
        # a valid "nothing's wrong" answer instead of being forced to pick
        # a deficiency for a healthy leaf. Never shown on the diagram.
        "key": "normal",
        "growth_stage": "new_growth",
        "name_en": "Normal / Healthy",
        "name_pl": "Normalny / Zdrowy",
        "symptom_en": "Uniform green leaf, no discoloration or deformity.",
        "symptom_pl": "Jednolicie zielony liść, bez przebarwień i deformacji.",
        "treatment_en": "No action needed.",
        "treatment_pl": "Brak działania wymaganego.",
    },
]

DEFICIENCIES_BY_KEY = {d["key"]: d for d in DEFICIENCIES}
VALID_KEYS = set(DEFICIENCIES_BY_KEY)
