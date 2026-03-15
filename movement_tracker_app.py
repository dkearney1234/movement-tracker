import json
from pathlib import Path
from datetime import datetime

import streamlit as st

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
        color: var(--text);
    }

    .hero-subtitle {
        font-size: 0.99rem;
        line-height: 1.55;
        color: rgba(254, 255, 255, 0.84);
        max-width: 34rem;
        margin: 0 auto;
    }

    .metric-wrap {
        margin-bottom: 0.4rem;
    }

    .section-label {
        font-size: 0.78rem;
        color: rgba(254, 255, 255, 0.58);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 800;
        margin: 1.1rem 0 0.7rem 0;
    }

    .goal-card {
        background: linear-gradient(180deg, rgba(41, 40, 41, 0.98), rgba(19, 20, 21, 1));
        border: 1px solid var(--border);
        border-radius: var(--radius-xl);
        padding: 1rem;
        box-shadow: var(--shadow);
        margin-bottom: 0.85rem;
    }

    .goal-card.complete {
        background:
            radial-gradient(circle at top center, rgba(58, 175, 72, 0.16), transparent 48%),
            linear-gradient(180deg, rgba(5, 70, 45, 0.94), rgba(19, 20, 21, 1));
        border: 1px solid rgba(58, 175, 72, 0.24);
        box-shadow: var(--glow);
    }

    .goal-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
        margin-bottom: 0.6rem;
    }

    .goal-name {
        font-size: 1.04rem;
        font-weight: 700;
        color: var(--text);
    }

    .goal-pill {
        display: inline-flex;
        align-items: center;
        padding: 0.32rem 0.68rem;
        border-radius: 999px;
        font-size: 0.74rem;
        font-weight: 800;
        background: rgba(254, 255, 255, 0.06);
        color: rgba(254, 255, 255, 0.76);
        border: 1px solid rgba(254, 255, 255, 0.06);
    }

    .goal-pill.complete {
        background: rgba(58, 175, 72, 0.16);
        color: #8ef6a0;
        border: 1px solid rgba(58, 175, 72, 0.18);
    }

    .goal-metrics {
        display: flex;
        align-items: baseline;
        gap: 0.4rem;
        margin-bottom: 0.45rem;
    }

    .goal-number {
        font-size: 1.7rem;
        font-weight: 800;
        line-height: 1;
        color: var(--text);
    }

    .goal-target {
        color: rgba(254, 255, 255, 0.62);
        font-size: 0.92rem;
    }

    .goal-caption {
        color: rgba(254, 255, 255, 0.7);
        font-size: 0.86rem;
        margin-top: 0.45rem;
    }

    .planner-card {
        background: linear-gradient(180deg, rgba(41, 40, 41, 1), rgba(19, 20, 21, 1));
        border: 1px solid rgba(254, 255, 255, 0.1);
        border-radius: 26px;
        padding: 1.25rem 1.2rem;
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.4);
        margin-bottom: 1rem;
    }

    .planner-header {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1rem;
        position: relative;
        min-height: 1.8rem;
    }

    .planner-day {
        font-size: 2.64rem;
        font-weight: 800;
        color: var(--text);
        text-align: center;
        width: 100%;
        line-height: 1.02;
        letter-spacing: -0.02em;
    }

    .planner-header .today-badge {
        position: absolute;
        right: 0;
        top: 50%;
        transform: translateY(-50%);
    }

    .planner-date {
        color: rgba(254, 255, 255, 0.62);
        font-size: 0.88rem;
    }

    .day-inner {
        padding-left: 20%;
        padding-right: 20%;
    }

    .mini-chip {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: rgba(254, 255, 255, 0.56);
        margin-bottom: 0.5rem;
    }

    .summary-card {
        background: linear-gradient(180deg, rgba(41, 40, 41, 0.96), rgba(19, 20, 21, 0.98));
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 1rem;
        box-shadow: var(--shadow);
        margin-top: 0.8rem;
    }

    .summary-line {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.55rem 0;
        border-bottom: 1px solid rgba(254, 255, 255, 0.06);
        font-size: 0.95rem;
        color: var(--text);
    }

    .summary-line:last-child {
        border-bottom: none;
    }

    .today-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.34rem 0.62rem;
        border-radius: 999px;
        background: rgba(58, 175, 72, 0.14);
        color: #8ef6a0;
        border: 1px solid rgba(58, 175, 72, 0.18);
        font-size: 0.75rem;
        font-weight: 800;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(180deg, rgba(41, 40, 41, 0.98), rgba(19, 20, 21, 1));
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 0.95rem;
        box-shadow: var(--shadow);
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] [data-testid="stMetricLabel"],
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--text) !important;
    }

    div[data-testid="stProgressBar"] {
        margin-top: -0.15rem;
        margin-bottom: 1.05rem;
    }

    div[data-testid="stProgressBar"] > div {
        background: rgba(254, 255, 255, 0.08) !important;
        border-radius: 999px;
    }

    div[data-testid="stProgressBar"] > div > div {
        border-radius: 999px;
        height: 10px;
        background: linear-gradient(90deg, #3aaf48, #74df82) !important;
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
        border-radius: 24px !important;
        padding: 0.28rem !important;
        border: 1px solid rgba(254, 255, 255, 0.06) !important;
        gap: 0.35rem !important;
        flex-wrap: wrap !important;
    }

    [data-baseweb="tab"] {
        color: rgba(254, 255, 255, 0.76) !important;
        font-weight: 800 !important;
        min-height: 2.55rem !important;
        padding: 0.55rem 0.9rem !important;
        border-radius: 999px !important;
        background: rgba(254, 255, 255, 0.04) !important;
        border: 1px solid rgba(254, 255, 255, 0.06) !important;
        flex-grow: 0 !important;
        box-shadow: none !important;
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
            font-size: 2.1rem;
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
            "pm_activity": "Rest",
            "pm_note": "",
        }
        for day in DAYS
    }

    # Sample data to make the app feel alive immediately.
    week_entries["Monday"] = {
        "am_activity": "Kickboxing",
        "am_note": "Bag work + footwork",
        "pm_activity": "Yoga",
        "pm_note": "10 min stretch before bed",
    }
    week_entries["Tuesday"] = {
        "am_activity": "Strength",
        "am_note": "Lower body",
        "pm_activity": "Rest",
        "pm_note": "",
    }
    week_entries["Wednesday"] = {
        "am_activity": "Run",
        "am_note": "Easy pace",
        "pm_activity": "Skill",
        "pm_note": "Shadowboxing drills",
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
            # Merge lightly with defaults to protect against missing keys.
            default = build_default_state()
            default.update(saved)
            for day in DAYS:
                if day not in default["week_entries"]:
                    default["week_entries"][day] = build_default_state()["week_entries"][day]
            return default
        except Exception:
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
        for time_of_day in ["am_activity", "pm_activity"]:
            activity = day_data.get(time_of_day, "Rest")
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



def goal_status_text(current, target):
    if current >= target:
        return "Complete"
    remaining = max(target - current, 0)
    if remaining == 1:
        return "1 to go"
    return f"{remaining} to go"



def render_hero(progress, goals):
    complete = completion_count(goals, progress)
    total = len(goals)
    st.markdown(
        f"""
        <div class='hero-card hero-card-v3'>
            <div class='hero-eyebrow'>Weekly Movement</div>
            <div class='hero-title'>Track Your Week.</div>
            <div class='hero-subtitle'>A calm, phone-friendly planner for AM and PM movement, notes, and weekly goal progress.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='metric-wrap'>", unsafe_allow_html=True)
    st.metric("Goals completed", f"{complete}/{total}")
    st.markdown("</div>", unsafe_allow_html=True)


def render_goal_cards(goals, progress):
    st.markdown("<div class='section-label'>Weekly goals</div>", unsafe_allow_html=True)

    for goal in goals:
        name = goal["name"]
        target = goal["target"]
        current = progress.get(name, 0)
        pct = min(current / target, 1.0) if target else 0
        is_complete = current >= target

        st.markdown(
            f"""
            <div class='goal-card {'complete' if is_complete else ''}'>
                <div class='goal-top'>
                    <div class='goal-name'>{name}</div>
                    <div class='goal-pill {'complete' if is_complete else ''}'>{'Done' if is_complete else 'In progress'}</div>
                </div>
                <div class='goal-metrics'>
                    <div class='goal-number'>{current}</div>
                    <div class='goal-target'>/ {target}</div>
                </div>
                <div class='goal-caption'>{goal_status_text(current, target)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(pct)



def render_activity_chip_group(day, period_label, key_name, current_value, activity_options):
    st.markdown(f"<div class='mini-chip'>{period_label}</div>", unsafe_allow_html=True)

    # Streamlit does not offer fully custom CSS-targetable pill chips with arbitrary styling
    # and state behavior the way a native app would. segmented_control is the cleanest,
    # most stable built-in alternative for fast one-tap selection.
    selected = st.segmented_control(
        f"{period_label} activity · {day}",
        options=activity_options,
        default=current_value if current_value in activity_options else activity_options[0],
        selection_mode="single",
        key=key_name,
        label_visibility="collapsed",
    )
    return selected



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

    st.markdown("<div style='margin-top:-5.0rem'></div>", unsafe_allow_html=True)

    with st.container(border=False):
        st.markdown("<div class='day-inner'>", unsafe_allow_html=True)

        day_data["am_activity"] = render_activity_chip_group(
            day,
            "Morning",
            f"{day}_am_activity",
            day_data.get("am_activity", activity_options[0]),
            activity_options,
        )
        day_data["am_note"] = st.text_area(
            f"AM note · {day}",
            value=day_data.get("am_note", ""),
            placeholder="Add a quick note...",
            key=f"{day}_am_note",
            height=88 if today_only else 78,
            label_visibility="collapsed",
        )

        st.markdown("<div style='height:0.65rem'></div>", unsafe_allow_html=True)

        day_data["pm_activity"] = render_activity_chip_group(
            day,
            "Evening",
            f"{day}_pm_activity",
            day_data.get("pm_activity", activity_options[0]),
            activity_options,
        )
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
            f"<div class='summary-line'><span>{goal['name']}</span><strong>{current} / {goal['target']}</strong></div>"
        )

    st.markdown(
        f"<div class='summary-card'>{''.join(rows)}</div>",
        unsafe_allow_html=True,
    )



def render_settings(data):
    with st.expander("Edit goals and activity settings", expanded=False):
        st.caption("Update weekly goals, activity names, and how each activity counts toward each goal.")

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
render_hero(progress, data["goals"])

# View switcher optimized for phones.
view = st.segmented_control(
    "View",
    options=["Today", "Week"],
    default="Today",
    selection_mode="single",
)

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
