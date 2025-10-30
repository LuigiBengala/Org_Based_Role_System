import pytest
from jose import jwt
from app import schemas
from app.config import settings

#! Test login


def test_sysadmin_login(client):
    response = client.post(
        "/login", data={"username": "sysadmin_test", "password": "123"}
    )

    login_response = schemas.Token(**response.json())
    payload = jwt.decode(
        login_response.access_token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )
    id = payload.get("user_id")

    assert id == "sysadmin_test"
    assert login_response.token_type == "bearer"
    assert response.status_code == 200


#! Test sysadmin login with incorrect credentials


@pytest.mark.parametrize(
    "username, password, status_code",
    [
        ("wrong_username", "123", 403),
        ("sysadmin_test", "wrongpassword", 403),
        ("wrong_username", "wrongpassword", 403),
        (None, "123", 403),
        ("sysadmin_test", None, 403),
    ],
)
def test_sysadmin_incorrect_login(client, username, password, status_code):
    response = client.post("/login", data={"username": username, "password": password})

    assert response.status_code == status_code


#! Test user creation


@pytest.mark.parametrize(
    "id, email, password, role, organization_id",
    [
        (
            "test_researchAssistant_org1",
            "researchAssistant_test_org1@gmail.com",
            "123",
            schemas.RoleEnum.research_assistant,
            "org1",
        ),
        (
            "test_researchAssistant_org2",
            "researchAssistant_test_org2@gmail.com",
            "123",
            schemas.RoleEnum.research_assistant,
            "org2",
        ),
        (
            "test_studyCoordinator_org1",
            "studyCoordinator_test_org1@gmail.com",
            "123",
            schemas.RoleEnum.study_coordinator,
            "org1",
        ),
        (
            "test_studyCoordinator_org2",
            "studyCoordinator_test_org2@gmail.com",
            "123",
            schemas.RoleEnum.study_coordinator,
            "org2",
        ),
        (
            "test_participant_org1",
            "participant_test_org1@gmail.com",
            "123",
            schemas.RoleEnum.participant,
            "org1",
        ),
        (
            "test_participant_org2",
            "participant_test_org2@gmail.com",
            "123",
            schemas.RoleEnum.participant,
            "org2",
        ),
    ],
)
def test_user_creation(
    authorized_admin, id, email, password, role, organization_id, test_organization
):
    response = authorized_admin.post(
        "/users/",
        json={
            "id": id,
            "email": email,
            "password": password,
            "role": role,
            "organization_id": organization_id,
        },
    )

    new_user = schemas.UserOut(**response.json())
    assert new_user.id == id
    assert response.status_code == 201


#! Test user creation with research assistant
def test_user_creation_with_research_assistant(
    authorized_client, test_user_research_assistant1
):
    data = {
        "id": "test_participant_org2",
        "email": "participant_test_org2@gmail.com",
        "password": "123",
        "role": schemas.RoleEnum.participant,
        "organization_id": "org2",
    }

    authorized_assistant = authorized_client(test_user_research_assistant1["id"])
    response = authorized_assistant.post("/users/", json=data)

    assert response.status_code == 404


#! Test user creation with study coordiantor
def test_user_creation_with_study_coordinator(
    authorized_client, test_user_coordinator1
):
    data = {
        "id": "test_participant_org2",
        "email": "participant_test_org2@gmail.com",
        "password": "123",
        "role": schemas.RoleEnum.participant,
        "organization_id": "org2",
    }

    authorized_coordinator = authorized_client(test_user_coordinator1["id"])
    response = authorized_coordinator.post("/users/", json=data)

    assert response.status_code == 404


#! Test user creation with participant
def test_user_creation_with_participant(
    authorized_client, test_user_participant1
):
    data = {
        "id": "test_participant_org2",
        "email": "participant_test_org2@gmail.com",
        "password": "123",
        "role": schemas.RoleEnum.participant,
        "organization_id": "org2",
    }

    authorized_participant = authorized_client(test_user_participant1["id"])
    response = authorized_participant.post("/users/", json=data)

    assert response.status_code == 404

#! Test delete user

def test_unauthorized_delete_user(client):
    response = client.delete("/users/1")

    assert response.status_code == 401
