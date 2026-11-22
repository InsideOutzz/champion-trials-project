
import requests

API_URL = "http://127.0.0.1:8000"


def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


# AUTHENTICATION

def register_user(username, email, password):
    return requests.post(
        f"{API_URL}/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password
        },
        timeout=10
    )


def login_user(email, password):
    return requests.post(
        f"{API_URL}/auth/login",
        json={
            "email": email,
            "password": password
        },
        timeout=10
    )


def get_profile(token):
    return requests.get(
        f"{API_URL}/auth/me",
        headers=auth_headers(token),
        timeout=10
    )


# BUS LINES

def get_buses():
    return requests.get(
        f"{API_URL}/buses/",
        timeout=10
    )


def add_bus(line_number, route_name, token):
    return requests.post(
        f"{API_URL}/buses/",
        json={
            "line_number": line_number,
            "route_name": route_name
        },
        headers=auth_headers(token),
        timeout=10
    )


# CROWD REPORTS

def submit_report(bus_id, crowd_level, token):
    return requests.post(
        f"{API_URL}/reports/",
        json={
            "bus_id": bus_id,
            "crowd_level": crowd_level
        },
        headers=auth_headers(token),
        timeout=10
    )


def get_reports():
    return requests.get(
        f"{API_URL}/reports/",
        timeout=10
    )


def get_my_reports(token):
    return requests.get(
        f"{API_URL}/reports/my",
        headers=auth_headers(token),
        timeout=10
    )


def update_report(report_id, crowd_level, token):
    return requests.put(
        f"{API_URL}/reports/{report_id}",
        json={
            "crowd_level": crowd_level
        },
        headers=auth_headers(token),
        timeout=10
    )


def delete_report(report_id, token):
    return requests.delete(
        f"{API_URL}/reports/{report_id}",
        headers=auth_headers(token),
        timeout=10
    )


# HEATMAP

def get_heatmap():
    return requests.get(
        f"{API_URL}/heatmap/",
        timeout=10
    )


def get_quietest_times():
    return requests.get(
        f"{API_URL}/heatmap/quietest",
        timeout=10
    )


# DEVELOPER KEYS

def generate_developer_key(token):
    return requests.post(
        f"{API_URL}/developer-keys/",
        headers=auth_headers(token),
        timeout=10
    )


def verify_developer_key(key, token):
    return requests.post(
        f"{API_URL}/developer-keys/verify",
        json={"key": key},
        headers=auth_headers(token),
        timeout=10
    )
