import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app as fastapi_app, activities


@pytest.fixture
def client():
    return TestClient(fastapi_app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Snapshot and restore the in-memory `activities` between tests."""
    snapshot = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(snapshot)
