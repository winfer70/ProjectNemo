"""Seeds water_test_parameters and default maintenance tasks + supplies on first run."""
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.orm import (
    CalendarTask,
    DosingTask,
    FeedingSchedule,
    MaintenanceTask,
    Supply,
    WaterTestParameter,
    WaterTestSession,
    WaterTestReading,
)


WATER_TEST_PARAMS = [
    # key            name_en                          name_pl                      unit    min_safe  max_safe  category
    ("temp",        "Temperature",                   "Temperatura",               "°C",   24.5,     27.5,     "continuous"),
    ("ph",          "pH",                            "pH",                        "",     7.2,      7.6,      "manual"),
    ("tds",         "TDS / Conductivity",            "TDS / Przewodność",         "ppm",  100,      500,      "continuous"),
    ("orp",         "ORP",                           "ORP",                       "mV",   150,      450,      "continuous"),
    ("kh",          "KH / Total Alkalinity",         "KH / Twardość Węglanowa",   "dKH",  3,        12,       "manual"),
    ("nitrate",     "Nitrate (NO3)",                 "Azotany (NO3)",             "mg/L", None,     30.0,     "manual"),
    ("nitrite",     "Nitrite (NO2)",                 "Azotyny (NO2)",             "mg/L", None,     0.0,      "manual"),
    ("ammonia",     "Ammonia (NH3/NH4+)",            "Amoniak (NH3/NH4+)",        "mg/L", None,     0.0,      "manual"),
    ("copper",      "Copper (Cu)",                   "Miedź (Cu)",                "mg/L", None,     0.05,     "manual"),
    ("iron",        "Iron (Fe)",                     "Żelazo (Fe)",               "mg/L", 0.05,     0.3,      "manual"),
    ("chlorine",    "Free Chlorine",                 "Chlor Wolny",               "mg/L", None,     0.0,      "manual"),
]

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
]

DEFAULT_DOSING_TASKS = [
    # supply_name               dose   unit  time    notes_en                                                              notes_pl
    ("Seachem Prime",           2.0,  "ml", None,   "Water change day only (Thursdays) — 2 ml per ~30L bucket",           "Tylko w dzień podmiany wody (czwartek) — 2 ml na ~30L wiadro"),
    ("Easy-Life ProFito",      12.5,  "ml", None,   "Weekly fertiliser, half-dose — Fridays from mid-July (from 17 Jul)", "Tygodniowy nawóz, połowa dawki — piątki od połowy lipca (od 17 lip)"),
    ("Seachem Stability",      25.0,  "ml", "08:00","Bacteria boost: 30 ml/day Thu–Sun after Step 1; 25 ml once after Steps 2–4", "Bakterie: 30 ml/dzień czw–niedz po Kroku 1; 25 ml jednorazowo po Krokach 2–4"),
]

DEFAULT_FEEDING_TIMES = ["08:00", "18:00"]

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
    # ── Phase 1 morning: algae wafer for Amano shrimp (Jun 2–15, before flakes start) ──
    {
        "name": "Morning: Green Algae Wafer (Shrimp)",
        "name_pl": "Rano: Zielony Wafel Algowy (Krewetki)",
        "color": "#00b4d8",
        "recurrence_type": "daily",
        "interval_days": None,
        "recurrence_days": [],
        "start_date": "2026-06-02",
        "end_date": "2026-06-15",
        "amount": "1 wafel",
        "notes_pl": "1 wafel algowy na piasek dla krewetek Amano. Tylko do 15 czerwca — od 16 czerwca (Krok 2) przełącz na płatki rano.",
    },
    # ── Phase 1 evening: crushed flakes for barbs + Gourami (Jun 2–15) ──────────────
    {
        "name": "Evening: Crushed Flakes (Barbs & Gourami)",
        "name_pl": "Wieczór: Roztarte Płatki (Barwniki i Gurami)",
        "color": "#4dd0e1",
        "recurrence_type": "daily",
        "interval_days": None,
        "recurrence_days": [],
        "start_date": "2026-06-02",
        "end_date": "2026-06-15",
        "amount": "szczypta (roztarte)",
        "notes_pl": "Mała szczypta płatków mocno roztartych w palcach — dla barwników Penta i Gurami Perłowych. Tylko do 15 czerwca.",
    },
    # ── Morning flakes — from Step 2 (Tue 16 Jun 2026) ───────────────────────────────
    {
        "name": "Morning: JBL Pronovo Bel Flakes",
        "name_pl": "Rano: JBL Pronovo Bel Płatki",
        "color": "#4dd0e1",
        "recurrence_type": "daily",
        "interval_days": None,
        "recurrence_days": [],
        "start_date": "2026-06-16",
        "end_date": None,
        "amount": "szczypta (roztarte)",
        "notes_pl": "Mała szczypta JBL Pronovo Bel MOCNO roztarta w palcach → do toni wodnej. Dla Tetry Kardynała, Gurami Perłowych i ławicy barwników Penta.",
    },
    # ── Odd evenings: algae wafers from Jun 17 (day after Step 2) ────────────────────
    {
        "name": "Evening: Green Algae Wafers",
        "name_pl": "Wieczór: Zielone Wafle Algowe",
        "color": "#00b4d8",
        "recurrence_type": "every_n_days",
        "interval_days": 2,
        "recurrence_days": [],
        "start_date": "2026-06-17",
        "end_date": None,
        "amount": "1–2 wafle",
        "notes_pl": "Połóż na piasku dla otoinkluzów i krewetek — nieparzyste wieczory.\nW niedzielę: pomiń — zamiast tego podaj artemię.",
    },
    # ── Sunday artemia treat — from Step 2 onward (first Sun on/after 16 Jun = 21 Jun) ─
    {
        "name": "Sunday Treat: Artemia",
        "name_pl": "Niedziela: Artemia (Przysmak)",
        "color": "#ff8a65",
        "recurrence_type": "weekdays",
        "interval_days": None,
        "recurrence_days": [6],  # Sunday
        "start_date": "2026-06-21",
        "end_date": None,
        "amount": "¼ kostki mrożonej",
        "notes_pl": "Rozmrożona ¼ kostki mrożonej artemii dla wszystkich ryb. Zamiast tabletek i waflów wieczorem.",
    },
    # ── Even evenings: Corydoras tablets — starts Step 3 (Tue 30 Jun 2026) ────────────
    {
        "name": "Evening: JBL Corydoras Tablets",
        "name_pl": "Wieczór: Tabletki JBL Corydoras",
        "color": "#29b6f6",
        "recurrence_type": "every_n_days",
        "interval_days": 2,
        "recurrence_days": [],
        "start_date": "2026-06-30",
        "end_date": None,
        "amount": "2–3 tabletki → piasek",
        "notes_pl": "Wciśnij 2-3 tabletki w piasek przy kirysach Sterbai i otoinkluzach — parzyste wieczory.\nW niedzielę: pomiń — zamiast tego podaj artemię.",
    },
    # ── Seachem Stability — Step 1 post-add: 30 ml/day Thu 4 Jun → Sun 7 Jun ─────────
    {
        "name": "Seachem Stability 30ml",
        "name_pl": "Seachem Stability 30ml",
        "color": "#aed581",
        "recurrence_type": "daily",
        "interval_days": None,
        "recurrence_days": [],
        "start_date": "2026-06-04",
        "end_date": "2026-06-07",
        "amount": "30 ml",
        "notes_pl": "Po dodaniu ryb Krok 1 (2 cze): 30 ml/dzień od czwartku 4 cze do niedzieli 7 cze, następnie STOP.",
    },
    # ── Seachem Stability — Step 2 fish addition (Tue 16 Jun) ─────────────────────────
    {
        "name": "Seachem Stability 25ml",
        "name_pl": "Seachem Stability 25ml",
        "color": "#aed581",
        "recurrence_type": "daily",
        "interval_days": None,
        "recurrence_days": [],
        "start_date": "2026-06-16",
        "end_date": "2026-06-16",
        "amount": "25 ml",
        "notes_pl": "Jednorazowo po wpuszczeniu Kroku 2 (Tetra Kardynał ×18, Apistogramma Double Red ×2): wlej 25 ml Seachem Stability.",
    },
    # ── Seachem Stability — Step 3 fish addition (Tue 30 Jun) ─────────────────────────
    {
        "name": "Seachem Stability 25ml",
        "name_pl": "Seachem Stability 25ml",
        "color": "#aed581",
        "recurrence_type": "daily",
        "interval_days": None,
        "recurrence_days": [],
        "start_date": "2026-06-30",
        "end_date": "2026-06-30",
        "amount": "25 ml",
        "notes_pl": "Jednorazowo po wpuszczeniu Kroku 3 (Kiryski Sterbai ×8, Otoinkluzy ×6, Penta Barb top-up ×6): wlej 25 ml Seachem Stability.",
    },
    # ── Seachem Stability — Step 4 fish addition (Tue 14 Jul) ─────────────────────────
    {
        "name": "Seachem Stability 25ml",
        "name_pl": "Seachem Stability 25ml",
        "color": "#aed581",
        "recurrence_type": "daily",
        "interval_days": None,
        "recurrence_days": [],
        "start_date": "2026-07-14",
        "end_date": "2026-07-14",
        "amount": "25 ml",
        "notes_pl": "Jednorazowo po wpuszczeniu Kroku 4 (Panda Garra ×4): wlej 25 ml Seachem Stability.",
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
    # ── Weekly water change — every Thursday from Thu 4 Jun 2026 ─────────────────────
    {
        "name": "Weekly Water Change",
        "name_pl": "Tygodniowa Wymiana Wody",
        "color": "#29b6f6",
        "recurrence_type": "weekdays",
        "interval_days": None,
        "recurrence_days": [3],  # Thursday
        "start_date": "2026-06-04",
        "end_date": None,
        "amount": "~30L (~30%)",
        "notes_pl": (
            "Co czwartek: spuść ~30L (1 wiadro). Do wiadra świeżej wody z kranu: 2 ml Seachem Prime. Wyrównaj temp do zbiornika (±1°C).\n"
            "Przed nalaniem: przetarcie przedniej szyby od środka czystą gąbką. Obcięcie żółtych/zniszczonych liści."
        ),
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


async def seed(session: AsyncSession):
    """Seeds reference data if tables are empty."""
    # Water test parameters
    existing = await session.scalar(select(WaterTestParameter).limit(1))
    if not existing:
        for key, name_en, name_pl, unit, min_safe, max_safe, category in WATER_TEST_PARAMS:
            session.add(WaterTestParameter(
                key=key, name_en=name_en, name_pl=name_pl,
                unit=unit, min_safe=min_safe, max_safe=max_safe, category=category,
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

    await session.commit()
