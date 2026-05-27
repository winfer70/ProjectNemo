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
)


WATER_TEST_PARAMS = [
    # key            name_en                          name_pl                      unit    min_safe  max_safe  category
    ("temp",        "Temperature",                   "Temperatura",               "°C",   24.5,     27.5,     "continuous"),
    ("ph",          "pH",                            "pH",                        "",     6.0,      6.8,      "manual"),
    ("tds",         "TDS / Conductivity",            "TDS / Przewodność",         "ppm",  100,      500,      "continuous"),
    ("orp",         "ORP",                           "ORP",                       "mV",   150,      450,      "continuous"),
    ("kh",          "KH / Total Alkalinity",         "KH / Twardość Węglanowa",   "dKH",  3,        12,       "manual"),
    ("nitrate",     "Nitrate (NO3)",                 "Azotany (NO3)",             "mg/L", None,     25.0,     "manual"),
    ("nitrite",     "Nitrite (NO2)",                 "Azotyny (NO2)",             "mg/L", None,     0.1,      "manual"),
    ("ammonia",     "Ammonia (NH3/NH4+)",            "Amoniak (NH3/NH4+)",        "mg/L", None,     0.25,     "manual"),
    ("copper",      "Copper (Cu)",                   "Miedź (Cu)",                "mg/L", None,     0.05,     "manual"),
    ("iron",        "Iron (Fe)",                     "Żelazo (Fe)",               "mg/L", 0.05,     0.3,      "manual"),
    ("chlorine",    "Free Chlorine",                 "Chlor Wolny",               "mg/L", None,     0.0,      "manual"),
]

DEFAULT_SUPPLIES = [
    # name                      name_pl                    type      amount  unit  min_thresh
    ("Seachem Prime",           "Seachem Prime",            "liquid", 500,   "ml", 50),
    ("Seachem Stability",       "Seachem Stability",        "liquid", 500,   "ml", 50),
    ("Easy-Life ProFito",       "Easy-Life ProFito",        "liquid", 500,   "ml", 50),
    ("Easy-Life EasyCarbo",     "Easy-Life EasyCarbo",      "liquid", 500,   "ml", 50),
    ("Filter Carbon/Phosphate", "Węgiel/Fosforan do filtra","part",   2,     "pcs", 1),
    ("Polishing Pad",           "Gąbka polerująca",         "part",   2,     "pcs", 1),
    ("Pre-filter Sponge",       "Gąbka wstępna",            "part",   2,     "pcs", 1),
]

DEFAULT_DOSING_TASKS = [
    # supply_name               dose   unit  time    notes_en                             notes_pl
    ("Easy-Life EasyCarbo",     5.0,  "ml", "08:00", "Daily liquid carbon dose",         "Dzienna dawka węgla ciekłego"),
    ("Easy-Life ProFito",      12.5,  "ml", None,    "Weekly fertiliser (252L full dose)","Tygodniowy nawóz (252L pełna dawka)"),
    ("Seachem Stability",      16.0,  "ml", "08:00", "Daily bacteria dose (7 days after fish additions)", "Dzienna dawka bakterii (7 dni po dodaniu ryb)"),
]

DEFAULT_FEEDING_TIMES = ["08:00", "18:00"]

DEFAULT_MAINTENANCE_TASKS = [
    {
        "name": "Partial Water Change (20-30%)",
        "name_pl": "Częściowa Wymiana Wody (20-30%)",
        "interval_days": 7,
        "steps": [
            {"order": 1, "text_en": "Prepare 2-3 × 25L buckets of tap water", "text_pl": "Przygotuj 2-3 × 25L wiadra wody z kranu"},
            {"order": 2, "text_en": "Add Seachem Prime to each bucket (1 ml per 25L) and mix", "text_pl": "Dodaj Seachem Prime do każdego wiadra (1 ml na 25L) i wymieszaj"},
            {"order": 3, "text_en": "Match bucket temperature to tank temperature (±1°C)", "text_pl": "Wyrównaj temperaturę wiadra do temperatury zbiornika (±1°C)"},
            {"order": 4, "text_en": "Siphon 50-75L from the bottom of the tank, removing detritus", "text_pl": "Zasyfonuj 50-75L z dna zbiornika, usuwając osad"},
            {"order": 5, "text_en": "Slowly pour treated water into the tank", "text_pl": "Powoli wlej uzdatnioną wodę do zbiornika"},
            {"order": 6, "text_en": "Log the water change in the app", "text_pl": "Zaloguj wymianę wody w aplikacji"},
        ],
        "required_parts": [
            {"supply_id": None, "supply_name": "Seachem Prime", "quantity": 3, "unit": "ml"},
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
            {"order": 6, "text_en": "Basket 3: Replace carbon + phosphate remover media", "text_pl": "Kosz 3: Wymień węgiel aktywny + pochłaniacz fosforanów"},
            {"order": 7, "text_en": "Basket 4: Rinse or replace Quick-Clear polishing pad", "text_pl": "Kosz 4: Przepłucz lub wymień gąbkę polerującą Quick-Clear"},
            {"order": 8, "text_en": "Reassemble baskets (1→2→3→4), prime with tank water", "text_pl": "Złóż kosze (1→2→3→4), zagruntuj wodą ze zbiornika"},
            {"order": 9, "text_en": "Reconnect hoses, open taps, restart filter plug", "text_pl": "Podłącz węże, otwórz kurki, uruchom wtyczkę filtra"},
            {"order": 10, "text_en": "Check for leaks. Add Seachem Stability dose for 7 days.", "text_pl": "Sprawdź przecieki. Dodawaj dawkę Seachem Stability przez 7 dni."},
        ],
        "required_parts": [
            {"supply_id": None, "supply_name": "Filter Carbon/Phosphate", "quantity": 1, "unit": "pcs"},
            {"supply_id": None, "supply_name": "Polishing Pad", "quantity": 1, "unit": "pcs"},
        ],
    },
    {
        "name": "Weekly Water Test",
        "name_pl": "Tygodniowy Test Wody",
        "interval_days": 7,
        "steps": [
            {"order": 1, "text_en": "Open Water Tests screen, tap New Test Session", "text_pl": "Otwórz ekran Testów Wody, naciśnij Nowa Sesja Testowa"},
            {"order": 2, "text_en": "Test KH, Nitrate, Nitrite, Ammonia — always", "text_pl": "Testuj KH, azotany, azotyny, amoniak — zawsze"},
            {"order": 3, "text_en": "Test Iron after ProFito dosing day", "text_pl": "Testuj żelazo po dniu dawkowania ProFito"},
            {"order": 4, "text_en": "Enter all values into the form and save", "text_pl": "Wpisz wszystkie wartości do formularza i zapisz"},
        ],
        "required_parts": [],
    },
]

CALENDAR_TASKS = [
    {
        # Every day: morning check + phased evening feeding
        "name": "Daily Check & Feeding",
        "name_pl": "Dzienny Przegląd i Karmienie",
        "color": "#4fc3f7",
        "recurrence_type": "daily",
        "interval_days": None,
        "recurrence_days": [],
        "start_date": "2026-05-28",
        "end_date": None,
        "amount": "rano + wieczór",
        "notes_pl": (
            "Codziennie rano: sprawdź temp 25-26°C, pracę filtra i bąbelki — czy wszystkie ryby widoczne?\n\n"
            "FAZA 1 (29 maja – 11 czerwca) — wieczorem:\n"
            "Dni parzyste (pt, nd, wt…): 1 tabletka JBL Pronovo Corydoras Tab M → na piasek, przy kirysach.\n"
            "Dni nieparzyste (sb, pn, śr…): 1 wafel Tropical Green Algae Wafers → na piasek, dla otosków i krewetek.\n\n"
            "FAZA 2 (od 12 czerwca) — karmisz 2× dziennie:\n"
            "Rano (przed pracą): mała szczypta JBL Pronovo Bel MOCNO roztarta w palcach → do toni wodnej (skalary, ławica).\n"
            "Wieczór parzyste: 3 tabletki JBL Pronovo Corydoras → na piasek (kiryski + piskorki).\n"
            "Wieczór nieparzyste: 2 wafle Tropical Green Algae Wafers → na piasek (otoski + phantom).\n"
            "Niedziela wieczór (przysmak): zamiast tabletek/waflów — 1/4 kostki mrożonej artemii dla wszystkich.\n\n"
            "Seachem Stability: 25 ml wieczorem 28 maja, 25 ml rano 29/30/31 maja. Od 1 czerwca STOP.\n"
            "Jednorazowe dawki Stability 25 ml: 11 czerwca (Krok 2) i 25 czerwca (Krok 3)."
        ),
    },
    {
        # Every Thursday: water change, Prime, glass cleaning, plant trimming
        "name": "Weekly Water Change",
        "name_pl": "Tygodniowa Wymiana Wody",
        "color": "#29b6f6",
        "recurrence_type": "weekdays",
        "interval_days": None,
        "recurrence_days": [3],  # Thursday
        "start_date": "2026-06-04",
        "end_date": None,
        "amount": "3 wiadra (~30L)",
        "notes_pl": (
            "Co czwartek: spuść 3 wiadra (~30L). Do każdego wiadra świeżej wody z kranu: 2-3 krople Seachem Prime. Wyrównaj temp do zbiornika (±1°C).\n"
            "Przed nalaniem: przetarcie przedniej szyby od środka czystą gąbką. Obcięcie żółtych/zniszczonych liści Żabienicy.\n\n"
            "Pierwsza podmiana: czwartek, 4 czerwca 2026.\n\n"
            "Od 11 czerwca (Piątek po podmianie): Easy-Life ProFito — połowa dawki zalecanej na opakowaniu.\n"
            "Seachem Stability (jednorazowo): 25 ml w czwartek 11 czerwca (wpuszczenie Kroku 2) i 25 ml 25 czerwca (Krok 3)."
        ),
    },
    {
        # Last Saturday of month: substrate vacuum over white sand
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
    {
        # Every 3 months: Fluval 307 full service — NEVER same day as water change
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
            "Czarne gąbki wstępne (intake strainer): przepłucz pod letnią wodą z kranu.\n"
            "Ceramika koszyki 1+2: NIGDY pod kranówką — przepłucz wyłącznie w wodzie ze zbiornika w misce.\n"
            "Kosz 3: wymień węgiel aktywny + pochłaniacz fosforanów.\n"
            "Kosz 4: przepłucz lub wymień gąbkę polerującą Quick-Clear.\n"
            "Złóż filtr, uruchom. Przez 7 kolejnych dni dodawaj dawkę Seachem Stability."
        ),
    },
    {
        # Every 6 months: filter tubes + substrate fertilizer capsules
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
            "Kapsułki nawozowe: wciśnij 1 kapsułkę głęboko pod korzenie Żabienicy i kryptokoryn w piasek (co 6 miesięcy)."
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

    await session.commit()
