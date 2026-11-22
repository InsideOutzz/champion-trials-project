
import streamlit as st
import pandas as pd
import requests

from api import (
    register_user,
    login_user,
    get_profile,
    get_buses,
    submit_report,
    get_reports,
    get_heatmap,
    get_quietest_times,
    verify_developer_key,
    generate_developer_key
)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Bus Crowd Meter",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# FUTURISTIC DESIGN
# --------------------------------------------------

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

.stTextInput input:focus {
    border: 1px solid #22D3EE !important;
    box-shadow: 0 0 10px #087FAD !important;
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

.stTabs [data-baseweb="tab"] {
    color: #A5D5E8;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    color: #22D3EE !important;
    border-bottom: 2px solid #22D3EE !important;
}

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #102A40, #0A1929);
    border: 1px solid #176080;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 0 12px rgba(34,211,238,.08);
}

div[data-testid="stMetricValue"] {
    color: #22D3EE !important;
}

div[data-testid="stMetricLabel"] {
    color: #A5D5E8 !important;
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


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "token" not in st.session_state:
    st.session_state.token = None

if "username" not in st.session_state:
    st.session_state.username = ""

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "new_developer_key" not in st.session_state:
    st.session_state.new_developer_key = None


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def show_error(response):
    try:
        detail = response.json().get("detail", response.text)
    except Exception:
        detail = response.text

    st.error(str(detail))


def get_data(response):
    if response is None:
        return None

    if response.status_code == 200:
        return response.json()

    show_error(response)
    return None


def make_dataframe(data):
    if isinstance(data, list):
        return pd.DataFrame(data)

    if isinstance(data, dict):
        for value in data.values():
            if isinstance(value, list):
                return pd.DataFrame(value)

        return pd.DataFrame([data])

    return pd.DataFrame()


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


# --------------------------------------------------
# LOGIN AND REGISTRATION
# --------------------------------------------------

def authentication_page():

    show_header()
    st.markdown("---")

    st.markdown(
        "<h2 style='text-align:center;'>Welcome to the future of public transport</h2>",
        unsafe_allow_html=True
    )

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "✨ Create Account"]
    )

    # LOGIN
    with login_tab:

        st.subheader("Access your account")

        with st.form("login_form"):

            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

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
                        token = result.get("access_token") or result.get("token")

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

                except Exception as error:
                    st.error(f"Login error: {error}")

    # REGISTER
    with register_tab:

        st.subheader("Create a new account")

        with st.form("register_form"):

            username = st.text_input("Username")
            email = st.text_input("Email", key="register_email")
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
                    response = register_user(username, email, password)

                    if response.status_code in [200, 201]:
                        st.success(
                            "Account created successfully! You can now log in."
                        )
                    else:
                        show_error(response)

                except requests.RequestException as error:
                    st.error(f"Backend connection error: {error}")

                except Exception as error:
                    st.error(f"Registration error: {error}")


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

def show_sidebar():

    st.sidebar.markdown(
        "<h2 style='color:#22D3EE;'>🚌 NAVIGATION</h2>",
        unsafe_allow_html=True
    )

    st.sidebar.markdown("---")
    st.sidebar.write(f"Welcome, **{st.session_state.username}**")

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

    if st.sidebar.button("🚪 Logout", use_container_width=True):

        st.session_state.token = None
        st.session_state.username = ""
        st.session_state.page = "Dashboard"
        st.session_state.new_developer_key = None

        st.rerun()


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

def dashboard_page():

    st.title("📊 Dashboard")
    st.write("Your real-time public transportation overview.")

    col1, col2, col3 = st.columns(3)

    try:
        buses_response = get_buses()
        buses = get_data(buses_response)

        if buses is not None:
            bus_list = buses if isinstance(buses, list) else buses.get("buses", [])
            col1.metric("🚌 Total Buses", len(bus_list))
        else:
            col1.metric("🚌 Total Buses", "N/A")

    except Exception:
        col1.metric("🚌 Total Buses", "N/A")

    try:
        reports_response = get_reports()
        reports = get_data(reports_response)

        if reports is not None:
            report_list = (
                reports if isinstance(reports, list)
                else reports.get("reports", [])
            )
            col2.metric("📋 Crowd Reports", len(report_list))
        else:
            col2.metric("📋 Crowd Reports", "N/A")

    except Exception:
        col2.metric("📋 Crowd Reports", "N/A")

    col3.metric("📡 System Status", "ONLINE")

    st.markdown("---")
    st.subheader("Welcome to Bus Crowd Meter")

    st.write("""
    Use this platform to:

    - View available buses.
    - Report how crowded a bus is.
    - Explore submitted crowd reports.
    - View crowd information on the heatmap.
    - Find quieter travel times.
    """)


# --------------------------------------------------
# BUSES
# --------------------------------------------------

def buses_page():

    st.title("🚌 Available Buses")

    if st.button("🔄 Refresh Buses"):
        st.rerun()

    try:
        response = get_buses()
        data = get_data(response)

        if data is not None:

            bus_list = (
                data if isinstance(data, list)
                else data.get("buses", [])
            )

            if bus_list:
                st.dataframe(
                    make_dataframe(bus_list),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No buses are currently available.")

    except Exception as error:
        st.error(f"Error loading buses: {error}")


# --------------------------------------------------
# SUBMIT CROWD REPORT
# --------------------------------------------------

def submit_report_page():

    st.title("📢 Submit Crowd Report")
    st.write("Help other passengers by reporting bus crowd levels.")

    try:
        buses_response = get_buses()
        buses_data = get_data(buses_response)

        if buses_data is None:
            return

        bus_list = (
            buses_data if isinstance(buses_data, list)
            else buses_data.get("buses", [])
        )

        if not bus_list:
            st.warning("No buses available for reporting.")
            return

        bus_options = {}

        for bus in bus_list:

            bus_id = bus.get("id") or bus.get("bus_id")

            bus_name = (
                bus.get("name")
                or bus.get("bus_number")
                or f"Bus {bus_id}"
            )

            if bus_id is not None:
                bus_options[bus_name] = bus_id

        if not bus_options:
            st.warning("Could not find bus IDs in the backend response.")
            return

        with st.form("report_form"):

            selected_bus = st.selectbox(
                "Select a bus",
                list(bus_options.keys())
            )

            crowd_level = st.selectbox(
                "How crowded is the bus?",
                ["Low", "Medium", "High", "Full"]
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
                st.success("Your crowd report was submitted successfully!")
            else:
                show_error(response)

    except Exception as error:
        st.error(f"Error submitting report: {error}")


# --------------------------------------------------
# REPORTS
# --------------------------------------------------

def reports_page():

    st.title("📋 Crowd Reports")

    if st.button("🔄 Refresh Reports"):
        st.rerun()

    try:
        response = get_reports()
        data = get_data(response)

        if data is not None:

            report_list = (
                data if isinstance(data, list)
                else data.get("reports", [])
            )

            if report_list:
                st.dataframe(
                    make_dataframe(report_list),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No reports have been submitted yet.")

    except Exception as error:
        st.error(f"Error loading reports: {error}")


# --------------------------------------------------
# HEATMAP
# --------------------------------------------------

def heatmap_page():

    st.title("🌍 Crowd Heatmap")
    st.write("Explore crowd information collected by the system.")

    try:
        response = get_heatmap()
        data = get_data(response)

        if data is not None:

            st.subheader("Crowd Information")

            if isinstance(data, list):
                st.dataframe(
                    make_dataframe(data),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.json(data)

    except Exception as error:
        st.error(f"Error loading heatmap: {error}")


# --------------------------------------------------
# QUIETEST TIMES
# --------------------------------------------------

def quietest_times_page():

    st.title("🕒 Quietest Travel Times")
    st.write("Discover the less crowded times to travel.")

    try:
        response = get_quietest_times()
        data = get_data(response)

        if data is not None:

            if isinstance(data, list):
                st.dataframe(
                    make_dataframe(data),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.json(data)

    except Exception as error:
        st.error(f"Error loading quietest times: {error}")


# --------------------------------------------------
# DEVELOPER KEY
# --------------------------------------------------


def developer_key_page():

    st.title("🔑 Developer Key")
    st.write("Generate and manage your developer access key.")

    token = st.session_state.get("token")

    if not token:
        st.warning("Please log in first.")
        return

    # GENERATE KEY
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
                    st.error("The server did not return a developer key.")

            else:
                show_error(response)

        except requests.RequestException as error:
            st.error(f"Could not connect to backend: {error}")

        except Exception as error:
            st.error(f"Error generating key: {error}")

    # DISPLAY GENERATED KEY
    key = st.session_state.get("new_developer_key")

    if key:
        st.subheader("Your Developer Key")
        st.code(key, language=None)

        st.warning(
            "Save this key somewhere safe. "
            "The original key may only be shown when it is generated."
        )

    st.markdown("---")

    # VERIFY KEY
    st.subheader("Verify Developer Key")

    developer_key = st.text_input(
        "Enter Developer Key",
        type="password",
        placeholder="Enter your developer key..."
    )

    if st.button("Verify Developer Key"):

        if not developer_key:
            st.error("Please enter your developer key.")

        else:
            try:
                response = verify_developer_key(
                    developer_key,
                    token
                )

                if response.status_code == 200:

                    result = response.json()

                    if result.get("valid"):
                        st.success("Developer key verified successfully!")
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

            except Exception as error:
                st.error(f"Verification error: {error}")


# --------------------------------------------------
# MAIN APPLICATION
# --------------------------------------------------

def main():

    if not st.session_state.token:

        authentication_page()

    else:

        show_sidebar()

        if st.session_state.page == "Dashboard":
            dashboard_page()

        elif st.session_state.page == "Buses":
            buses_page()

        elif st.session_state.page == "Submit Report":
            submit_report_page()

        elif st.session_state.page == "Reports":
            reports_page()

        elif st.session_state.page == "Heatmap":
            heatmap_page()

        elif st.session_state.page == "Quietest Times":
            quietest_times_page()

        elif st.session_state.page == "Developer Key":
            developer_key_page()


if __name__ == "__main__":
    main()
