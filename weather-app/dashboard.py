
import streamlit as st
import base64
st.set_page_config(
    page_title="Weather Data Analysis System",
    page_icon="🌤️",
    layout="wide"
)
st.markdown("""
<style>
/* Main background */
.stApp {
    background-color: #f5f7fb;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0f2747;
}

[data-testid="stSidebar"] * {
    color: white !important;
}
/* Sidebar filter controls */
[data-testid="stSidebar"] input {
    border-radius: 8px !important;
}

/* Multiselect containers */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    border-radius: 8px !important;
    border: 1px solid #3d5f86 !important;
}

/* Selected filter tags */
[data-testid="stSidebar"] [data-baseweb="tag"] {
    border-radius: 6px !important;
}

/* Sidebar filter labels */
[data-testid="stSidebar"] label {
    font-weight: 600 !important;
}

.main-title {
    font-size: 36px;
    font-weight: 700;
    color: #12355b;
    margin-bottom: 2px;
}

.subtitle {
    color: #667085;
    font-size: 15px;
    margin-bottom: 12px;
}

/* Section headings */
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    color: #12355b !important;
    font-weight: 700;
}

/* Metric cards */
/* Base metric card */
[data-testid="stMetric"] {
    padding: 20px 14px;
    border-radius: 14px;
    min-height: 125px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
    border: 1px solid #e6eaf0;
}

/* Card 1 */
[data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(1) [data-testid="stMetric"] {
    background: #e8f3ff;
    border-left: 5px solid #1976d2;
}

/* Card 2 */
[data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) [data-testid="stMetric"] {
    background: #fff0e6;
    border-left: 5px solid #f57c00;
}

/* Card 3 */
[data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(3) [data-testid="stMetric"] {
    background: #e8f8f5;
    border-left: 5px solid #00897b;
}

/* Card 4 */
[data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(4) [data-testid="stMetric"] {
    background: #f3eaff;
    border-left: 5px solid #8e44ad;
}

/* Metric card colours (newer Streamlit uses stColumn) */
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(1) [data-testid="stMetric"] {
    background: #e8f3ff; border-left: 5px solid #1976d2;
}
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"] {
    background: #fff0e6; border-left: 5px solid #f57c00;
}
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"] {
    background: #e8f8f5; border-left: 5px solid #00897b;
}
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(4) [data-testid="stMetric"] {
    background: #f3eaff; border-left: 5px solid #8e44ad;
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    color: #475467 !important;
    font-size: 14px;
    font-weight: 600;
}

/* Metric values */
[data-testid="stMetricValue"] {
    color: #12355b !important;
    font-size: 30px;
    font-weight: 700;
}
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* Buttons */
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
}

/* Download button */
.stDownloadButton > button {
    border-radius: 8px;
    font-weight: 600;
}

/* Horizontal divider */
hr {
    border-color: #d9dee7;
}
header[data-testid="stHeader"] {
    background-color: #12355b;
}

.main .block-container {
    padding-top: 2rem;
}

/* ---- Consistent colours in BOTH light and dark mode ---- */
[data-testid="stMain"] p, [data-testid="stMain"] li, [data-testid="stMain"] label,
[data-testid="stMain"] h1, [data-testid="stMain"] h2, [data-testid="stMain"] h3,
[data-testid="stMain"] h4, [data-testid="stMain"] [data-testid="stMarkdownContainer"] {
    color: #12355b;
}
[data-testid="stMain"] [data-testid="stCaptionContainer"] {
    color: #667085 !important;
}
button[data-baseweb="tab"] {
    color: #12355b !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #1672e8 !important;
}
[data-testid="stMain"] input, [data-testid="stMain"] textarea {
    background-color: #ffffff !important;
    color: #12355b !important;
}
[data-testid="stMain"] [data-baseweb="input"],
[data-testid="stMain"] [data-baseweb="input"] button {
    background-color: #ffffff !important;
    color: #12355b !important;
}
[data-testid="stMain"] [data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #12355b !important;
}
[data-testid="stMain"] [data-baseweb="select"] * {
    color: #12355b !important;
}
/* Sidebar inputs: dark-blue fields with white text */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] [data-baseweb="input"],
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #1b3a63 !important;
    color: #ffffff !important;
}
/* Top bar icons visible on navy header */
header[data-testid="stHeader"] button, header[data-testid="stHeader"] a,
header[data-testid="stHeader"] span, header[data-testid="stHeader"] svg {
    color: #ffffff !important;
    fill: #ffffff !important;
}
</style>

 """, unsafe_allow_html=True)

# ---------------- Login / Create Account / Forgot Password ----------------
import os
import auth
import mailer

auth.init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if not st.session_state.logged_in:
    st.markdown("""
    <style>
    .login-title {
        text-align: center;
        color: #12355b;
        font-size: 30px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .login-subtitle {
        text-align: center;
        color: #667085;
        font-size: 14px;
        margin-bottom: 20px;
    }
    /* Login card */
.st-key-login_card {
    background: #ffffff !important;
    border: 1px solid #dbe5f0 !important;
    border-radius: 20px !important;
    padding: 30px !important;
    max-width: 500px;
    margin: 20px auto !important;
    box-shadow: 0 10px 35px rgba(18, 53, 91, 0.15);
}
/* Login labels */
.stTextInput label {
    color: #12355b !important;
    font-weight: 600 !important;
}

/* Input boxes */
.stTextInput input {
    background-color: #ffffff !important;
    color: #12355b !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
}

/* Login button */
.stButton button *, .st-key-login_card .stButton button * {
    color: #ffffff !important;
}
.stButton button {
    background-color: #1672e8 !important;
    color: white !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    min-height: 45px;
}
    /* Improve input placeholder visibility */
    .stTextInput input::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Login background image: put image.png (or .jpg/.jpeg/.webp) in the same folder as dashboard.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for fname, mime in [("image.png", "png"), ("image.jpg", "jpeg"),
                        ("image.jpeg", "jpeg"), ("image.webp", "webp")]:
        img_path = os.path.join(base_dir, fname)
        if os.path.exists(img_path):
            with open(img_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/{mime};base64,{img_data}") !important;
                background-size: cover !important;
                background-position: center !important;
                background-repeat: no-repeat !important;
                background-attachment: fixed !important;
            }}
            </style>
            """, unsafe_allow_html=True)
            break

    left, center, right = st.columns([1, 2, 1])

    with center:
        with st.container(border=True, key="login_card"):
            st.markdown(
                '<div style="text-align:center; font-size:55px;">🌤️</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="login-title">Weather Data Analysis System</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="login-subtitle">Login to access the weather dashboard</div>',
                unsafe_allow_html=True
            )

            tab_login, tab_signup, tab_forgot = st.tabs(
                ["🔐 Login", "📝 Create Account", "🔑 Forgot Password"]
            )

            # ---- Login ----
            with tab_login:
                username = st.text_input(
                    "Username", placeholder="Enter your username", key="login_username"
                )
                password = st.text_input(
                    "Password", placeholder="Enter your password",
                    type="password", key="login_password"
                )
                if st.button("🔐 Login", width="stretch", key="btn_login"):
                    if auth.verify(username, password):
                        st.session_state.logged_in = True
                        st.session_state.current_user = username.strip().lower()
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                st.caption("🔒 Authorized access only")

            # ---- Create Account (email OTP verification) ----
            with tab_signup:
                su_user = st.text_input("Username", placeholder="Choose a username", key="su_user")
                su_email = st.text_input("Email", placeholder="you@example.com", key="su_email")
                su_pass = st.text_input("Password", type="password",
                                        placeholder="Minimum 6 characters", key="su_pass")
                su_pass2 = st.text_input("Confirm Password", type="password",
                                         placeholder="Re-enter password", key="su_pass2")

                if st.button("📧 Send OTP", width="stretch", key="btn_signup_otp"):
                    ok, msg = auth.validate_signup(su_user, su_email, su_pass, su_pass2)
                    if not ok:
                        st.session_state.su_sent = False
                        st.error(msg)
                    elif not mailer.is_configured() and not mailer.demo_allowed():
                        st.session_state.su_sent = False
                        st.error("Email service is not configured. Please contact the admin.")
                    else:
                        otp = auth.issue_otp(su_email, "signup")
                        sent, info = mailer.send_otp(su_email.strip(), otp, "signup")
                        if sent:
                            st.session_state.su_sent = True
                            st.session_state.su_demo_otp = None
                        elif mailer.is_configured():
                            st.session_state.su_sent = False
                            st.error(info)
                        else:                       # local demo mode only
                            st.session_state.su_sent = True
                            st.session_state.su_demo_otp = otp

                if st.session_state.get("su_sent"):
                    if st.session_state.get("su_demo_otp"):
                        st.warning(f"Demo mode (SMTP not configured). Your OTP is: "
                                   f"**{st.session_state.su_demo_otp}**")
                    else:
                        st.info("OTP sent to your email. It is valid for 5 minutes.")
                    su_otp = st.text_input("Enter OTP", max_chars=6, key="su_otp")
                    if st.button("✅ Verify & Create Account", width="stretch",
                                 key="btn_signup"):
                        ok, msg = auth.check_otp(su_email, "signup", su_otp)
                        if ok and not auth.username_exists(su_user):
                            auth.register(su_user, su_email, su_pass)
                            st.session_state.su_sent = False
                            st.success("Account created successfully. Go to the Login tab.")
                        elif ok:
                            st.error("Username already taken.")
                        else:
                            st.error(msg)

            # ---- Forgot Password (email OTP) ----
            with tab_forgot:
                fp_email = st.text_input("Registered Email", placeholder="you@example.com",
                                         key="fp_email")
                if st.button("📧 Send OTP", width="stretch", key="btn_reset_otp"):
                    if not fp_email.strip():
                        st.error("Enter your registered email.")
                    elif not mailer.is_configured() and not mailer.demo_allowed():
                        st.session_state.fp_sent = False
                        st.error("Email service is not configured. Please contact the admin.")
                    else:
                        st.session_state.fp_sent = True
                        st.session_state.fp_demo_otp = None
                        if auth.email_exists(fp_email):
                            otp = auth.issue_otp(fp_email, "reset")
                            sent, info = mailer.send_otp(fp_email.strip(), otp, "reset")
                            if not sent and mailer.is_configured():
                                st.session_state.fp_sent = False
                                st.error(info)
                            elif not sent:
                                st.session_state.fp_demo_otp = otp

                if st.session_state.get("fp_sent"):
                    if st.session_state.get("fp_demo_otp"):
                        st.warning(f"Demo mode (SMTP not configured). Your OTP is: "
                                   f"**{st.session_state.fp_demo_otp}**")
                    else:
                        st.info("If this email is registered, an OTP has been sent "
                                "(valid for 5 minutes).")
                    fp_otp = st.text_input("Enter OTP", max_chars=6, key="fp_otp")
                    fp_new = st.text_input("New Password", type="password",
                                           placeholder="Minimum 6 characters", key="fp_new")
                    fp_new2 = st.text_input("Confirm New Password", type="password",
                                            key="fp_new2")
                    if st.button("🔑 Reset Password", width="stretch", key="btn_reset"):
                        ok, msg = auth.reset_password(fp_email, fp_otp, fp_new, fp_new2)
                        if ok:
                            st.session_state.fp_sent = False
                        (st.success if ok else st.error)(msg)
    st.stop()
st.sidebar.markdown(
    """
    <div style="text-align:center; padding:10px 0 20px 0;">
        <div style="font-size:42px;">🌤️</div>
        <div style="font-size:24px; font-weight:700;">
            Weather Analysis
        </div>
        <div style="font-size:13px; opacity:0.75; margin-top:5px;">
            Data Analysis System
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.caption(f"👤 Logged in as **{st.session_state.current_user}**")
st.sidebar.markdown("---")
def go_to(target):
    st.session_state.page_nav = target


page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Data View",
        "Analysis",
        "Visualizations",
        "Monthly Analysis",
        "Data Cleaning",
        "Download Data"
    ],
    key="page_nav"
)

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.rerun()
st.markdown("""
<div style="
    background: linear-gradient(90deg, #12355b, #1d5c91);
    padding: 22px 28px;
    border-radius: 14px;
    margin-bottom: 25px;
    color: white;
">
    <div style="font-size: 27px; font-weight: 700;">
        🌤️ Weather Data Analysis System
    </div>
    <div style="font-size: 14px; margin-top: 6px; color: #dceafa;">
        Interactive Weather Data Analysis and Visualization Dashboard
    </div>
</div>
""", unsafe_allow_html=True)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/weather.csv")

st.sidebar.subheader("Filters")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df["Date"].min(), df["Date"].max())
)
if len(date_range) == 2:
    start_date, end_date = date_range

    df = df[
        (pd.to_datetime(df["Date"]).dt.date >= start_date)
        & (pd.to_datetime(df["Date"]).dt.date <= end_date)
    ]

weather_filter = st.sidebar.multiselect(
    "Select Weather Condition",
    options=sorted(df["Weather"].unique()),
    default=sorted(df["Weather"].unique())
)

df = df[df["Weather"].isin(weather_filter)]
location_filter = st.sidebar.multiselect(
    "Select Location",
    options=sorted(df["Location"].unique()),
    default=sorted(df["Location"].unique())
)

df = df[df["Location"].isin(location_filter)]

# ---------------- PAGE CONTENT ----------------

if df.empty:
    st.warning("No weather records found for the selected filters.")

elif page == "Dashboard":
    st.markdown("""
    <h1 style="color:#102b55; margin-bottom:0;">Dashboard Overview</h1>
    <p style="color:#718096;">Overview of key weather metrics and trends</p>
    """, unsafe_allow_html=True)

    # ---- Quick access module tiles (click = open that module) ----
    modules = [
        ("Data View", "📋", "Browse and search all weather records", "#1976d2", "#e8f3ff"),
        ("Analysis", "🔬", "Statistics, correlation and location insights", "#f57c00", "#fff0e6"),
        ("Visualizations", "📈", "Interactive weather charts and trends", "#00897b", "#e8f8f5"),
        ("Monthly Analysis", "📅", "Month-wise temperature, humidity and rain", "#8e44ad", "#f3eaff"),
        ("Data Cleaning", "🧹", "Check missing values and duplicates", "#e53935", "#fee2e2"),
        ("Download Data", "⬇️", "Export filtered weather data as CSV", "#239447", "#dcfce7"),
    ]

    tile_css = ""
    for idx, (_, _, _, color, bg) in enumerate(modules):
        tile_css += f"""
        .st-key-tile_{idx} {{
            background: {bg};
            border-left: 6px solid {color};
            border-radius: 14px;
            padding: 14px 18px 8px 18px;
            box-shadow: 0 3px 12px rgba(0,0,0,0.08);
        }}
        .st-key-tile_{idx} button {{
            background: {color} !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }}
        .st-key-tile_{idx} button * {{
            color: #ffffff !important;
        }}
        """
    st.markdown(f"<style>{tile_css}</style>", unsafe_allow_html=True)

    st.markdown("### 🚀 Quick Access")
    for row_start in (0, 3):
        cols = st.columns(3)
        for col, idx in zip(cols, range(row_start, row_start + 3)):
            name, icon, desc, _, _ = modules[idx]
            with col:
                with st.container(key=f"tile_{idx}"):
                    st.markdown(
                        f"<div style='font-size:34px;'>{icon}</div>"
                        f"<div style='font-size:19px; font-weight:700; color:#12355b;'>{name}</div>"
                        f"<div style='font-size:13px; color:#667085; margin-bottom:8px;'>{desc}</div>",
                        unsafe_allow_html=True,
                    )
                    st.button(f"Open {name} →", key=f"go_{idx}", width="stretch",
                              on_click=go_to, args=(name,))
    st.markdown("---")

        # Attractive Weather Summary Cards
        # Attractive Weather Summary Cards
    st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
        min-height: 125px;
    }

    div[data-testid="stMetric"]:nth-child(1) {
        background: #fee2e2;
        border-left: 5px solid #ef4444;
    }

    div[data-testid="stMetric"]:nth-child(2) {
        background: #dbeafe;
        border-left: 5px solid #3b82f6;
    }

    div[data-testid="stMetric"]:nth-child(3) {
        background: #dcfce7;
        border-left: 5px solid #22c55e;
    }

    div[data-testid="stMetric"]:nth-child(4) {
        background: #f3e8ff;
        border-left: 5px solid #a855f7;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🌡️ Average Temperature",
            f"{df['Temperature'].mean():.1f} °C"
        )

    with col2:
        st.metric(
            "💧 Average Humidity",
            f"{df['Humidity'].mean():.1f} %"
        )

    with col3:
        st.metric(
            "🌧️ Total Precipitation",
            f"{df['Precipitation'].sum():.1f} mm"
        )

    with col4:
        st.metric(
            "💨 Average Wind Speed",
            f"{df['WindSpeed'].mean():.1f} km/h"
        )
    st.markdown("<br>", unsafe_allow_html=True)

    # Main trend charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("###  Temperature Trend")
        st.line_chart(
            df.set_index("Date")["Temperature"],
            color="#e53935",
            width="stretch"
        )

    with col2:
        st.markdown("### 💧 Humidity Trend")
        st.line_chart(
            df.set_index("Date")["Humidity"],
            color="#1976d2",
            width="stretch"
        )

    st.markdown("---")

    # Detailed visualizations
    st.markdown("## 📊 Data Visualizations")
    st.caption("Detailed analysis and visual representation of weather data")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🌧️ Precipitation Analysis")
        st.bar_chart(
            df.set_index("Date")["Precipitation"],
            color="#1976d2",
            width="stretch"
        )

    with col2:
        st.markdown("### 💨 Wind Speed Trend")
        st.line_chart(
            df.set_index("Date")["WindSpeed"],
            color="#239447",
            width="stretch"
        )

    with col3:
        st.markdown("### 🌡️ Monthly Temperature")
        monthly_temp = df.copy()
        monthly_temp["Month"] = pd.to_datetime(
            monthly_temp["Date"]
        ).dt.strftime("%b")

        monthly_avg = monthly_temp.groupby(
            "Month", sort=False
        )["Temperature"].mean()

        st.bar_chart(
            monthly_avg,
            color="#ff9838",
            width="stretch"
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🌤️ Weather Condition Distribution")
        weather_counts = df["Weather"].value_counts()

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(
            weather_counts,
            labels=weather_counts.index,
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")
        st.pyplot(fig, width="stretch")
        plt.close(fig)

    with col2:
        st.markdown("###  Temperature vs Precipitation")
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.scatter(
            df["Temperature"],
            df["Precipitation"],
            color="#e53935"
        )
        ax.set_xlabel("Temperature (°C)")
        ax.set_ylabel("Precipitation (mm)")
        ax.grid(alpha=0.2)
        st.pyplot(fig, width="stretch")
        plt.close(fig)

    with col3:
        st.markdown("### 🔥 Correlation Heatmap")
        numeric_df = df.select_dtypes(include="number")
        correlation = numeric_df.corr()

        fig, ax = plt.subplots(figsize=(5, 4))
        sns.heatmap(
            correlation,
            annot=True,
            cmap="coolwarm",
            fmt=".2f",
            ax=ax
        )
        st.pyplot(fig, width="stretch")
        plt.close(fig)
elif page == "Data View":
    st.markdown("""
    <h1 style="color:#12355b;">📋 Complete Weather Data</h1>
    <p style="color:#667085;">Explore and inspect the complete weather dataset.</p>
    """, unsafe_allow_html=True)

    # Choose which dataset to view
    data_choice = st.radio(
        "Select Dataset",
        ["Original Data", "Cleaned Data"],
        horizontal=True,
        key="dv_dataset"
    )

    cleaned_df = df.drop_duplicates().dropna().copy()
    removed = len(df) - len(cleaned_df)

    if data_choice == "Cleaned Data":
        view_df = cleaned_df
        st.success(
            f"🧹 Showing cleaned data: {removed} duplicate/missing record(s) removed."
        )
    else:
        view_df = df

    # Dataset summary cards
    total_rows = len(view_df)
    total_columns = len(view_df.columns)
    duplicates = int(view_df.duplicated().sum())
    missing_values = int(view_df.isnull().sum().sum())

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📄 Total Records", total_rows)
    col2.metric("📊 Total Columns", total_columns)
    col3.metric("🔁 Duplicate Rows", duplicates)
    col4.metric("❓ Missing Values", missing_values)

    st.markdown("<br>", unsafe_allow_html=True)

    # Search and display table
    st.markdown("### 🔎 Weather Records")

    search_text = st.text_input(
        "Search records",
        placeholder="Enter a city or weather condition..."
    )

    if search_text:
        mask = view_df.astype(str).apply(
            lambda column: column.str.contains(
                search_text, case=False, na=False
            )
        ).any(axis=1)
        display_df = view_df[mask]
    else:
        display_df = view_df

    st.caption(f"Showing {len(display_df)} of {total_rows} records ({data_choice})")

    st.dataframe(
        display_df,
        width="stretch",
        height=500,
        hide_index=True
    )

    if data_choice == "Cleaned Data":
        st.download_button(
            label="📥 Download Cleaned Data",
            data=cleaned_df.to_csv(index=False),
            file_name="cleaned_weather_data.csv",
            mime="text/csv",
            key="dv_download_cleaned"
        )

elif page == "Analysis":
    st.subheader("🔬 Weather Analysis")

    st.write("### Statistical Summary")
    st.dataframe(
    df.describe().round(2),
    width="stretch",
    hide_index=False
)

    st.write("### Weather Feature Correlation")
    numeric_df = df.select_dtypes(include="number")
    if len(numeric_df.columns) >= 2:
        correlation = numeric_df.corr()
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Not enough numeric columns for correlation analysis.")

    st.write("### 📍 Location-wise Average Temperature")

    location_temperature = df.groupby("Location")["Temperature"].mean()

    fig, ax = plt.subplots(figsize=(10, 5))

    bars = ax.bar(
        location_temperature.index,
        location_temperature.values,
        color="#3B82F6",
        width=0.6
    )

    ax.bar_label(bars, fmt="%.1f°C", padding=5, fontsize=11)

    ax.set_xlabel("Location", fontsize=12)
    ax.set_ylabel("Average Temperature (°C)", fontsize=12)
    ax.set_title("Average Temperature by Location", fontsize=14, fontweight="bold")

    ax.set_ylim(0, location_temperature.max() * 1.2)
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)

    plt.xticks(rotation=0)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


elif page == "Visualizations":
    st.subheader(" Weather Visualizations")
    st.caption("Explore weather trends and relationships through interactive charts.")

    viz_df = df.copy()
    viz_df["Date"] = pd.to_datetime(viz_df["Date"])
    viz_df = viz_df.sort_values("Date")

    # First row: Temperature and Humidity
    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(viz_df["Date"], viz_df["Temperature"], color="#e53935", linewidth=2)
        ax.set_title("Temperature Trend", color="#12355b", fontsize=14, fontweight="bold")
        ax.set_ylabel("Temperature (°C)")
        ax.set_xlabel("Date")
        ax.xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=2))
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%b"))
        ax.grid(True, linestyle="--", alpha=0.3)
        fig.tight_layout()
        st.pyplot(fig, width="stretch")
        plt.close(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(viz_df["Date"], viz_df["Humidity"], color="#1976d2", linewidth=2)
        ax.set_title("Humidity Trend", color="#12355b", fontsize=14, fontweight="bold")
        ax.set_ylabel("Humidity (%)")
        ax.set_xlabel("Date")
        ax.xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=2))
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%b"))
        ax.grid(True, linestyle="--", alpha=0.3)
        fig.tight_layout()
        st.pyplot(fig, width="stretch")
        plt.close(fig)

    # Second row: Precipitation and Wind Speed
    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(viz_df["Date"], viz_df["Precipitation"], color="#4a90e2", width=1.5)
        ax.set_title("Daily Precipitation", color="#12355b", fontsize=14, fontweight="bold")
        ax.set_ylabel("Precipitation (mm)")
        ax.set_xlabel("Date")
        ax.xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=2))
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%b"))
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        fig.tight_layout()
        st.pyplot(fig, width="stretch")
        plt.close(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(viz_df["Date"], viz_df["WindSpeed"], color="#239447", linewidth=2)
        ax.set_title("Wind Speed Trend", color="#12355b", fontsize=14, fontweight="bold")
        ax.set_ylabel("Wind Speed (km/h)")
        ax.set_xlabel("Date")
        ax.xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=2))
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%b"))
        ax.grid(True, linestyle="--", alpha=0.3)
        fig.tight_layout()
        st.pyplot(fig, width="stretch")
        plt.close(fig)

    # Third row: Relationship between temperature and precipitation
    st.markdown("### 🌡️ Temperature vs Precipitation")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(
        viz_df["Temperature"],
        viz_df["Precipitation"],
        color="#1976d2",
        alpha=0.65,
        s=45
    )
    ax.set_title("Temperature and Precipitation Relationship",
                 color="#12355b", fontsize=14, fontweight="bold")
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Precipitation (mm)")
    ax.grid(True, linestyle="--", alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig, width="stretch")
    plt.close(fig)

elif page == "Monthly Analysis":
    st.subheader("📅 Monthly Weather Analysis")

    monthly_df = df.copy()
    monthly_df["Month"] = pd.to_datetime(monthly_df["Date"]).dt.month

    monthly_temperature = monthly_df.groupby("Month")["Temperature"].mean()
    monthly_humidity = monthly_df.groupby("Month")["Humidity"].mean()
    monthly_rain = monthly_df.groupby("Month")["Precipitation"].sum()

    month_names = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
        5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
        9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }

    monthly_temperature.index = monthly_temperature.index.map(month_names)
    monthly_humidity.index = monthly_humidity.index.map(month_names)
    monthly_rain.index = monthly_rain.index.map(month_names)

    st.write("🌡️ Average Monthly Temperature")
    st.bar_chart(monthly_temperature)

    st.write("💧 Average Monthly Humidity")
    st.line_chart(monthly_humidity)

    st.write("🌧️ Monthly Total Precipitation")
    st.bar_chart(monthly_rain)


elif page == "Data Cleaning":
    st.subheader("🧹 Data Quality and Cleaning")

    st.write("### Original Data Quality")
    st.metric("Missing Values", int(df.isnull().sum().sum()))
    st.metric("Duplicate Rows", int(df.duplicated().sum()))

    cleaned_df = df.drop_duplicates().dropna().copy()

    st.write("### Cleaned Data Preview")
    st.dataframe(cleaned_df, width="stretch")

    st.write(f"Original records: {len(df)}")
    st.write(f"Cleaned records: {len(cleaned_df)}")
    st.write(f"Removed records: {len(df) - len(cleaned_df)}")

    cleaned_csv = cleaned_df.to_csv(index=False)

    st.download_button(
        label="📥 Download Cleaned Data",
        data=cleaned_csv,
        file_name="cleaned_weather_data.csv",
        mime="text/csv"
    )


elif page == "Download Data":
    st.subheader("⬇️ Download Weather Data")

    st.write("Download the weather records based on your selected filters.")

    csv_data = df.to_csv(index=False)

    st.download_button(
        label="📥 Download Filtered Weather Data",
        data=csv_data,
        file_name="filtered_weather_data.csv",
        mime="text/csv"
    )

    st.write("### Data Preview")
    st.dataframe(df.head(10), width="stretch")