
import streamlit as st
import pandas as pd
import requests

from api import (
    register_user,
    login_user,
    get_profile,
    get_buses,
    add_bus,
    submit_report,
    get_reports,
    get_my_reports,
    update_report,
    delete_report,
    get_heatmap,
    get_quietest_times,
    verify_developer_key,
    generate_developer_key
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Bus Crowd Meter",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# DESIGN
# ==========================================

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 15% 10%, #102D48 0%, transparent 35%),
        linear-gradient(135deg, #050B16, #091827, #07111F);
    color: #E0F7FF;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #DDF8FF !important;
    letter-spacing: 1px;
}

p, label, .stMarkdown {
    color: #B6D5E3;
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background-color: #102438 !important;
    color: #E0F7FF !important;
    border: 1px solid #176080 !important;
    border-radius: 10px !important;
}

.stButton button,
.stFormSubmitButton button {
    background: linear-gradient(90deg, #087FAD, #155EAA);
    color: white !important;
    border: 1px solid #22D3EE !important;
    border-radius: 10px;
    font-weight: 600;
    transition: all .25s ease;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    background: linear-gradient(90deg, #0891B2, #2563EB);
    box-shadow: 0 0 18px #0891B2;
    transform: translateY(-2px);
}

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #102A40, #0A1929);
    border: 1px solid #176080;
    border-radius: 14px;
    padding: 20px;
}

div[data-testid="stMetricValue"] {
    color: #22D3EE !important;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #081421, #102438);
    border-right: 1px solid #176080;
}

hr {
    border-color: #176080;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "token": None,
    "username": "",
    "page": "Dashboard",
    "new_developer_key": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# HELPERS
# ==========================================

def show_error(response):
    try:
        detail = response.json().get("detail", response.text)
    except Exception:
        detail = response.text

    st.error(str(detail))


def get_data(response):
    if response is None:
        return None

    if response.status_code in [200, 201]:
        return response.json()

    show_error(response)
    return None


def show_header():
    st.markdown("""
    <div style="text-align:center; padding:20px 0;">
        <h1 style="
            color:#22D3EE;
            font-size:42px;
            letter-spacing:4px;
            text-shadow:0 0 15px #087FAD;
        ">
            🚌 BUS CROWD METER
        </h1>
        <p style="
            color:#77A9C1;
            letter-spacing:3px;
            font-size:12px;
        ">
            SMART TRANSPORTATION INTELLIGENCE SYSTEM
        </p>
    </div>
    """, unsafe_allow_html=True)


def bus_label(bus):
    return (
        f"Line {bus['line_number']} - {bus['route_name']}"
    )


def load_buses():
    response = get_buses()
    data = get_data(response)

    if isinstance(data, list):
        return data

    return []


def load_reports():
    response = get_reports()
    data = get_data(response)

    if isinstance(data, list):
        return data

    return []


# ==========================================
# LOGIN AND REGISTRATION
# ==========================================

def authentication_page():

    show_header()
    st.markdown("---")

    st.markdown(
        "<h2 style='text-align:center;'>"
        "Welcome to the future of public transport"
        "</h2>",
        unsafe_allow_html=True
    )

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "✨ Create Account"]
    )

    with login_tab:

        st.subheader("Access your account")

        with st.form("login_form"):

            email = st.text_input("Email")
            password = st.text_input(
                "Password",
                type="password"
            )

            login_button = st.form_submit_button(
                "Login",
                use_container_width=True
            )

        if login_button:

            if not email or not password:
                st.warning("Please enter your email and password.")

            else:
                try:
                    response = login_user(email, password)

                    if response.status_code == 200:

                        result = response.json()

                        token = (
                            result.get("access_token")
                            or result.get("token")
                        )

                        if token:

                            st.session_state.token = token

                            profile_response = get_profile(token)

                            if profile_response.status_code == 200:
                                profile = profile_response.json()
                                st.session_state.username = profile.get(
                                    "username", email
                                )
                            else:
                                st.session_state.username = email

                            st.success("Login successful!")
                            st.rerun()

                        else:
                            st.error("No access token was returned.")

                    else:
                        show_error(response)

                except requests.RequestException as error:
                    st.error(f"Backend connection error: {error}")

    with register_tab:

        st.subheader("Create a new account")

        with st.form("register_form"):

            username = st.text_input("Username")
            email = st.text_input(
                "Email",
                key="register_email"
            )
            password = st.text_input(
                "Password",
                type="password",
                key="register_password"
            )

            register_button = st.form_submit_button(
                "Register",
                use_container_width=True
            )

        if register_button:

            if not username or not email or not password:
                st.warning("Please complete all fields.")

            else:
                try:
                    response = register_user(
                        username,
                        email,
                        password
                    )

                    if response.status_code in [200, 201]:
                        st.success(
                            "Account created! You can now log in."
                        )
                    else:
                        show_error(response)

                except requests.RequestException as error:
                    st.error(f"Backend connection error: {error}")


# ==========================================
# SIDEBAR
# ==========================================

def show_sidebar():

    st.sidebar.markdown(
        "<h2 style='color:#22D3EE;'>🚌 NAVIGATION</h2>",
        unsafe_allow_html=True
    )

    st.sidebar.markdown("---")
    st.sidebar.write(
        f"Welcome, **{st.session_state.username}**"
    )

    pages = [
        "Dashboard",
        "Buses",
        "Submit Report",
        "Reports",
        "Heatmap",
        "Quietest Times",
        "Developer Key"
    ]

    if st.session_state.page not in pages:
        st.session_state.page = "Dashboard"

    selected_page = st.sidebar.radio(
        "Choose a page",
        pages,
        index=pages.index(st.session_state.page)
    )

    st.session_state.page = selected_page

    st.sidebar.markdown("---")

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):
        st.session_state.token = None
        st.session_state.username = ""
        st.session_state.page = "Dashboard"
        st.session_state.new_developer_key = None
        st.rerun()


# ==========================================
# DASHBOARD
# ==========================================

def dashboard_page():

    st.title("📊 Dashboard")
    st.write("Your public transportation overview.")

    col1, col2, col3 = st.columns(3)

    try:
        buses = load_buses()
        reports = load_reports()

        col1.metric("🚌 Total Bus Lines", len(buses))
        col2.metric("📋 Crowd Reports", len(reports))
        col3.metric("📡 System Status", "ONLINE")

    except requests.RequestException:
        st.error("Could not connect to the backend.")
        return

    st.markdown("---")
    st.subheader("Welcome to Bus Crowd Meter")

    st.write("""
    Use this platform to:

    - View available bus lines.
    - Add new bus lines.
    - Report how crowded a bus is.
    - View crowd reports.
    - Edit or delete your own reports.
    - Explore crowd information and quieter travel times.
    """)


# ==========================================
# BUS LINES
# ==========================================

def buses_page():

    st.title("🚌 Bus Lines")
    st.write("View existing bus lines or add a new one.")

    st.subheader("➕ Add a Bus Line")

    with st.form("add_bus_form"):

        line_number = st.text_input(
            "Bus line number",
            placeholder="Example: 4"
        )

        route_name = st.text_input(
            "Route name",
            placeholder="Example: City Center - University"
        )

        add_button = st.form_submit_button(
            "Add Bus Line",
            use_container_width=True
        )

    if add_button:

        if not line_number.strip() or not route_name.strip():
            st.warning("Please complete both fields.")

        else:
            try:
                response = add_bus(
                    line_number.strip(),
                    route_name.strip(),
                    st.session_state.token
                )

                if response.status_code in [200, 201]:
                    st.success("Bus line added successfully!")
                    st.rerun()
                else:
                    show_error(response)

            except requests.RequestException as error:
                st.error(f"Backend connection error: {error}")

    st.markdown("---")
    st.subheader("Available Bus Lines")

    if st.button("🔄 Refresh Bus Lines"):
        st.rerun()

    try:
        buses = load_buses()

        if buses:
            st.dataframe(
                pd.DataFrame(buses),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No bus lines are currently available.")

    except requests.RequestException as error:
        st.error(f"Could not load bus lines: {error}")


# ==========================================
# SUBMIT REPORT
# ==========================================

def submit_report_page():

    st.title("📢 Submit Crowd Report")
    st.write(
        "Help other passengers by reporting bus crowd levels."
    )

    try:
        buses = load_buses()

        if not buses:
            st.warning("No bus lines available. Add a bus line first.")
            return

        bus_options = {
            bus_label(bus): bus["id"]
            for bus in buses
        }

        with st.form("report_form"):

            selected_bus = st.selectbox(
                "Select a bus line",
                list(bus_options.keys())
            )

            crowd_level = st.selectbox(
                "How crowded is the bus?",
                ["empty", "low", "medium", "high", "full"]
            )

            submit_button = st.form_submit_button(
                "Submit Report",
                use_container_width=True
            )

        if submit_button:

            response = submit_report(
                bus_options[selected_bus],
                crowd_level,
                st.session_state.token
            )

            if response.status_code in [200, 201]:
                st.success(
                    "Your crowd report was submitted successfully!"
                )
            else:
                show_error(response)

    except requests.RequestException as error:
        st.error(f"Backend connection error: {error}")


# ==========================================
# REPORTS
# ==========================================

def reports_page():

    st.title("📋 Crowd Reports")

    all_tab, my_tab = st.tabs(
        ["🌍 All Reports", "👤 My Reports"]
    )

    # ALL REPORTS

    with all_tab:

        st.subheader("All submitted reports")

        try:
            reports = load_reports()

            if reports:
                st.dataframe(
                    pd.DataFrame(reports),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No reports have been submitted yet.")

        except requests.RequestException as error:
            st.error(f"Could not load reports: {error}")

    # MY REPORTS

    with my_tab:

        st.subheader("Manage your reports")

        try:
            response = get_my_reports(
                st.session_state.token
            )

            my_reports = get_data(response)

            if my_reports is None:
                return

            if not my_reports:
                st.info("You haven't submitted any reports yet.")
                return

            st.dataframe(
                pd.DataFrame(my_reports),
                use_container_width=True,
                hide_index=True
            )

            st.markdown("---")
            st.subheader("Edit or Delete a Report")

            report_options = {
                f"Report #{report['id']} - "
                f"{report['crowd_level']} "
                f"(Bus ID: {report['bus_id']})": report
                for report in my_reports
            }

            selected_label = st.selectbox(
                "Select your report",
                list(report_options.keys())
            )

            selected_report = report_options[selected_label]
            report_id = selected_report["id"]

            st.write(
                f"Current crowd level: "
                f"**{selected_report['crowd_level']}**"
            )

            with st.form(f"edit_report_{report_id}"):

                new_level = st.selectbox(
                    "New crowd level",
                    ["empty", "low", "medium", "high", "full"],
                    index=[
                        "empty", "low", "medium", "high", "full"
                    ].index(selected_report["crowd_level"])
                )

                edit_button = st.form_submit_button(
                    "Save Changes",
                    use_container_width=True
                )

            if edit_button:

                update_response = update_report(
                    report_id,
                    new_level,
                    st.session_state.token
                )

                if update_response.status_code == 200:
                    st.success("Report updated successfully!")
                    st.rerun()
                else:
                    show_error(update_response)

            st.markdown("---")

            if st.button(
                f"🗑️ Delete Report #{report_id}",
                key=f"delete_{report_id}"
            ):

                delete_response = delete_report(
                    report_id,
                    st.session_state.token
                )

                if delete_response.status_code == 200:
                    st.success("Report deleted successfully!")
                    st.rerun()
                else:
                    show_error(delete_response)

        except requests.RequestException as error:
            st.error(f"Could not manage reports: {error}")


# ==========================================
# HEATMAP
# ==========================================

def heatmap_page():

    st.title("🌍 Crowd Heatmap")
    st.write("Explore crowd information collected by the system.")

    try:
        response = get_heatmap()
        data = get_data(response)

        if data is not None:
            if isinstance(data, list):
                st.dataframe(
                    pd.DataFrame(data),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.json(data)

    except requests.RequestException as error:
        st.error(f"Error loading heatmap: {error}")


# ==========================================
# QUIETEST TIMES
# ==========================================

def quietest_times_page():

    st.title("🕒 Quietest Travel Times")
    st.write("Discover less crowded times to travel.")

    try:
        response = get_quietest_times()
        data = get_data(response)

        if data is not None:
            if isinstance(data, list):
                st.dataframe(
                    pd.DataFrame(data),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.json(data)

    except requests.RequestException as error:
        st.error(f"Error loading quietest times: {error}")


# ==========================================
# DEVELOPER KEY
# ==========================================

def developer_key_page():

    st.title("🔑 Developer Key")
    st.write("Generate and manage your developer access key.")

    token = st.session_state.token

    st.subheader("Generate Developer Key")

    if st.button("🔑 Generate Developer Key"):

        try:
            response = generate_developer_key(token)

            if response.status_code in [200, 201]:

                result = response.json()
                key = result.get("developer_key")

                if key:
                    st.session_state.new_developer_key = key
                    st.success("Developer key generated successfully!")
                else:
                    st.error("No developer key was returned.")

            else:
                show_error(response)

        except requests.RequestException as error:
            st.error(f"Backend connection error: {error}")

    key = st.session_state.new_developer_key

    if key:
        st.subheader("Your Developer Key")
        st.code(key, language=None)
        st.warning("Save this key somewhere safe.")

    st.markdown("---")
    st.subheader("Verify Developer Key")

    developer_key = st.text_input(
        "Enter Developer Key",
        type="password"
    )

    if st.button("Verify Developer Key"):

        if not developer_key:
            st.warning("Please enter your developer key.")

        else:
            try:
                response = verify_developer_key(
                    developer_key,
                    token
                )

                if response.status_code == 200:

                    result = response.json()

                    if result.get("valid"):
                        st.success("Developer key verified!")
                    else:
                        st.error(
                            result.get(
                                "message",
                                "Invalid developer key."
                            )
                        )

                else:
                    show_error(response)

            except requests.RequestException as error:
                st.error(f"Backend connection error: {error}")


# ==========================================
# MAIN
# ==========================================

def main():

    if not st.session_state.token:
        authentication_page()
        return

    show_sidebar()

    pages = {
        "Dashboard": dashboard_page,
        "Buses": buses_page,
        "Submit Report": submit_report_page,
        "Reports": reports_page,
        "Heatmap": heatmap_page,
        "Quietest Times": quietest_times_page,
        "Developer Key": developer_key_page
    }

    pages[st.session_state.page]()


if __name__ == "__main__":
    main()
