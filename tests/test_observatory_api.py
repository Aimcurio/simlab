"""Automated tests for SimLab Observatory REST API endpoints."""

import pytest
from starlette.testclient import TestClient
from simlab.observatory.server import create_observatory_app


@pytest.fixture(scope="module")
def client():
    app = create_observatory_app()
    with TestClient(app) as test_client:
        yield test_client


def test_observatory_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "SimLab Observatory" in response.text


def test_api_scenarios(client):
    response = client.get("/api/scenarios")
    assert response.status_code == 200
    data = response.json()
    assert "scenarios" in data
    assert any(s["scenario_id"] == "cooperative_pipeline" for s in data["scenarios"])


def test_api_governance(client):
    response = client.get("/api/governance")
    assert response.status_code == 200
    data = response.json()
    assert "canonical_lifecycle_state" in data


def test_api_runs(client):
    response = client.get("/api/runs")
    assert response.status_code == 200
    data = response.json()
    assert "runs" in data
    assert isinstance(data["runs"], list)


def test_api_benchmarks_routing(client):
    response = client.get("/api/benchmarks/routing")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 3


def test_api_benchmarks_coding(client):
    response = client.get("/api/benchmarks/coding")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "pass_rate" in data["results"]


def test_api_benchmarks_invalid(client):
    response = client.get("/api/benchmarks/unknown_type")
    assert response.status_code == 400


def test_api_memory_query(client):
    response = client.post(
        "/api/memory/query",
        json={"query_vec": [0.1, 0.2, 0.3], "alpha": 0.3, "beta": 0.4, "gamma": 0.3}
    )
    assert response.status_code == 200
    data = response.json()
    assert "retrieved" in data
    assert len(data["retrieved"]) > 0


def test_api_start_run_and_fetch(client):
    response = client.post(
        "/api/start_run",
        json={
            "scenario_id": "cooperative_pipeline",
            "seed": 999,
            "steps": 3,
            "fault_loss": 0.0,
            "fault_delay": 0
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    run_id = data["run_id"]
    assert run_id is not None

    # Fetch detail
    detail_res = client.get(f"/api/run/{run_id}")
    assert detail_res.status_code == 200
    detail_data = detail_res.json()
    assert detail_data["manifest"]["run_id"] == run_id

    # Fetch events
    events_res = client.get(f"/api/run/{run_id}/events")
    assert events_res.status_code == 200
    events_data = events_res.json()
    assert events_data["total_events"] > 0
    assert len(events_data["events"]) == events_data["total_events"]


def test_api_run_not_found(client):
    res = client.get("/api/run/definitely_not_a_real_run_id_xyz")
    assert res.status_code == 404


def test_api_run_verify(client):
    # Verify the created run
    runs_res = client.get("/api/runs")
    runs = runs_res.json()["runs"]
    assert len(runs) > 0
    target_run_id = runs[0]["run_id"]

    verify_res = client.get(f"/api/run/{target_run_id}/verify")
    assert verify_res.status_code == 200
    vdata = verify_res.json()
    assert vdata["chain_valid"] is True
    assert vdata["state_replay_valid"] is True
    assert vdata["is_fully_verified"] is True


def test_api_run_verify_not_found(client):
    res = client.get("/api/run/nonexistent_run_404/verify")
    assert res.status_code == 404
