import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[4] / "app"
sys.path.insert(0, str(APP_DIR))

from main import app


def test_correlation_api_returns_success():
    client = app.test_client()

    response = client.get("/api/correlation?health=SLEEP&weather=TAVG&year_start=2014&year_end=2022")

    assert response.status_code == 200


def test_correlation_api_returns_expected_payload():
    client = app.test_client()

    response = client.get("/api/correlation?health=SLEEP&weather=TAVG&year_start=2014&year_end=2022")
    data = response.get_json()

    expected_keys = {
        "correlation",
        "data",
        "health_var",
        "n",
        "regression",
        "state",
        "weather_var",
        "year_end",
        "year_start",
    }

    assert set(data.keys()) == expected_keys
    assert data["health_var"] == "SLEEP"
    assert data["weather_var"] == "TAVG"
    assert data["year_start"] == 2014
    assert data["year_end"] == 2022
    assert data["n"] == len(data["data"])
    assert data["n"] > 0


def test_correlation_api_returns_county_points():
    client = app.test_client()

    response = client.get("/api/correlation?health=SLEEP&weather=TAVG&year_start=2014&year_end=2022")
    data = response.get_json()
    first_record = data["data"][0]

    assert "fips" in first_record
    assert "county" in first_record
    assert "state" in first_record
    assert "climate" in first_record
    assert "health_val" in first_record
    assert "weather_val" in first_record
    assert "population" in first_record


def test_correlation_api_returns_400_for_invalid_var():
    client = app.test_client()

    response = client.get("/api/correlation?health=NOT_A_COLUMN&weather=TAVG")
    data = response.get_json()

    assert response.status_code == 400
    assert data == {"error": "Invalid variable"}
