from datetime import date
import pytest

BASE_URL = "/api"

@pytest.fixture
def token(client):
    response = client.post("/auth/token", data={
        "username": "johndoe",
        "password": "secret123"
    })
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture
def auth_client(client, token):
    client.headers["Authorization"] = f"Bearer {token}"
    return client

def test_create_sample(auth_client):
    response = auth_client.post(f"{BASE_URL}/samples", json={
        "sample_type": "blood",
        "subject_id": "P001",
        "collection_date": str(date.today()),
        "status": "collected",
        "storage_location": "freezer-1-shelfA"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["sample_type"] == "blood"
    assert "sample_id" in data

def test_create_sample_with_invalid_type(auth_client):
    response = auth_client.post(f"{BASE_URL}/samples", json={
        "sample_type": "INVALID",
        "subject_id": "P010",
        "collection_date": str(date.today()),
        "status": "collected",
        "storage_location": "freezer-B"
    })
    assert response.status_code == 422

def test_create_sample_with_missing_fields(auth_client):
    response = auth_client.post(f"{BASE_URL}/samples", json={
        "sample_type": "blood"
    })
    assert response.status_code == 422

def test_get_samples(auth_client):
    response = auth_client.get(f"{BASE_URL}/samples")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_sample_by_id(auth_client):
    # First, create a sample
    response = auth_client.post(f"{BASE_URL}/samples", json={
        "sample_type": "tissue",
        "subject_id": "P002",
        "collection_date": str(date.today()),
        "status": "processing",
        "storage_location": "freezer-2-rowB"
    })
    sample_id = response.json()["sample_id"]

    # Now, retrieve it
    response = auth_client.get(f"{BASE_URL}/samples/{sample_id}")
    assert response.status_code == 200
    assert response.json()["sample_id"] == sample_id

def test_get_sample_with_invalid_id_format(auth_client):
    response = auth_client.get(f"{BASE_URL}/samples/not-a-uuid")
    assert response.status_code == 404

def test_get_non_existing_sample(auth_client):
    response = auth_client.get(f"{BASE_URL}/samples/11111111-1111-1111-1111-111111111111")
    assert response.status_code == 404

def test_update_sample(auth_client):
    # Create sample
    response = auth_client.post(f"{BASE_URL}/samples", json={
        "sample_type": "saliva",
        "subject_id": "P003",
        "collection_date": str(date.today()),
        "status": "collected",
        "storage_location": "freezer-3"
    })
    sample_id = response.json()["sample_id"]

    # Update it
    response = auth_client.put(f"{BASE_URL}/samples/{sample_id}", json={
        "status": "archived",
        "storage_location": "freezer-99"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "archived"
    assert response.json()["storage_location"] == "freezer-99"

def test_update_sample_with_invalid_field(auth_client):
    # Create valid sample
    response = auth_client.post(f"{BASE_URL}/samples", json={
        "sample_type": "saliva",
        "subject_id": "P999",
        "collection_date": str(date.today()),
        "status": "processing",
        "storage_location": "freezer-Z"
    })
    sample_id = response.json()["sample_id"]

    # Try to update with invalid enum
    response = auth_client.put(f"{BASE_URL}/samples/{sample_id}", json={
        "status": "not-a-valid-status"
    })
    assert response.status_code == 422

def test_update_non_existing_sample(auth_client):
    response = auth_client.put(f"{BASE_URL}/samples/00000000-0000-0000-0000-000000000000", json={
        "status": "archived"
    })
    assert response.status_code == 404

def test_filter_samples_by_status(auth_client):
    # Create samples
    auth_client.post(f"{BASE_URL}/samples", json={
        "sample_type": "saliva",
        "subject_id": "P101",
        "collection_date": str(date.today()),
        "status": "processing",
        "storage_location": "F-A"
    })
    auth_client.post(f"{BASE_URL}/samples", json={
        "sample_type": "tissue",
        "subject_id": "P102",
        "collection_date": str(date.today()),
        "status": "collected",
        "storage_location": "F-B"
    })

    response = auth_client.get(f"{BASE_URL}/samples?sample_status=processing")
    assert response.status_code == 200
    assert all(sample["status"] == "processing" for sample in response.json())

def test_filter_samples_by_type_and_status(auth_client):
    response = auth_client.get(f"{BASE_URL}/samples?sample_status=collected&sample_type=tissue")
    assert response.status_code == 200
    for sample in response.json():
        assert sample["status"] == "collected"
        assert sample["sample_type"] == "tissue"

def test_delete_sample(auth_client):
    # Create sample
    response = auth_client.post(f"{BASE_URL}/samples", json={
        "sample_type": "blood",
        "subject_id": "P004",
        "collection_date": str(date.today()),
        "status": "collected",
        "storage_location": "freezer-X"
    })
    sample_id = response.json()["sample_id"]

    # Delete it
    response = auth_client.delete(f"{BASE_URL}/samples/{sample_id}")
    assert response.status_code == 204

    # Confirm it's gone
    response = auth_client.get(f"{BASE_URL}/samples/{sample_id}")
    assert response.status_code == 404

def test_create_sample_same_subject_multiple_times(auth_client):
    response1 = auth_client.post(f"{BASE_URL}/samples", json={
        "sample_type": "blood",
        "subject_id": "PX1",
        "collection_date": str(date.today()),
        "status": "collected",
        "storage_location": "A"
    })

    response2 = auth_client.post(f"{BASE_URL}/samples", json={
        "sample_type": "blood",
        "subject_id": "PX1",
        "collection_date": str(date.today()),
        "status": "collected",
        "storage_location": "A"
    })

    assert response1.status_code == 200
    assert response2.status_code == 200

def test_login_with_invalid_username(client):
    response = client.post("/auth/token", data={
        "username": "notarealuser",
        "password": "secret123"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"

def test_login_with_invalid_password(client):
    response = client.post("/auth/token", data={
        "username": "johndoe",
        "password": "wrongpassword"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"

def test_access_with_invalid_jwt(client):
    headers = {"Authorization": "Bearer invalid.jwt.token"}
    response = client.get("/api/samples", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
