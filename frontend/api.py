import requests

API_URL = "http://127.0.0.1:8000"

def generate_developer_key(token):
    return requests.post(
        f"{API_URL}/developer-keys/",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10
    )


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
        headers={"Authorization": f"Bearer {token}"},
        timeout=10
    )


def get_buses():
    return requests.get(
        f"{API_URL}/buses/",
        timeout=10
    )


def submit_report(bus_id, crowd_level, token):
    return requests.post(
        f"{API_URL}/reports/",
        json={
            "bus_id": bus_id,
            "crowd_level": crowd_level
        },
        headers={"Authorization": f"Bearer {token}"},
        timeout=10
    )


def get_reports():
    return requests.get(
        f"{API_URL}/reports/",
        timeout=10
    )


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

def verify_developer_key(key, token):
    return requests.post(
        f"{API_URL}/developer-keys/verify",
        json={"key": key},
        headers={"Authorization": f"Bearer {token}"},
        timeout=10
    )

def generate_developer_key(token):
    return requests.post(
        f"{API_URL}/developer-keys/",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10
    )