"""Database seeder for ProjectNemo reference data — called once by main.py on startup.

Populates SQLite with water test parameters, supplies, dosing/feeding/maintenance tasks,
calendar events, livestock species (Fish), and plants (Plant). Imports all ORM models
from models.orm. Only seeds tables when empty to preserve manual edits.
"""
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.orm import (
    CalendarTask,
    DosingTask,
    FeedingSchedule,
    Fish,
    MaintenanceTask,
    Plant,
    Supply,
    WaterTestParameter,
    WaterTestSession,
    WaterTestReading,
)


WATER_TEST_PARAMS = [
    # key               name_en                          name_pl                           unit    min_safe  max_safe  category
    # Strip params: read at 30S — except ammonia (3 min)
    ("temp",            "Temperature",                   "Temperatura",                    "°C",   24.5,     27.5,     "continuous"),
    ("ph",              "pH",                            "pH",                             "",     7.2,      7.6,      "manual"),
    ("kh",              "KH / Total Alkalinity",         "KH / Twardość Węglanowa",        "°dKH", 2.2,      6.7,      "manual"),
    ("gh",              "Hardness (GH)",                 "Twardość Ogólna (GH)",           "°dGH", 7.0,      14.0,     "manual"),
    ("total_alkalinity","Total Alkalinity (TAL)",        "Zasadowość Całkowita (TAL)",     "ppm",  80,       120,      "manual"),
    ("nitrate",         "Nitrate (NO3)",                 "Azotany (NO3)",                  "mg/L", None,     30.0,     "manual"),
    ("nitrite",         "Nitrite (NO2)",                 "Azotyny (NO2)",                  "mg/L", None,     0.0,      "manual"),
    ("ammonia",         "Ammonia Nitrogen (NH3/NH4)",    "Azot Amonowy (NH3/NH4)",         "mg/L", None,     0.0,      "manual"),
    ("copper",          "Copper (Cu)",                   "Miedź (Cu)",                     "mg/L", None,     0.2,      "manual"),
    ("free_chlorine",   "Free Chlorine (Cl)",            "Wolny Chlor (Cl)",               "mg/L", None,     0.0,      "manual"),
]

# key -> (test_frequency_days, high_effect_en, high_effect_pl). None frequency
# = no reminder (continuous sensor). Based on standard freshwater community
# tank test-kit guidance.
WATER_TEST_REMINDER_DEFAULTS = {
    "temp": (None, None, None),
    "ph": (7,
        "High pH increases the toxicity of ammonia and can stress or burn fish; sudden swings during water changes are especially dangerous.",
        "Wysokie pH zwiększa toksyczność amoniaku i może stresować lub poparzyć ryby; nagłe skoki podczas podmian są szczególnie niebezpieczne."),
    "kh": (7,
        "Very high KH keeps pH locked stubbornly high, making it hard to lower and stressing fish that prefer softer water.",
        "Bardzo wysokie KH usztywnia pH na wysokim poziomie, utrudniając jego obniżenie i stresując ryby preferujące miększą wodę."),
    "gh": (30,
        "High GH (very hard water) stresses soft-water species, can impair osmoregulation and reduce breeding success.",
        "Wysokie GH (bardzo twarda woda) stresuje gatunki miękkowodne, może zaburzać osmoregulację i obniżać sukces rozrodu."),
    "total_alkalinity": (14,
        "High alkalinity buffers pH very high and can stress fish adapted to softer, more acidic water.",
        "Wysoka zasadowość utrzymuje pH na wysokim poziomie i może stresować ryby przystosowane do miększej, bardziej kwaśnej wody."),
    "nitrate": (7,
        "Chronic high nitrate causes stress, stunted growth, poor coloration and fuels algae blooms — usually means it's time for a water change.",
        "Przewlekle wysokie azotany powodują stres, zahamowanie wzrostu, słabsze wybarwienie i sprzyjają glonom — zwykle czas na podmianę wody."),
    "nitrite": (7,
        "Even a small rise in nitrite blocks oxygen transport in the blood ('brown blood disease') and can suffocate fish within hours.",
        "Nawet niewielki wzrost azotynów blokuje transport tlenu we krwi ('choroba brunatnej krwi') i może udusić ryby w ciągu kilku godzin."),
    "ammonia": (7,
        "Ammonia is highly toxic — it burns gills and fins and can kill fish within hours, especially at higher pH/temperature.",
        "Amoniak jest silnie toksyczny — poparza skrzela i płetwy i może zabić ryby w ciągu kilku godzin, zwłaszcza przy wyższym pH/temperaturze."),
    "copper": (30,
        "Copper is lethal to shrimp, snails and other invertebrates even at low concentrations, and can damage fish gills/liver.",
        "Miedź jest śmiertelna dla krewetek, ślimaków i innych bezkręgowców nawet w niskich stężeniach i może uszkodzić skrzela/wątrobę ryb."),
    "free_chlorine": (30,
        "Chlorine destroys gill tissue and kills the beneficial bacteria your filter depends on — usually only a risk after a tap water treatment failure.",
        "Chlor niszczy tkankę skrzelową i zabija pożyteczne bakterie w filtrze — zwykle zagrożenie tylko po awarii uzdatniania wody kranowej."),
}


DEFAULT_SUPPLIES = [
    # name                              name_pl                                     type      amount  unit    min_thresh
    ("Seachem Prime",                   "Seachem Prime",                            "liquid", 500,    "ml",   50),
    ("Seachem Stability",               "Seachem Stability",                        "liquid", 500,    "ml",   50),
    ("Easy-Life ProFito",               "Easy-Life ProFito",                        "liquid", 0,      "ml",   50),
    ("JBL Pronovo Corydoras Tab M",     "JBL Pronovo Corydoras Tab M 250ml",        "food",   0,      "ml",   50),
    ("Tropical Green Algae Wafers",     "Tropical Zielone Wafle Algowe 250ml",      "food",   0,      "ml",   50),
    ("Niteangel Coconut Shell Caves",   "Niteangel Jaskinie Kokosowe x4",           "part",   4,      "pcs",  1),
    ("JBL Pronovo Bel Flakes M",        "JBL Pronovo Bel Płatki M",                "food",   0,      "g",    20),
    ("Frozen Artemia/Cyclops",          "Mrożona Artemia/Cyklopy (blistry)",        "food",   0,      "pcs",  2),
    ("Filter Carbon Pad (Fluval)",      "Wkład Węglowy Carbon Pad (Fluval)",        "part",   1,      "pcs",  1),
    ("Quick-Clear Polishing Pad (Fluval)", "Gąbka Polerująca Quick-Clear (Fluval)", "part",   1,      "pcs",  1),
    ("Fluval Biomax / Seachem Matrix",  "Fluval Biomax / Seachem Matrix",           "part",   1,      "pcs",  1),
    ("Aquavital Stress-Protect",        "Aquavital Stress-Protect",                         "liquid", 1,      "btl",  1),
]

DEFAULT_DOSING_TASKS = [
    # supply_name               dose   unit  time    notes_en                                                              notes_pl
    ("Seachem Prime",           2.0,  "ml", None,   "Water change day only (Thursdays) — 2 ml per ~30L bucket",           "Tylko w dzień podmiany wody (czwartek) — 2 ml na ~30L wiadro"),
    ("Easy-Life ProFito",      12.5,  "ml", None,   "Weekly fertiliser, half-dose — Fridays from mid-July (from 17 Jul)", "Tygodniowy nawóz, połowa dawki — piątki od połowy lipca (od 17 lip)"),
    ("Seachem Stability",      25.0,  "ml", "08:00","Bacteria boost: 30 ml/day Thu–Sun after Step 1; 25 ml once after Steps 2–4", "Bakterie: 30 ml/dzień czw–niedz po Kroku 1; 25 ml jednorazowo po Krokach 2–4"),
]

DEFAULT_FEEDING_TIMES = ["19:00"]

DEFAULT_MAINTENANCE_TASKS = [
    {
        "name": "Partial Water Change (~30%)",
        "name_pl": "Częściowa Wymiana Wody (~30%)",
        "interval_days": 7,
        "steps": [
            {"order": 1, "text_en": "Prepare 1 × 30L bucket of tap water", "text_pl": "Przygotuj 1 × 30L wiadro wody z kranu"},
            {"order": 2, "text_en": "Add 2 ml Seachem Prime to the bucket and mix", "text_pl": "Dodaj 2 ml Seachem Prime do wiadra i wymieszaj"},
            {"order": 3, "text_en": "Match bucket temperature to tank temperature (±1°C)", "text_pl": "Wyrównaj temperaturę wiadra do temperatury zbiornika (±1°C)"},
            {"order": 4, "text_en": "Siphon ~30L from the bottom of the tank, removing detritus", "text_pl": "Zasyfonuj ~30L z dna zbiornika, usuwając osad"},
            {"order": 5, "text_en": "Slowly pour treated water into the tank", "text_pl": "Powoli wlej uzdatnioną wodę do zbiornika"},
            {"order": 6, "text_en": "Log the water change in the app", "text_pl": "Zaloguj wymianę wody w aplikacji"},
        ],
        "required_parts": [
            {"supply_id": None, "supply_name": "Seachem Prime", "quantity": 2, "unit": "ml"},
        ],
    },
    {
        "name": "Clean Intake Pre-filter",
        "name_pl": "Czyszczenie Gąbki Wstępnej",
        "interval_days": 10,
        "steps": [
            {"order": 1, "text_en": "Pause filter (use Feed Now or manually turn off filter plug)", "text_pl": "Zatrzymaj filtr (użyj Nakarm lub ręcznie wyłącz wtyczkę filtra)"},
            {"order": 2, "text_en": "Remove pre-filter sponge from the 16mm intake strainer", "text_pl": "Zdejmij gąbkę wstępną ze strainera wlotowego 16mm"},
            {"order": 3, "text_en": "Rinse sponge in a bucket of tank water (NOT tap water)", "text_pl": "Przepłucz gąbkę w wiadrze wody ze zbiornika (NIE z kranu)"},
            {"order": 4, "text_en": "Reattach sponge and restart filter", "text_pl": "Ponownie zamocuj gąbkę i uruchom filtr"},
            {"order": 5, "text_en": "Note new baseline watt draw on filter plug in Screen 2", "text_pl": "Zanotuj nowy bazowy pobór mocy wtyczki filtra na Ekranie 2"},
        ],
        "required_parts": [],
    },
    {
        "name": "Fluval 307 Full Filter Service",
        "name_pl": "Pełny Serwis Filtra Fluval 307",
        "interval_days": 90,
        "steps": [
            {"order": 1, "text_en": "Turn off filter plug via smart plug", "text_pl": "Wyłącz wtyczkę filtra przez inteligentną wtyczkę"},
            {"order": 2, "text_en": "Place towels under filter, close inlet/outlet taps", "text_pl": "Połóż ręczniki pod filtrem, zamknij kurki wlotowy/wylotowy"},
            {"order": 3, "text_en": "Disconnect hoses — have a bucket ready", "text_pl": "Odłącz węże — przygotuj wiadro"},
            {"order": 4, "text_en": "Open canister, remove baskets in order (4→3→2→1)", "text_pl": "Otwórz obudowę, wyjmij kosze w kolejności (4→3→2→1)"},
            {"order": 5, "text_en": "Basket 1+2: Rinse ceramic biomedia in tank water only — never tap!", "text_pl": "Kosz 1+2: Przepłucz ceramiczne biomedia wyłącznie w wodzie ze zbiornika — nie z kranu!"},
            {"order": 6, "text_en": "Basket 3: Replace Filter Carbon Pad (Fluval)", "text_pl": "Kosz 3: Wymień wkład węglowy Carbon Pad (Fluval)"},
            {"order": 7, "text_en": "Basket 4: Rinse or replace Quick-Clear Polishing Pad", "text_pl": "Kosz 4: Przepłucz lub wymień gąbkę polerującą Quick-Clear"},
            {"order": 8, "text_en": "Reassemble baskets (1→2→3→4), prime with tank water", "text_pl": "Złóż kosze (1→2→3→4), zagruntuj wodą ze zbiornika"},
            {"order": 9, "text_en": "Reconnect hoses, open taps, restart filter plug", "text_pl": "Podłącz węże, otwórz kurki, uruchom wtyczkę filtra"},
            {"order": 10, "text_en": "Check for leaks. Add Seachem Stability dose for 7 days.", "text_pl": "Sprawdź przecieki. Dodawaj dawkę Seachem Stability przez 7 dni."},
        ],
        "required_parts": [
            {"supply_id": None, "supply_name": "Filter Carbon Pad (Fluval)", "quantity": 1, "unit": "pcs"},
            {"supply_id": None, "supply_name": "Quick-Clear Polishing Pad (Fluval)", "quantity": 1, "unit": "pcs"},
        ],
    },
    {
        "name": "Weekly Water Test",
        "name_pl": "Tygodniowy Test Wody",
        "interval_days": 7,
        "steps": [
            {"order": 1, "text_en": "Open Water Tests screen, tap New Test Session", "text_pl": "Otwórz ekran Testów Wody, naciśnij Nowa Sesja Testowa"},
            {"order": 2, "text_en": "Test KH, Nitrate, Nitrite, Ammonia — always; bring jar to Seahorse Aquariums before each new fish purchase", "text_pl": "Testuj KH, azotany, azotyny, amoniak — zawsze; zanieś słoik do Seahorse Aquariums przed każdym zakupem ryb"},
            {"order": 3, "text_en": "Test Iron after ProFito dosing day", "text_pl": "Testuj żelazo po dniu dawkowania ProFito"},
            {"order": 4, "text_en": "Enter all values into the form and save", "text_pl": "Wpisz wszystkie wartości do formularza i zapisz"},
        ],
        "required_parts": [],
    },
]

CALENDAR_TASKS = [
    # ── Daily morning check — starts when first fish arrive (Step 1: Tue 2 Jun 2026) ──
    {
        "name": "Morning Check",
        "name_pl": "Sprawdzenie Poranne",
        "color": "#4fc3f7",
        "recurrence_type": "daily",
        "interval_days": None,
        "recurrence_days": [],
        "start_date": "2026-06-02",
        "end_date": None,
        "amount": "temp + filtr + ryby",
        "notes_pl": "Sprawdź temp 25-26°C, pracę filtra i bąbelki z tyłu. Czy wszystkie ryby widoczne i aktywne?",
    },
    # ── Seachem Stability — Step 2A fish addition (Tue 16 Jun) ────────────────────────
    {
        "name": "Seachem Stability 25ml",
        "name_pl": "Seachem Stability 25ml",
        "color": "#aed581",
        "recurrence_type": "daily",
        "interval_days": None,
        "recurrence_days": [],
        "start_date": "2026-06-13",
        "end_date": "2026-06-13",
        "amount": "25 ml",
        "notes_pl": "Jednorazowo po wpuszczeniu Etap A (Bystrzyk Raccoon ×12, Panda Garra ×4, Gurami ×2): wlej 25 ml Seachem Stability.",
    },
    # ── Seachem Stability — Step 2B fish addition (Tue 30 Jun) ────────────────────────
    {
        "name": "Seachem Stability 25ml",
        "name_pl": "Seachem Stability 25ml",
        "color": "#aed581",
        "recurrence_type": "daily",
        "interval_days": None,
        "recurrence_days": [],
        "start_date": "2026-06-25",
        "end_date": "2026-06-25",
        "amount": "25 ml",
        "notes_pl": "Jednorazowo po wpuszczeniu Etap B (Ołówkoryba ×12, Otonek ×6): wlej 25 ml Seachem Stability.",
    },
    # ── Seachem Stability — Step 3 fish addition (Tue 14 Jul) ─────────────────────────
    {
        "name": "Seachem Stability 25ml",
        "name_pl": "Seachem Stability 25ml",
        "color": "#aed581",
        "recurrence_type": "daily",
        "interval_days": None,
        "recurrence_days": [],
        "start_date": "2026-07-09",
        "end_date": "2026-07-09",
        "amount": "25 ml",
        "notes_pl": "Jednorazowo po wpuszczeniu Etap C (Apistogramma Double Red ×2): wlej 25 ml Seachem Stability.",
    },
    # ── ProFito — every Friday from mid-July (Fri 17 Jul, day after Step 4) ──────────
    {
        "name": "Easy-Life ProFito Fertiliser",
        "name_pl": "Nawóz: Easy-Life ProFito",
        "color": "#81c784",
        "recurrence_type": "weekdays",
        "interval_days": None,
        "recurrence_days": [4],  # Friday
        "start_date": "2026-07-17",
        "end_date": None,
        "amount": "½ dawki",
        "notes_pl": "Wlej połowę dawki zalecanej przez producenta na opakowaniu. Zawsze dzień po podmianie wody (czwartek → piątek). Zaczyna się od 17 lipca 2026.",
    },
    # ── Day-specific 19:00 feeding schedule ────────────────────────────────────────
    {
        "name": "Monday: Flakes + ½ JBL Pronovo Tab",
        "name_pl": "Poniedziałek: Płatki + ½ Tabletki JBL",
        "color": "#4dd0e1",
        "recurrence_type": "weekdays",
        "interval_days": None,
        "recurrence_days": [0],
        "start_date": "2026-06-11",
        "end_date": None,
        "amount": "szczypta płatków + ½ tabletki JBL Pronovo",
        "notes_pl": "19:00. Płatki (szczypta) + 1 tabletka JBL Pronovo łamana na pół. Rano: 15 ml Seachem Stability.",
    },
    {
        "name": "Tuesday: Flakes",
        "name_pl": "Wtorek: Płatki",
        "color": "#4dd0e1",
        "recurrence_type": "weekdays",
        "interval_days": None,
        "recurrence_days": [1],
        "start_date": "2026-06-11",
        "end_date": None,
        "amount": "szczypta płatków",
        "notes_pl": "19:00. Tylko płatki — szczypta mocno roztarta.",
    },
    {
        "name": "Wednesday: ½ JBL Tab + ¼ Algae Wafer",
        "name_pl": "Środa: ½ Tabletki JBL + ¼ Wafla",
        "color": "#00b4d8",
        "recurrence_type": "weekdays",
        "interval_days": None,
        "recurrence_days": [2],
        "start_date": "2026-06-11",
        "end_date": None,
        "amount": "½ tabletki JBL + ¼ wafla algowego",
        "notes_pl": "19:00. BEZ płatków. 1 tabletka JBL Pronovo łamana na pół + ¼ wafla algowego na piasek.",
    },
    {
        "name": "Thursday: Flakes",
        "name_pl": "Czwartek: Płatki",
        "color": "#4dd0e1",
        "recurrence_type": "weekdays",
        "interval_days": None,
        "recurrence_days": [3],
        "start_date": "2026-06-11",
        "end_date": None,
        "amount": "szczypta płatków",
        "notes_pl": "19:00. Tylko płatki — szczypta mocno roztarta.",
    },
    {
        "name": "FRIDAY: FASTING DAY",
        "name_pl": "PIĄTEK: DZIEŃ POSTU",
        "color": "#ef9a9a",
        "recurrence_type": "weekdays",
        "interval_days": None,
        "recurrence_days": [4],
        "start_date": "2026-06-11",
        "end_date": None,
        "amount": "BRAK KARMIENIA",
        "notes_pl": "Zero jedzenia przez cały piątek. Reset jelit ryb i filtra biologicznego. Nie podawaj nic, nawet wafla.",
    },
    {
        "name": "Saturday: Flakes + ½ JBL Pronovo Tab",
        "name_pl": "Sobota: Płatki + ½ Tabletki JBL",
        "color": "#4dd0e1",
        "recurrence_type": "weekdays",
        "interval_days": None,
        "recurrence_days": [5],
        "start_date": "2026-06-11",
        "end_date": None,
        "amount": "szczypta płatków + ½ tabletki JBL Pronovo",
        "notes_pl": "19:00. Płatki (szczypta) + 1 tabletka JBL Pronovo łamana na pół.",
    },
    {
        "name": "Sunday: TEST DAY + Flakes + ¼ Algae Wafer",
        "name_pl": "Niedziela: DZIEŃ TESTÓW + Płatki + ¼ Wafla",
        "color": "#ff8a65",
        "recurrence_type": "weekdays",
        "interval_days": None,
        "recurrence_days": [6],
        "start_date": "2026-06-11",
        "end_date": None,
        "amount": "pasek testowy + mała szczypta + ¼ wafla",
        "notes_pl": "Przetestuj strip + droplet: NO3, NO2, NH3, pH.\nJeśli NO3 < 25 ppm → brak podmiany. Jeśli NO3 > 25 lub NO2 > 0 → podmień wodę.\n\n19:00: mała szczypta płatków + ¼ wafla algowego na piasek.",
    },
    # ── Monday morning Seachem Stability dose (ongoing — support for new fish) ─────
    {
        "name": "Monday Morning: Seachem Stability 15ml",
        "name_pl": "Poniedziałek Rano: Seachem Stability 15ml",
        "color": "#aed581",
        "recurrence_type": "weekdays",
        "interval_days": None,
        "recurrence_days": [0],
        "start_date": "2026-06-11",
        "end_date": "2026-07-31",
        "amount": "15 ml",
        "notes_pl": "Rano, przed pracą: 15 ml Seachem Stability wlej przy odpływie filtra. Wspiera bakterie po każdym dodaniu ryb.",
    },
    # ── Weekly water change — every Thursday from Thu 4 Jun 2026 ─────────────────────
    {
        "name": "Water Change (max 4 weeks)",
        "name_pl": "Podmiana Wody (maks 4 tygodnie)",
        "color": "#29b6f6",
        "recurrence_type": "every_n_days",
        "interval_days": 28,
        "recurrence_days": [],
        "start_date": "2026-06-21",
        "end_date": None,
        "amount": "~15% (~38L)",
        "notes_pl": "WARUNEK: podmień wcześniej jeśli NO2 > 0 lub NO3 > 25 ppm lub NH3 > 0. Maks. 4 tygodnie bez podmiany niezależnie od wyników.\n\n~15% (ok. 38L) — do wiadra świeżej wody z kranu: 2 ml Seachem Prime. Wyrównaj temp do zbiornika (±1°C).\nNajbliższa podmiana: 21 czerwca 2026 (po Etap A). Długoterminowo: co 2–3 tygodnie.",
    },
    # ── Monthly substrate vacuum — last Saturday of month (first: Sat 27 Jun) ─────────
    {
        "name": "Monthly Substrate Vacuum",
        "name_pl": "Miesięczne Odmulanie Podłoża",
        "color": "#66bb6a",
        "recurrence_type": "every_n_days",
        "interval_days": 30,
        "recurrence_days": [],
        "start_date": "2026-06-27",
        "end_date": None,
        "amount": "~10 min",
        "notes_pl": (
            "Ostatnia sobota miesiąca: odmulacz delikatnie po powierzchni białego piasku — tylko tam gdzie karmisz ryby.\n"
            "Nie kopaj głęboko — tylko zbieraj brud z wierzchu. Nie ruszaj korzeni ani roślin."
        ),
    },
    # ── Fluval 307 full service — every 90 days; NEVER same day as water change ───────
    {
        "name": "Fluval 307 Filter Service",
        "name_pl": "Serwis Filtra Fluval 307",
        "color": "#ffa726",
        "recurrence_type": "every_n_days",
        "interval_days": 90,
        "recurrence_days": [],
        "start_date": "2026-08-29",
        "end_date": None,
        "amount": "~20 min",
        "notes_pl": (
            "⚠️ NIGDY tego samego dnia co podmiana wody — czekaj min. 2-3 dni!\n"
            "Najbliższy termin: sobota, 29 sierpnia 2026.\n\n"
            "Czarne gąbki wstępne: przepłucz pod letnią wodą z kranu.\n"
            "Ceramika koszyki 1+2: NIGDY pod kranówką — tylko w wodzie ze zbiornika w misce.\n"
            "Kosz 3: wymień Carbon Pad (Fluval).\n"
            "Kosz 4: przepłucz lub wymień gąbkę polerującą Quick-Clear.\n"
            "Złóż filtr, uruchom. Przez 7 kolejnych dni dodawaj dawkę Seachem Stability."
        ),
    },
    # ── Biannual: filter tubes + substrate capsules ────────────────────────────────────
    {
        "name": "Biannual Maintenance",
        "name_pl": "Konserwacja Półroczna/Roczna",
        "color": "#ab47bc",
        "recurrence_type": "every_n_days",
        "interval_days": 180,
        "recurrence_days": [],
        "start_date": "2026-11-28",
        "end_date": None,
        "amount": "co 6 mies.",
        "notes_pl": (
            "Węże filtra: jeśli przepływ wyraźnie słabszy — oczyść wyciorem do węży.\n"
            "Kapsułki nawozowe: wciśnij 1 kapsułkę głęboko pod korzenie roślin w piasek (co 6 miesięcy)."
        ),
    },
]

DEFAULT_FISH = [
    # ── Currently in tank (as of 11 June 2026) ──────────────────────────────────────
    {"name_en": "Pearl Gourami",            "name_pl": "Gurami Mozaikowe",    "latin": "Trichopodus leerii",                  "qty": 1,  "zone": "Top/Mid",       "status": "in_tank",  "temp": "24–28°C", "notes_pl": "1 szt. (płeć nieznana). Surfuje po szybie — szuka towarzystwa. Etap A (13 cze): dosypujemy 2 szt. by uzupełnić harem 1M+2F.",    "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Trichopodus_leerii_Natural_History_Museum_University_of_Pisa.jpg/330px-Trichopodus_leerii_Natural_History_Museum_University_of_Pisa.jpg"},
    {"name_en": "Five-Banded Barb (Penta)", "name_pl": "Brzanka Pięciopręga", "latin": "Desmopuntius pentazona",              "qty": 14, "zone": "Mid",            "status": "in_tank",  "temp": "23–26°C", "notes_pl": "Ławica 14 szt. Blade pomarańczowe — brak karotenoidów w diecie. Podaj artemię/cyklopsy dla koloru.",                              "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Cyprinidae_Desmopuntius_pentazona_1.jpg/330px-Cyprinidae_Desmopuntius_pentazona_1.jpg"},
    {"name_en": "False Julii Corydoras",    "name_pl": "Kirysek Fałszywy Julii","latin": "Corydoras trilineatus",             "qty": 7,  "zone": "Bottom (sand)", "status": "in_tank",  "temp": "22–26°C", "notes_pl": "7 szt. Bardzo energiczne — eksplorują całe 120 cm dna. Naturalne surfowanie po szybie (zachowanie nowego zbiornika).",          "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Corydoras_trilineatus.jpg/330px-Corydoras_trilineatus.jpg"},
    {"name_en": "Kuhli Loach",              "name_pl": "Wężyk Kuhli",          "latin": "Pangio kuhlii",                      "qty": 6,  "zone": "Caves/Cracks",  "status": "in_tank",  "temp": "24–30°C", "notes_pl": "6 szt. Nocne węgorze-czyściciele. Chowają się za korzeniam i w kokosnatch za dnia.",                                          "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Pangio_kuhlii.jpg/330px-Pangio_kuhlii.jpg"},
    {"name_en": "Amano Shrimp",             "name_pl": "Krewetka Amano",       "latin": "Caridina multidentata",              "qty": 5,  "zone": "Everywhere",    "status": "in_tank",  "temp": "20–27°C", "notes_pl": "5 szt. (2 padły ze stresu transportowego / niepowodzenia linki). Czyści biofilm z korzenia.",                                "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Amano_Garnele_%2885281493%29.jpeg/330px-Amano_Garnele_%2885281493%29.jpeg"},
    # ── Etap A — Sobota 13 Czerwca 2026 ──────────────────────────────────────────────
    {"name_en": "Raccoon Tetra",            "name_pl": "Bystrzyk Szop",        "latin": "Hemigrammus pulcher",                "qty": 12, "zone": "Mid",            "status": "arriving", "temp": "23–27°C", "notes_pl": "12 szt. Etap A — sobota 13 czerwca 2026. Aklimatyzacja 45 min ze zgaszonym Aquasky.",                                        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Hemigrammus_pulcher.jpg/330px-Hemigrammus_pulcher.jpg"},
    {"name_en": "Panda Garra",              "name_pl": "Garra Panda",          "latin": "Garra flavatra",                     "qty": 4,  "zone": "Rocks/Wood",    "status": "arriving", "temp": "23–27°C", "notes_pl": "4 szt. Etap A — sobota 13 czerwca 2026. Zeskrobują biofilm ze skał Dragon Stone.",                                      "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Panda_Garra.jpg/330px-Panda_Garra.jpg"},
    # ── Etap B — Czwartek 25 Czerwca 2026 ────────────────────────────────────────────
    {"name_en": "Purple Pencilfish",        "name_pl": "Ołówkoryba Fioletowa", "latin": "Nannostomus sp.",                    "qty": 12, "zone": "Top/Mid",        "status": "arriving", "temp": "24–28°C", "notes_pl": "12 szt. Etap B — czwartek 25 czerwca 2026. Alternatywa: 8× Cherry Barb (Puntius titteya) przy dnie.",                      "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Nannostomus_mortenthaleri.jpg/330px-Nannostomus_mortenthaleri.jpg"},
    {"name_en": "Otocinclus",               "name_pl": "Otonek Pospolity",     "latin": "Otocinclus vittatus",                "qty": 6,  "zone": "Leaves/Glass",  "status": "arriving", "temp": "22–26°C", "notes_pl": "6 szt. Etap B — czwartek 25 czerwca 2026. Czyści liście Echinodorusa i szyby.",                                        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Otocinclus_vittatus.jpg/330px-Otocinclus_vittatus.jpg"},
    # ── Etap C — Czwartek 9 Lipca 2026 ───────────────────────────────────────────────
    {"name_en": "Red Apistogramma Double Red","name_pl": "Pielęgniczka Double Red","latin": "Apistogramma agassizii \"Double Red\"","qty": 2, "zone": "Bottom/Caves","status": "arriving","temp": "24–27°C", "notes_pl": "Para (1M+1F). Etap C — czwartek 9 lipca 2026. Kupić też Liście Catappa — naturalnie obniżają pH i działają antygrzybiczo.",  "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Apistogramma_agassizii_in_aquarium.jpg/330px-Apistogramma_agassizii_in_aquarium.jpg"},
]

DEFAULT_PLANTS = [
    {"name_en": "Rotala Bangladesh",     "name_pl": None,           "latin": "Rotala sp. Bangladesh",          "location": "Left rear corner (background)",           "notes_pl": "Fast stem. Thrives on MasterLine Golden column dosing.",                  "img": None},
    {"name_en": "Alternanthera Rosanervig", "name_pl": None,        "latin": "Alternanthera reineckii",         "location": "Left mid-ground, high light access",      "notes_pl": "Demanding pink/red stem. Root tabs + daily Carbo.",                       "img": None},
    {"name_en": "Lobelia cardinalis Mini", "name_pl": None,         "latin": "Lobelia cardinalis",              "location": "Right foreground next to Dragon Stone",   "notes_pl": "Compact bushy. Sturdy, locked into sand with root tabs.",                 "img": None},
    {"name_en": "Limnophila",            "name_pl": "Limnofila",    "latin": "Limnophila sessiliflora",         "location": "Background clusters",                     "notes_pl": "Fast lacy stem. Primary biological shield against nutrient spikes.",      "img": None},
    {"name_en": "Amazon Sword",          "name_pl": "Żabienica",    "latin": "Echinodorus argentinensis",       "location": "Mid-ground focus",                        "notes_pl": "Root-feeder rosette. Relies almost entirely on buried root tabs.",        "img": None},
    {"name_en": "Ludwigia Rubin",        "name_pl": "Ludwigia",     "latin": "Ludwigia repens Rubin",           "location": "Mid-to-background",                       "notes_pl": "Deep red stem. Absorbs micro-nutrients via roots and leaves.",            "img": None},
    {"name_en": "Water Wisteria",        "name_pl": None,           "latin": "Hygrophila difformis",            "location": "Background",                              "notes_pl": "Serrated leaf stem. Rapidly consumes ammonia and nitrates.",              "img": None},
    {"name_en": "Hygrophila Sunset",     "name_pl": None,           "latin": "Hygrophila polysperma Sunset",    "location": "Mid-to-background",                       "notes_pl": "Veined leaf stem. Indicator for iron and potassium levels.",             "img": None},
    {"name_en": "Cryptocoryne Broad Leaf", "name_pl": "Kryptokoryna", "latin": "Cryptocoryne undulata",         "location": "Mid-ground shaded zones",                 "notes_pl": "Sturdy rosette. Prefers low light, root nutrition. Do not move.",        "img": None},
    {"name_en": "Hydrocotyle",           "name_pl": None,           "latin": "Hydrocotyle cf. tripartita",      "location": "Foreground / attached to hardscape",      "notes_pl": "Creeping pennywort. Fast grower, dense clover-like cushions.",           "img": None},
    {"name_en": "Monte Carlo",           "name_pl": None,           "latin": "Micranthemum Monte Carlo",        "location": "Front open sand layout",                  "notes_pl": "Miniature carpeting plant. Slow under 35% lighting. Algae via Carbo.",  "img": None},
    {"name_en": "African Water Fern",    "name_pl": None,           "latin": "Bolbitis heudelotii",             "location": "Attached to central root / Dragon Stone", "notes_pl": "True rhizome epiphyte. NEVER bury in sand. Column feed only.",          "img": None},
    {"name_en": "Bucephalandra Red",     "name_pl": None,           "latin": "Bucephalandra sp. Red",           "location": "Dragon Stone cracks / root joints",       "notes_pl": "Slow premium epiphyte. NEVER bury. MasterLine Golden only.",            "img": None},
    {"name_en": "Java Fern Narrow",      "name_pl": None,           "latin": "Microsorum pteropus Narrow",      "location": "Anchored to wood structures",             "notes_pl": "Sturdy rhizome epiphyte. NEVER bury. Grazing-resistant.",               "img": None},
]


async def seed(session: AsyncSession):
    """Seeds reference data if tables are empty."""
    # Water test parameters
    existing = await session.scalar(select(WaterTestParameter).limit(1))
    if not existing:
        for key, name_en, name_pl, unit, min_safe, max_safe, category in WATER_TEST_PARAMS:
            freq, effect_en, effect_pl = WATER_TEST_REMINDER_DEFAULTS.get(key, (None, None, None))
            session.add(WaterTestParameter(
                key=key, name_en=name_en, name_pl=name_pl,
                unit=unit, min_safe=min_safe, max_safe=max_safe, category=category,
                test_frequency_days=freq, high_effect_en=effect_en, high_effect_pl=effect_pl,
            ))

    # Supplies
    existing_supply = await session.scalar(select(Supply).limit(1))
    if not existing_supply:
        supply_map = {}
        for name, name_pl, stype, amount, unit, thresh in DEFAULT_SUPPLIES:
            s = Supply(name=name, name_pl=name_pl, type=stype,
                       current_amount=amount, unit=unit, min_threshold=thresh)
            session.add(s)
            supply_map[name] = s
        await session.flush()

        # Dosing tasks linked to supplies
        for supply_name, dose, unit, time_of_day, notes_en, notes_pl in DEFAULT_DOSING_TASKS:
            if supply_name in supply_map:
                session.add(DosingTask(
                    supply_id=supply_map[supply_name].id,
                    dose_amount=dose, dose_unit=unit,
                    time_of_day=time_of_day,
                    notes=notes_en, notes_pl=notes_pl,
                ))

    # Feeding schedule
    existing_feed = await session.scalar(select(FeedingSchedule).limit(1))
    if not existing_feed:
        for t in DEFAULT_FEEDING_TIMES:
            session.add(FeedingSchedule(time_of_day=t, active=True))

    # Maintenance tasks
    existing_maint = await session.scalar(select(MaintenanceTask).limit(1))
    if not existing_maint:
        now = datetime.utcnow()
        for task_data in DEFAULT_MAINTENANCE_TASKS:
            task = MaintenanceTask(
                name=task_data["name"],
                name_pl=task_data["name_pl"],
                interval_days=task_data["interval_days"],
                next_due=now + timedelta(days=task_data["interval_days"]),
            )
            task.steps = task_data["steps"]
            task.required_parts = task_data["required_parts"]
            session.add(task)

    # Calendar tasks
    existing_cal = await session.scalar(select(CalendarTask).limit(1))
    if not existing_cal:
        for t in CALENDAR_TASKS:
            task = CalendarTask(
                name=t["name"],
                name_pl=t["name_pl"],
                color=t["color"],
                recurrence_type=t["recurrence_type"],
                interval_days=t["interval_days"],
                start_date=t["start_date"],
                end_date=t["end_date"],
                amount=t["amount"],
                notes_pl=t.get("notes_pl"),
            )
            task.recurrence_days = t["recurrence_days"]
            session.add(task)

    # Milestone water test — 3 June 2026 (cycle complete, first fish added)
    existing_wt = await session.scalar(select(WaterTestSession).limit(1))
    if not existing_wt:
        param_map = {
            row.key: row
            for row in (await session.scalars(select(WaterTestParameter))).all()
        }
        test_session = WaterTestSession(
            tested_at=datetime(2026, 6, 3, 18, 0, 0),
            notes="Cycle complete. NO2 = 0. First fish added same day (Pearl Gourami + Penta Barb + Amano Shrimp). Confirmed by Seahorse Aquariums.",
        )
        session.add(test_session)
        await session.flush()
        milestone_readings = [
            # key      value   out_of_range  notes
            ("nitrite",   0.0,  False, "Cycling complete"),
            ("nitrate",  10.0,  False, "Safe — plants will uptake"),
            ("ammonia",   0.0,  False, None),
            ("ph",        7.4,  False, None),
        ]
        for key, value, oor, notes in milestone_readings:
            if key in param_map:
                session.add(WaterTestReading(
                    session_id=test_session.id,
                    parameter_id=param_map[key].id,
                    value=value,
                    out_of_range=oor,
                    notes=notes,
                ))

    # Fish
    existing_fish = await session.scalar(select(Fish).limit(1))
    if not existing_fish:
        for f in DEFAULT_FISH:
            session.add(Fish(**f))

    # Plants
    existing_plants = await session.scalar(select(Plant).limit(1))
    if not existing_plants:
        for p in DEFAULT_PLANTS:
            session.add(Plant(**p))

    await session.commit()
