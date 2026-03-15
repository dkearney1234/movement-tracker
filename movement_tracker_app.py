import json
from pathlib import Path
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components

# ============================================================
# Page config
# ============================================================
st.set_page_config(
    page_title="Movement Tracker",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# Styling
# ============================================================
CUSTOM_CSS = """
<style>
    :root {
        --bg: #131415;
        --bg-2: #0f1814;
        --panel: rgba(41, 40, 41, 0.98);
        --panel-2: rgba(19, 20, 21, 0.99);
        --panel-soft: rgba(254, 255, 255, 0.04);
        --text: #feffff;
        --muted: rgba(254, 255, 255, 0.68);
        --accent: #3aaf48;
        --accent-2: #05462d;
        --accent-red: #fa4d56;
        --border: rgba(254, 255, 255, 0.08);
        --shadow: 0 18px 40px rgba(0, 0, 0, 0.34);
        --glow: 0 0 0 1px rgba(58, 175, 72, 0.08), 0 18px 40px rgba(0, 0, 0, 0.34);
        --radius-xl: 26px;
        --radius-lg: 20px;
        --radius-md: 16px;
    }

    html, body, [class*="css"] {
        color: var(--text);
    }

    .stApp {
        background:
            radial-gradient(circle at top center, rgba(58, 175, 72, 0.24), transparent 26%),
            radial-gradient(circle at 20% 10%, rgba(5, 70, 45, 0.52), transparent 28%),
            linear-gradient(180deg, #16261d 0%, #131415 18%, #131415 100%);
        color: var(--text);
    }

    .block-container {
        max-width: 760px;
        padding-top: 5.2rem;
        padding-bottom: 6rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    h1, h2, h3, p, label, span, div {
        color: var(--text);
    }

    .hero-card {
        background: linear-gradient(180deg, #05462d 0%, #131415 100%);
        border: 1px solid rgba(254, 255, 255, 0.14);
        border-radius: 30px;
        padding: 1.7rem 1.35rem;
        color: var(--text);
        box-shadow: 0 22px 52px rgba(0, 0, 0, 0.42);
        margin-bottom: 1.15rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .hero-card::before {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 30px;
        padding: 1px;
        background: linear-gradient(135deg, rgba(58, 175, 72, 0.55), rgba(254, 255, 255, 0.10));
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }

    .hero-eyebrow {
        font-size: 0.8rem;
        color: rgba(254, 255, 255, 0.76);
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.48rem;
        font-weight: 800;
    }

    .hero-title {
        font-size: 2.05rem;
        font-weight: 800;
        line-height: 1.06;
        margin-bottom: 0.45rem;
        color: #3aaf48;
        text-shadow: 0 0 18px rgba(58, 175, 72, 0.16);
    }

    .hero-subtitle {
        font-size: 0.99rem;
        line-height: 1.55;
        color: rgba(254, 255, 255, 0.84);
        max-width: 34rem;
        margin: 0 auto;
    }

    .metric-wrap {
        display: none;
    }

    .hero-stats-row {
        display: flex;
        justify-content: center;
        gap: 0.8rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }

    .hero-stat {
        min-width: 170px;
        padding: 0.78rem 1rem;
        border-radius: 18px;
        background: rgba(254, 255, 255, 0.05);
        border: 1px solid rgba(254, 255, 255, 0.08);
        text-align: center;
    }

    .hero-stat-number {
        font-size: 1.24rem;
        font-weight: 800;
        color: #feffff;
        line-height: 1.05;
    }

    .hero-stat-label {
        margin-top: 0.18rem;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        color: rgba(254, 255, 255, 0.68);
        text-transform: lowercase;
    }

    .view-wrap {
        display: flex;
        justify-content: center;
        margin: -0.1rem auto 0.35rem auto;
        width: 100%;
    }

    .goal-circles-wrap {
        display: flex;
        justify-content: space-between;
        gap: 0.8rem;
        flex-wrap: nowrap;
        width: 100%;
        margin: -0.05rem 0 0.12rem 0;
        overflow-x: auto;
        overflow-y: hidden;
        padding-bottom: 0.15rem;
        -ms-overflow-style: none;
        scrollbar-width: none;
    }

    .goal-circles-wrap::-webkit-scrollbar {
        display: none;
    }

    .goal-circle-item {
        flex: 0 0 auto;
        min-width: 78px;
        text-align: center;
    }

    .goal-circle-label {
        font-size: 0.72rem;
        line-height: 1.08;
        font-weight: 700;
        color: var(--text);
        min-height: 1.8rem;
        margin-bottom: 0.42rem;
        display: flex;
        align-items: flex-end;
        justify-content: center;
        text-align: center;
    }

    .goal-circle {
        --pct: 0;
        width: 72px;
        height: 72px;
        border-radius: 50%;
        background: conic-gradient(#3aaf48 calc(var(--pct) * 1%), rgba(0,0,0,0.84) 0);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        box-shadow: 0 10px 22px rgba(0,0,0,0.28);
        border: 1px solid rgba(254,255,255,0.08);
    }

    .goal-circle-inner {
        width: 72px;
        height: 72px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
        font-weight: 800;
        color: #131415;
        background: transparent;
    }

    .goal-circle-text-dark {
        color: #feffff;
    }

    .section-label {
        font-size: 0.78rem;
        color: rgba(254, 255, 255, 0.58);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 800;
        margin: 1.1rem 0 0.7rem 0;
    }

    .goal-strip {
        display: flex;
        gap: 0.45rem;
        width: 100%;
        overflow-x: auto;
        overflow-y: hidden;
        padding-bottom: 0.2rem;
        margin-bottom: 0.5rem;
        scroll-snap-type: x proximity;
        -ms-overflow-style: none;
        scrollbar-width: none;
    }

    .goal-strip::-webkit-scrollbar {
        display: none;
    }

    .goal-tile {
        flex: 0 0 110px;
        min-width: 110px;
        max-width: 110px;
        background: linear-gradient(180deg, rgba(41, 40, 41, 0.96), rgba(19, 20, 21, 0.98));
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 0.42rem 0.46rem;
        box-shadow: var(--shadow);
        min-height: unset;
        scroll-snap-align: start;
    }

    .goal-tile.complete {
        background:
            radial-gradient(circle at top center, rgba(58, 175, 72, 0.08), transparent 48%),
            linear-gradient(180deg, rgba(5, 70, 45, 0.86), rgba(19, 20, 21, 0.98));
        border: 1px solid rgba(58, 175, 72, 0.22);
        box-shadow: var(--glow);
    }

    .goal-card {
        background: transparent;
        border: none;
        border-radius: 0;
        padding: 0;
        box-shadow: none;
        margin-bottom: 0;
        min-height: unset;
    }

    .goal-card.complete {
        background: transparent;
        border: none;
        box-shadow: none;
    }

    .goal-top {
        display: none;
    }

    .goal-name {
        font-size: 0.66rem;
        font-weight: 700;
        color: var(--text);
        line-height: 1.02;
        letter-spacing: -0.01em;
        margin-bottom: 0.18rem;
    }

    .goal-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.1rem 0.3rem;
        border-radius: 999px;
        font-size: 0.48rem;
        font-weight: 800;
        background: rgba(254, 255, 255, 0.06);
        color: rgba(254, 255, 255, 0.76);
        border: 1px solid rgba(254, 255, 255, 0.06);
        white-space: nowrap;
        margin-top: 0.14rem;
        line-height: 1.1;
    }

    .goal-pill.complete {
        background: rgba(58, 175, 72, 0.16);
        color: #8ef6a0;
        border: 1px solid rgba(58, 175, 72, 0.18);
    }

    .goal-metrics {
        display: flex;
        align-items: baseline;
        gap: 0.12rem;
        margin-bottom: 0.06rem;
    }

    .goal-number {
        font-size: 0.92rem;
        font-weight: 800;
        line-height: 1;
        color: var(--text);
    }

    .goal-target {
        color: rgba(254, 255, 255, 0.62);
        font-size: 0.56rem;
    }

    .goal-caption {
        display: none;
    }

    .planner-card {
        background:
            radial-gradient(circle at 20% 10%, rgba(58, 175, 72, 0.12), transparent 34%),
            linear-gradient(135deg, rgba(41, 40, 41, 0.98) 0%, rgba(19, 20, 21, 1) 72%);
        border: 1px solid rgba(254, 255, 255, 0.11);
        border-radius: 28px;
        padding: 1rem 1.2rem;
        box-shadow: 0 20px 44px rgba(0, 0, 0, 0.42);
        margin-top: 1.2rem;
        margin-bottom: 0.3rem;
        position: relative;
        overflow: hidden;
    }

    .planner-card::before {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 28px;
        padding: 1px;
        background: linear-gradient(135deg, rgba(58, 175, 72, 0.28), rgba(254, 255, 255, 0.08));
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }

    .planner-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.85rem;
        margin-bottom: 0;
        position: relative;
        min-height: 0;
        padding: 0.18rem 0.05rem;
    }

    .planner-day {
        font-size: 2.48rem;
        font-weight: 800;
        color: #3aaf48;
        text-align: left;
        width: auto;
        line-height: 0.98;
        letter-spacing: -0.03em;
        text-shadow: 0 0 18px rgba(58, 175, 72, 0.16);
        flex: 1 1 auto;
    }

    .planner-header .today-badge {
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.16rem;
        padding: 0.5rem 0.8rem;
        border-radius: 999px;
        background: linear-gradient(180deg, rgba(58, 175, 72, 0.18), rgba(5, 70, 45, 0.22));
        color: #8ef6a0;
        border: 1px solid rgba(58, 175, 72, 0.22);
        font-size: 0.76rem;
        font-weight: 800;
        min-width: 5.7rem;
        line-height: 1.02;
        text-align: center;
        box-shadow: 0 8px 20px rgba(5, 70, 45, 0.22);
        flex: 0 0 auto;
    }

    .completion-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.34rem 0.7rem;
        border-radius: 999px;
        background: rgba(254, 255, 255, 0.05);
        color: rgba(254, 255, 255, 0.72);
        border: 1px solid rgba(254, 255, 255, 0.08);
        font-size: 0.76rem;
        font-weight: 800;
        margin: 0.35rem 0 0.5rem 0;
    }

    .completion-pill.complete {
        background: rgba(58, 175, 72, 0.16);
        color: #8ef6a0;
        border: 1px solid rgba(58, 175, 72, 0.2);
    }

    .period-card {
        background: transparent;
        border: none;
        border-radius: 0;
        padding: 0;
        margin-bottom: 0;
        box-shadow: none;
    }

    .period-card.complete {
        background: transparent;
        border: none;
        box-shadow: none;
    }

    .summary-card {
        background: linear-gradient(180deg, rgba(41, 40, 41, 0.96), rgba(19, 20, 21, 0.98));
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 0.85rem 1rem;
        box-shadow: var(--shadow);
        margin-top: 0.8rem;
    }

    .summary-line {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.9rem;
        padding: 0.58rem 0;
        border-bottom: 1px solid rgba(254, 255, 255, 0.06);
        font-size: 0.95rem;
        color: var(--text);
    }

    .summary-line:last-child {
        border-bottom: none;
    }

    .summary-name {
        display: inline-block;
        color: var(--text);
        line-height: 1.35;
    }

    .summary-value {
        color: var(--text);
        white-space: nowrap;
        text-align: right;
        font-weight: 800;
        flex-shrink: 0;
    }

    div[data-testid="stMetric"] {
        display: none;
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] [data-testid="stMetricLabel"],
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--text) !important;
        text-align: center !important;
        justify-content: center !important;
    }

    

    .stButton > button,
    .stDownloadButton > button {
        width: 100%;
        border-radius: 16px;
        border: 1px solid rgba(254, 255, 255, 0.08);
        min-height: 2.9rem;
        font-weight: 800;
        background: linear-gradient(180deg, rgba(41, 40, 41, 0.96), rgba(19, 20, 21, 1));
        color: var(--text);
        box-shadow: var(--shadow);
    }

    .stButton > button[kind="primary"],
    .stDownloadButton > button {
        background: linear-gradient(180deg, rgba(58, 175, 72, 1), rgba(5, 70, 45, 1));
        color: #feffff;
        border: 1px solid rgba(58, 175, 72, 0.28);
    }

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] > div,
    .stDateInput input {
        border-radius: 16px !important;
        border: 1px solid rgba(254, 255, 255, 0.08) !important;
        background: rgba(254, 255, 255, 0.04) !important;
        color: var(--text) !important;
        box-shadow: none !important;
    }

    .stTextArea textarea {
        padding-left: 0.95rem !important;
        padding-right: 0.95rem !important;
    }

    div[data-testid="stToggle"] {
        margin-top: 0.35rem;
        margin-bottom: 0.15rem;
    }

    div[data-testid="stToggle"] label {
        color: rgba(254, 255, 255, 0.86) !important;
        font-weight: 700 !important;
    }

    .done-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: rgba(254, 255, 255, 0.72);
        margin-top: 0.42rem;
        margin-bottom: 0.2rem;
    }

    .day-inner {
        padding-top: 0.15rem;
    }

    @media (max-width: 640px) {
        .block-container {
            padding-top: 5.8rem;
            padding-left: 0.85rem;
            padding-right: 0.85rem;
        }

        .hero-title {
            font-size: 1.75rem;
        }

        .planner-day {
            font-size: 2.0rem;
        }

        .day-inner {
            padding-left: 8%;
            padding-right: 8%;
            padding-top: 0.15rem;
        }

        .goal-circles-wrap {
            gap: 0.55rem;
            justify-content: space-between;
        }

        .goal-circle-item {
            min-width: 70px;
        }

        .goal-circle-label {
            font-size: 0.66rem;
            min-height: 1.55rem;
        }

        .goal-circle,
        .goal-circle-inner {
            width: 62px;
            height: 62px;
        }

        .goal-circle-inner {
            font-size: 0.78rem;
        }

        [data-baseweb="tab"] {
            min-width: 116px !important;
            min-height: 2.8rem !important;
            font-size: 0.96rem !important;
        }
    }

    textarea::placeholder,
    input::placeholder {
        color: rgba(254, 255, 255, 0.34) !important;
    }

    .stSelectbox label,
    .stTextArea label,
    .stTextInput label,
    .stNumberInput label,
    .stCaption,
    small {
        color: rgba(254, 255, 255, 0.62) !important;
    }

    button[role="tab"],
    .stSegmentedControl button {
        border-radius: 999px !important;
    }

    [data-baseweb="tab-list"] {
        background: rgba(254, 255, 255, 0.05) !important;
        border-radius: 999px !important;
        padding: 0.22rem !important;
        border: 1px solid rgba(254, 255, 255, 0.08) !important;
        gap: 0.18rem !important;
        justify-content: center !important;
    }

    [data-baseweb="tab"] {
        color: rgba(254, 255, 255, 0.8) !important;
        font-weight: 800 !important;
        min-height: 2.9rem !important;
        min-width: 128px !important;
        padding: 0.6rem 1.25rem !important;
        border-radius: 999px !important;
        background: rgba(254, 255, 255, 0.03) !important;
        border: 1px solid rgba(254, 255, 255, 0.06) !important;
        flex-grow: 0 !important;
        box-shadow: none !important;
        font-size: 1rem !important;
    }

    [aria-selected="true"][data-baseweb="tab"] {
        background: linear-gradient(180deg, rgba(58, 175, 72, 1), rgba(5, 70, 45, 1)) !important;
        color: #feffff !important;
        border: 1px solid rgba(58, 175, 72, 0.34) !important;
        box-shadow: 0 8px 20px rgba(5, 70, 45, 0.35) !important;
    }

    .stAlert {
        background: rgba(250, 77, 86, 0.12);
        border: 1px solid rgba(250, 77, 86, 0.18);
        color: var(--text);
        border-radius: 16px;
    }

    [data-testid="stExpander"] {
        background: linear-gradient(180deg, rgba(41, 40, 41, 0.96), rgba(19, 20, 21, 0.98));
        border: 1px solid var(--border);
        border-radius: 22px;
        overflow: hidden;
    }

    hr {
        border-color: rgba(254, 255, 255, 0.08);
    }

    @media (max-width: 640px) {
        .block-container {
            padding-top: 5.8rem;
            padding-left: 0.85rem;
            padding-right: 0.85rem;
        }

        .hero-title {
            font-size: 1.75rem;
        }

        .planner-day {
            font-size: 2.0rem;
        }

        .day-inner {
            padding-left: 8%;
            padding-right: 8%;
        }
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ============================================================
# Constants and helpers
# ============================================================
DATA_FILE = Path("movement_tracker_data.json")
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
TODAY_NAME = datetime.now().strftime("%A")
DEFAULT_DATE_LABELS = {
    "Monday": "Mon",
    "Tuesday": "Tue",
    "Wednesday": "Wed",
    "Thursday": "Thu",
    "Friday": "Fri",
    "Saturday": "Sat",
    "Sunday": "Sun",
}


def build_default_state():
    goals = [
        {"name": "Kickboxing Sessions", "target": 3},
        {"name": "Strength Sessions", "target": 3},
        {"name": "Yoga / Mobility", "target": 2},
        {"name": "Cardio / Run", "target": 2},
    ]

    activity_catalog = {
        "Rest": {},
        "Kickboxing": {"Kickboxing Sessions": 1},
        "Strength": {"Strength Sessions": 1},
        "Yoga": {"Yoga / Mobility": 1},
        "HIIT": {"Cardio / Run": 1},
        "Run": {"Cardio / Run": 1},
        "Skill": {"Kickboxing Sessions": 1},
    }

    week_entries = {
        day: {
            "am_activity": "Rest",
            "am_note": "",
            "am_completed": False,
            "pm_activity": "Rest",
            "pm_note": "",
            "pm_completed": False,
        }
        for day in DAYS
    }

    week_entries["Monday"] = {
        "am_activity": "Kickboxing",
        "am_note": "Bag work + footwork",
        "am_completed": True,
        "pm_activity": "Yoga",
        "pm_note": "10 min stretch before bed",
        "pm_completed": False,
    }
    week_entries["Tuesday"] = {
        "am_activity": "Strength",
        "am_note": "Lower body",
        "am_completed": False,
        "pm_activity": "Rest",
        "pm_note": "",
        "pm_completed": False,
    }
    week_entries["Wednesday"] = {
        "am_activity": "Run",
        "am_note": "Easy pace",
        "am_completed": True,
        "pm_activity": "Skill",
        "pm_note": "Shadowboxing drills",
        "pm_completed": True,
    }

    return {
        "goals": goals,
        "activity_catalog": activity_catalog,
        "week_entries": week_entries,
        "week_label": "This Week",
        "last_reset": datetime.now().strftime("%Y-%m-%d"),
    }



def load_data():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            default = build_default_state()
            default.update(saved)
            for day in DAYS:
                if day not in default["week_entries"]:
                    default["week_entries"][day] = build_default_state()["week_entries"][day]
                day_entry = default["week_entries"][day]
                day_entry.setdefault("am_activity", "Rest")
                day_entry.setdefault("am_note", "")
                day_entry.setdefault("am_completed", False)
                day_entry.setdefault("pm_activity", "Rest")
                day_entry.setdefault("pm_note", "")
                day_entry.setdefault("pm_completed", False)
            return default
        except Exception:
            return build_default_state()
    return build_default_state()
    return build_default_state()



def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)



def ensure_state():
    if "app_data" not in st.session_state:
        st.session_state.app_data = load_data()



def get_goal_lookup(goals):
    return {goal["name"]: goal["target"] for goal in goals}



def calculate_goal_progress(goals, activity_catalog, week_entries):
    progress = {goal["name"]: 0 for goal in goals}

    for day_data in week_entries.values():
        for activity_key, complete_key in [("am_activity", "am_completed"), ("pm_activity", "pm_completed")]:
            if not day_data.get(complete_key, False):
                continue
            activity = day_data.get(activity_key, "Rest")
            mapping = activity_catalog.get(activity, {})
            for goal_name, increment in mapping.items():
                if goal_name in progress:
                    progress[goal_name] += increment

    return progress



def completion_count(goals, progress):
    complete = 0
    for goal in goals:
        if progress.get(goal["name"], 0) >= goal["target"]:
            complete += 1
    return complete



def planned_and_completed_session_counts(week_entries):
    planned = 0
    completed = 0
    for day_data in week_entries.values():
        for activity_key, complete_key in [("am_activity", "am_completed"), ("pm_activity", "pm_completed")]:
            activity = day_data.get(activity_key, "Rest")
            if activity and activity != "Rest":
                planned += 1
            if day_data.get(complete_key, False) and activity and activity != "Rest":
                completed += 1
    return planned, completed



def goal_status_text(current, target):
    if current >= target:
        return "Complete"
    remaining = max(target - current, 0)
    if remaining == 1:
        return "1 to go"
    return f"{remaining} to go"



def render_hero(progress, goals, week_entries):
    planned, completed = planned_and_completed_session_counts(week_entries)

    st.markdown(
        f"""
        <div class='hero-card hero-card-v3'>
            <div class='hero-eyebrow'>Weekly Movement</div>
            <div class='hero-title'>Track Your Week</div>
            <div class='hero-subtitle'>A calm, phone-friendly planner for AM and PM movement, notes, and weekly goal progress.</div>
            <div class='hero-stats-row'>
                <div class='hero-stat'>
                    <div class='hero-stat-number'>{completed}/{planned if planned else 0}</div>
                    <div class='hero-stat-label'>sessions completed</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )



def render_goal_cards(goals, progress):
    st.markdown("<div class='section-label'>Weekly goals</div>", unsafe_allow_html=True)

    def short_goal_name(name: str) -> str:
        name = name.replace(" Sessions", "")
        name = name.replace(" / ", "/")
        name = name.replace("Cardio/Run", "Cardio")
        return name

    circles = []
    for goal in goals[:4]:
        name = goal["name"]
        target = max(goal["target"], 1)
        current = progress.get(name, 0)
        pct = max(0, min((current / target) * 100, 100))
        label = short_goal_name(name)
        text_color = "#131415" if current >= target else "#feffff"
        wave_height = max(6, min(12, int(6 + (pct / 100) * 6)))
        circles.append(
            f"""
            <div class='goal-circle-item'>
                <div class='goal-circle-label'>{label}</div>
                <div class='goal-liquid-circle'>
                    <div class='goal-liquid-fill' style='height: {pct}%; opacity: {0 if current == 0 else 1};'>
                        <div class='goal-liquid-wave' style='height: {wave_height}px;'></div>
                    </div>
                    <div class='goal-circle-inner' style='color: {text_color};'>{current}/{goal['target']}</div>
                </div>
            </div>
            """
        )

    circles_html = f"""
    <!doctype html>
    <html>
    <head>
      <meta name='viewport' content='width=device-width, initial-scale=1' />
      <style>
        html, body {{
          margin: 0;
          padding: 0;
          background: transparent;
          overflow: hidden;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}
        .goal-circles-wrap {{
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          gap: 8px;
          width: 100%;
          box-sizing: border-box;
          padding: 0 2px;
        }}
        .goal-circle-item {{
          flex: 1 1 0;
          min-width: 0;
          text-align: center;
        }}
        .goal-circle-label {{
          font-size: 11px;
          line-height: 1.1;
          font-weight: 700;
          color: #feffff;
          min-height: 28px;
          margin-bottom: 6px;
          display: flex;
          align-items: flex-end;
          justify-content: center;
          text-align: center;
          word-break: break-word;
        }}
        .goal-liquid-circle {{
          width: 62px;
          height: 62px;
          border-radius: 50%;
          position: relative;
          overflow: hidden;
          margin: 0 auto;
          background: rgba(0,0,0,0.22);
          box-shadow: 0 8px 18px rgba(0,0,0,0.28);
          border: 1px solid rgba(254,255,255,0.08);
        }}
        .goal-liquid-fill {{
          position: absolute;
          left: 0;
          right: 0;
          bottom: 0;
          background: #3aaf48;
        }}
        .goal-liquid-wave {{
          position: absolute;
          top: calc(-1 * var(--wave-h, 8px));
          left: -8%;
          width: 116%;
          background: #3aaf48;
          border-radius: 50% 50% 0 0;
          height: 8px;
        }}
        .goal-circle-inner {{
          position: absolute;
          inset: 0;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 13px;
          font-weight: 800;
          z-index: 2;
        }}
      </style>
    </head>
    <body>
      <div class='goal-circles-wrap'>
        {''.join(circles)}
      </div>
    </body>
    </html>
    """
    circles_html = circles_html.replace('var(--wave-h, 8px)', '8px')
    components.html(circles_html, height=104, scrolling=False)



def render_activity_chip_group(day, period_label, key_name, current_value, activity_options):
    st.markdown(f"<div class='mini-chip'>{period_label}</div>", unsafe_allow_html=True)

    selected = st.segmented_control(
        f"{period_label} activity · {day}",
        options=activity_options,
        default=current_value if current_value in activity_options else activity_options[0],
        selection_mode="single",
        key=key_name,
        label_visibility="collapsed",
    )
    return selected



def render_completion_toggle(day, label, key_name, current_value):
    if key_name not in st.session_state:
        st.session_state[key_name] = False if current_value is None else bool(current_value)

    st.markdown(f"<div class='done-label'>Mark {label.lower()} as done</div>", unsafe_allow_html=True)
    value = st.toggle(
        f"Done · {label} · {day}",
        value=st.session_state[key_name],
        key=key_name,
        label_visibility="collapsed",
    )
    status = "Completed" if value else "Planned"
    cls = "completion-pill complete" if value else "completion-pill"
    st.markdown(f"<div class='{cls}'>{status}</div>", unsafe_allow_html=True)
    return value



def render_day_card(day, day_data, activity_options, today_only=False):
    badge = ""
    if day == TODAY_NAME:
        badge = "<span class='today-badge'>● Today</span>"

    st.markdown(
        f"""
        <div class='planner-card'>
            <div class='planner-header'>
                <div class='planner-day'>{day}</div>
                <div>{badge}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='margin-top:0rem'></div>", unsafe_allow_html=True)

    with st.container(border=False):
        st.markdown("<div class='day-inner'>", unsafe_allow_html=True)

        day_data["am_activity"] = render_activity_chip_group(
            day,
            "Morning",
            f"{day}_am_activity",
            day_data.get("am_activity", activity_options[0]),
            activity_options,
        )
        day_data["am_completed"] = render_completion_toggle(
            day,
            "Morning",
            f"{day}_am_completed",
            day_data.get("am_completed", False),
        )
        am_notes_label = "Hide note" if day_data.get("am_note", "").strip() else "Add note"
        with st.expander(am_notes_label, expanded=today_only and bool(day_data.get("am_note", "").strip())):
            day_data["am_note"] = st.text_area(
                f"AM note · {day}",
                value=day_data.get("am_note", ""),
                placeholder="Add a quick note...",
                key=f"{day}_am_note",
                height=88 if today_only else 78,
                label_visibility="collapsed",
            )

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        day_data["pm_activity"] = render_activity_chip_group(
            day,
            "Evening",
            f"{day}_pm_activity",
            day_data.get("pm_activity", activity_options[0]),
            activity_options,
        )
        day_data["pm_completed"] = render_completion_toggle(
            day,
            "Evening",
            f"{day}_pm_completed",
            day_data.get("pm_completed", False),
        )
        pm_notes_label = "Hide note" if day_data.get("pm_note", "").strip() else "Add note"
        with st.expander(pm_notes_label, expanded=today_only and bool(day_data.get("pm_note", "").strip())):
            day_data["pm_note"] = st.text_area(
                f"PM note · {day}",
                value=day_data.get("pm_note", ""),
                placeholder="How did it feel?",
                key=f"{day}_pm_note",
                height=88 if today_only else 78,
                label_visibility="collapsed",
            )
        st.markdown("</div>", unsafe_allow_html=True)


def render_today_view(data):
    st.markdown("<div class='section-label'>Today</div>", unsafe_allow_html=True)
    day = TODAY_NAME if TODAY_NAME in DAYS else "Monday"
    render_day_card(
        day,
        data["week_entries"][day],
        list(data["activity_catalog"].keys()),
        today_only=True,
    )



def render_week_view(data):
    st.markdown("<div class='section-label'>Week planner</div>", unsafe_allow_html=True)
    for day in DAYS:
        render_day_card(day, data["week_entries"][day], list(data["activity_catalog"].keys()))



def render_summary(goals, progress):
    st.markdown("<div class='section-label'>Weekly summary</div>", unsafe_allow_html=True)
    rows = []
    for goal in goals:
        current = progress.get(goal["name"], 0)
        rows.append(
            f"<div class='summary-line'><span class='summary-name'>{goal['name']}</span><strong class='summary-value'>{current} / {goal['target']}</strong></div>"
        )

    st.markdown(
        f"<div class='summary-card'>{''.join(rows)}</div>",
        unsafe_allow_html=True,
    )



def render_settings(data):
    with st.expander("Edit goals and activity settings", expanded=False):
        st.caption(
    "Tip: this version stores data locally in a JSON file. Later, you can swap that layer for SQLite, Supabase, Firebase, or another database without changing the overall app structure much. In this version, activities are planned first and only count toward goals after they are explicitly marked complete."
)

        st.subheader("Weekly goals")
        for idx, goal in enumerate(data["goals"]):
            col1, col2 = st.columns([2.4, 1])
            with col1:
                goal["name"] = st.text_input(
                    f"Goal name {idx + 1}",
                    value=goal["name"],
                    key=f"goal_name_{idx}",
                )
            with col2:
                goal["target"] = st.number_input(
                    f"Target {idx + 1}",
                    min_value=0,
                    step=1,
                    value=int(goal["target"]),
                    key=f"goal_target_{idx}",
                )

        st.divider()
        st.subheader("Activity catalog")
        st.caption("Each activity can count toward one or more weekly goals.")

        current_goal_names = [goal["name"] for goal in data["goals"] if goal["name"].strip()]
        new_catalog = {}

        activity_names = list(data["activity_catalog"].keys())
        for idx, activity in enumerate(activity_names):
            st.markdown(f"**Activity {idx + 1}**")
            new_name = st.text_input(
                f"Activity name {idx + 1}",
                value=activity,
                key=f"activity_name_{idx}",
            )

            mapping = data["activity_catalog"].get(activity, {})
            updated_mapping = {}
            cols = st.columns(len(current_goal_names)) if current_goal_names else []

            for g_idx, goal_name in enumerate(current_goal_names):
                with cols[g_idx]:
                    updated_mapping[goal_name] = st.number_input(
                        f"{new_name or activity} → {goal_name}",
                        min_value=0,
                        step=1,
                        value=int(mapping.get(goal_name, 0)),
                        key=f"map_{idx}_{g_idx}",
                    )

            cleaned_mapping = {k: v for k, v in updated_mapping.items() if v > 0}
            if new_name.strip():
                new_catalog[new_name.strip()] = cleaned_mapping
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
        if st.button("Add new activity"):
            new_catalog[f"New Activity {len(new_catalog) + 1}"] = {}
            data["activity_catalog"] = new_catalog
            save_data(data)
            st.rerun()

        if new_catalog:
            data["activity_catalog"] = new_catalog

        st.divider()
        st.subheader("Save and reset")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Save changes", type="primary"):
                save_data(data)
                st.success("Saved locally to JSON.")
        with c2:
            if st.button("Reset week"):
                defaults = build_default_state()
                data["week_entries"] = defaults["week_entries"]
                data["last_reset"] = datetime.now().strftime("%Y-%m-%d")
                save_data(data)
                st.success("Started a fresh week.")
                st.rerun()



def render_sidebar(data):
    with st.sidebar:
        st.header("Local data")
        st.caption("Save to a local JSON file so the current week persists on this machine.")

        if st.button("Save now", type="primary"):
            save_data(data)
            st.success("Saved.")

        if DATA_FILE.exists():
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                st.download_button(
                    "Download JSON backup",
                    data=f.read(),
                    file_name="movement_tracker_data.json",
                    mime="application/json",
                )

        uploaded = st.file_uploader("Load JSON backup", type=["json"])
        if uploaded is not None:
            try:
                loaded = json.load(uploaded)
                st.session_state.app_data = loaded
                save_data(loaded)
                st.success("Backup loaded.")
                st.rerun()
            except Exception:
                st.error("That file could not be loaded.")


# ============================================================
# Main app
# ============================================================
ensure_state()
data = st.session_state.app_data
render_sidebar(data)

# Keep activity options available everywhere.
activity_options = list(data["activity_catalog"].keys())
if not activity_options:
    data["activity_catalog"] = {"Rest": {}}
    activity_options = ["Rest"]

# Make sure current entries always use a valid option.
for day in DAYS:
    for key in ["am_activity", "pm_activity"]:
        if data["week_entries"][day].get(key) not in activity_options:
            data["week_entries"][day][key] = activity_options[0]

progress = calculate_goal_progress(data["goals"], data["activity_catalog"], data["week_entries"])
render_hero(progress, data["goals"], data["week_entries"])

# View switcher optimized for phones.
st.markdown("<div class='view-wrap'>", unsafe_allow_html=True)
_view_left, _view_center, _view_right = st.columns([1, 3, 1])
with _view_center:
    view = st.segmented_control(
        "View",
        options=["Today", "Week"],
        default="Today",
        selection_mode="single",
    )
st.markdown("</div>", unsafe_allow_html=True)

render_goal_cards(data["goals"], progress)

if view == "Today":
    render_today_view(data)
else:
    render_week_view(data)

# Recalculate after edits so progress changes instantly.
progress = calculate_goal_progress(data["goals"], data["activity_catalog"], data["week_entries"])
render_summary(data["goals"], progress)
render_settings(data)

# Persist automatically after UI interactions.
save_data(data)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
st.caption(
    "Tip: this version stores data locally in a JSON file. Later, you can swap that layer for SQLite, Supabase, Firebase, or another database without changing the overall app structure much. Streamlit does not provide fully custom native chip controls, so this version uses segmented controls as the cleanest stable alternative to dropdowns for faster one-tap activity selection."
)
