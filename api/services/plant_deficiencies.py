"""Static reference data for the plant-health deficiency diagram/legend.

Adapted from the classic "New Growth vs Old Growth" aquarium plant
deficiency chart. Keys are stable identifiers used everywhere a deficiency
is referenced (PlantHealthEvent.deficiency_key, the vision model's
classification output, Kamilo's read/write tools) - never rename a key
without a migration, existing rows reference these by key.
"""

DEFICIENCIES: list[dict] = [
    {
        "key": "severe_nitrogen",
        "growth_stage": "new_growth",
        "name_en": "Severe Nitrogen Deficiency",
        "name_pl": "Ciężki niedobór azotu",
        "symptom_en": "White/yellow tiny new leaves.",
        "symptom_pl": "Białe/żółte, bardzo małe nowe liście.",
        "treatment_en": "Increase nitrate dosing (e.g. KNO3 or an all-in-one fertilizer) - new growth should green up within days.",
        "treatment_pl": "Zwiększ dawkowanie azotanów (np. KNO3 lub nawóz all-in-one) - nowe liście powinny zzielenieć w ciągu kilku dni.",
    },
    {
        "key": "calcium",
        "growth_stage": "new_growth",
        "name_en": "Calcium Deficiency (or K/Mg overdose)",
        "name_pl": "Niedobór wapnia (lub przedawkowanie K/Mg)",
        "symptom_en": "Twisted, pale new growth.",
        "symptom_pl": "Skręcone, blade nowe przyrosty.",
        "treatment_en": "Check GH/calcium levels first; if calcium is low, dose a calcium supplement. If GH is fine, check you're not overdosing potassium or magnesium.",
        "treatment_pl": "Najpierw sprawdź GH/poziom wapnia; jeśli niski, dodaj suplement wapnia. Jeśli GH jest w normie, sprawdź czy nie przedawkowujesz potasu lub magnezu.",
    },
    {
        "key": "iron",
        "growth_stage": "new_growth",
        "name_en": "Iron Deficiency",
        "name_pl": "Niedobór żelaza",
        "symptom_en": "Yellowing or whitening of new leaves only (veins often stay green).",
        "symptom_pl": "Żółknięcie lub bielenie tylko nowych liści (żyłki często zostają zielone).",
        "treatment_en": "Dose a chelated iron/micronutrient fertilizer.",
        "treatment_pl": "Dawkuj chelatowane żelazo / nawóz mikroelementowy.",
    },
    {
        "key": "magnesium",
        "growth_stage": "old_growth",
        "name_en": "Magnesium Deficiency",
        "name_pl": "Niedobór magnezu",
        "symptom_en": "Dark veins with lighter leaf tissue between them, on older leaves.",
        "symptom_pl": "Ciemne żyłki z jaśniejszą tkanką liścia między nimi, na starszych liściach.",
        "treatment_en": "Dose a magnesium supplement (e.g. Epsom salt / MgSO4) if GH is otherwise low.",
        "treatment_pl": "Dawkuj suplement magnezu (np. sól gorzka / MgSO4), jeśli GH jest ogólnie niskie.",
    },
    {
        "key": "potassium",
        "growth_stage": "old_growth",
        "name_en": "Potassium Deficiency",
        "name_pl": "Niedobór potasu",
        "symptom_en": "Pin-holes form in the leaf that enlarge, with a yellowing edge - the rest of the leaf looks normal.",
        "symptom_pl": "W liściu powstają dziurki, które się powiększają, z żółknącym brzegiem - reszta liścia wygląda normalnie.",
        "treatment_en": "Increase potassium dosing (e.g. K2SO4 or an all-in-one fertilizer).",
        "treatment_pl": "Zwiększ dawkowanie potasu (np. K2SO4 lub nawóz all-in-one).",
    },
    {
        "key": "early_nitrogen",
        "growth_stage": "old_growth",
        "name_en": "Early Nitrogen Deficiency",
        "name_pl": "Wczesny niedobór azotu",
        "symptom_en": "Old leaves yellow and are reabsorbed from the tip toward the stem.",
        "symptom_pl": "Stare liście żółkną i są wchłaniane od czubka w stronę łodygi.",
        "treatment_en": "Increase nitrate dosing.",
        "treatment_pl": "Zwiększ dawkowanie azotanów.",
    },
    {
        "key": "phosphate",
        "growth_stage": "old_growth",
        "name_en": "Phosphate Deficiency",
        "name_pl": "Niedobór fosforanów",
        "symptom_en": "Older leaves yellow with dead patches as parts are reabsorbed; the leaf falls off quickly. Looks similar to early nitrogen deficiency.",
        "symptom_pl": "Starsze liście żółkną z martwymi plamami w miarę wchłaniania fragmentów; liść szybko odpada. Wygląda podobnie do wczesnego niedoboru azotu.",
        "treatment_en": "Increase phosphate dosing (e.g. KH2PO4 or an all-in-one fertilizer).",
        "treatment_pl": "Zwiększ dawkowanie fosforanów (np. KH2PO4 lub nawóz all-in-one).",
    },
    {
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
