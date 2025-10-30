import pytest
from datetime import datetime
from app import schemas

#! Get Sessions

#! Test get sessions with admin

def test_admin_get_all_sessions(authorized_admin, test_session):
    response = authorized_admin.get("/sessions/")

    assert len(response.json()) == len(test_session)
    assert response.status_code == 200

def test_admin_get_one_session(authorized_admin, test_session):
    response = authorized_admin.get(f"/sessions/{test_session[0].id}")
    session = schemas.SessionOut(**response.json())

    assert session.id == test_session[0].id
    assert session.study_id == test_session[0].study_id
    assert session.participant_id == test_session[0].participant_id

#! Test get sessions with anauthorized

def test_unauthorized_user_get_all_sessions(client):
    response = client.get("/sessions/")
    assert response.status_code == 401

def test_unauthorized_user_get_one_session(client):
    response = client.get("/sessions/session_test_1")
    
    assert response.status_code == 401
 
#! Test get non existent session
    
def test_get_non_existent_session(authorized_admin):
    response = authorized_admin.get("/sesssions/0")
    assert response.status_code == 404

#! Test Get Sessions from research assistant

def test_get_sessions_from_research_assistant_from_same_organization(authorized_client, test_user_research_assistant1, test_session):
    authorized_research_assistant = authorized_client(test_user_research_assistant1["id"])
    response = authorized_research_assistant.get("/sessions/")
    
    assert response.status_code == 200
    
def test_get_one_session_from_research_assistant_from_same_organization(authorized_client, test_user_research_assistant1, test_session):
    authorized_research_assistant = authorized_client(test_user_research_assistant1["id"])
    response = authorized_research_assistant.get(f"/sessions/{test_session[0].id}")
    
    assert response.status_code == 200

#! Test Get other organization session with research assistant
  
def test_get_sessions_from_research_assistant_from_other_organization(authorized_client, test_user_research_assistant2, test_session):
    authorized_research_assistant = authorized_client(test_user_research_assistant2["id"])
    response = authorized_research_assistant.get(f"/sessions/{test_session[0].id}")
    
    assert response.status_code == 404

#! Test Get Sessions from Study Coordinator

def test_get_sessions_from_study_coordinator_from_same_organization(authorized_client, test_user_coordinator1, test_session):
    authorized_study_coordinator = authorized_client(test_user_coordinator1["id"])
    response = authorized_study_coordinator.get(f"/sessions/{test_session[0].id}")
    
    assert response.status_code == 200

#! Test Get other organization session with study coordinator
   
def test_get_sessions_from_study_coordinator_from_other_organization(authorized_client, test_user_coordinator2, test_session):
    authorized_study_coordinator = authorized_client(test_user_coordinator2["id"])
    response = authorized_study_coordinator.get(f"/sessions/{test_session[0].id}")
    
    assert response.status_code == 404

#! Test Get sessions with participant

def test_get_participant_get_own_session(authorized_client, test_user_participant1, test_session):
    authorized_participant = authorized_client(test_user_participant1["id"])
    response = authorized_participant.get(f"/sessions/{test_session[0].id}")
    
    assert response.status_code == 200
    
def test_participant_that_is_not_assigned_to_session(authorized_client, test_user_participant2, test_session):
    authorized_participant = authorized_client(test_user_participant2["id"])
    response = authorized_participant.get(f"/sessions/{test_session[0].id}")
    
    assert response.status_code == 404
    
    
#! Create Session

#! Test create session with admin
@pytest.mark.parametrize(
    "id, study_id, participant_id",
    [
        ("session_create_test1_org1", "study_test_org1", "participant_test1"),
        ("session_create_test2_org2", "study_test_org2", "participant_test2"),
    ],
)
def test_create_session(
    authorized_admin,
    id,
    study_id,
    participant_id,
    test_user_participant1,
    test_user_participant2,
    test_study
):
    response = authorized_admin.post(
        "/sessions/",
        json={"id": id, "study_id": study_id, "participant_id": participant_id, "scheduled_time": "2023-01-01T10:00:00"},
    )
    
    created_session = schemas.SessionCreate(**response.json())
    assert response.status_code == 201
    assert created_session.id == id
    assert created_session.study_id == study_id
    assert created_session.participant_id == participant_id

#! Test create session with study coordinator

#! Test create session with research assistant

#! Test create session with unauthorized user

def test_unauthorized_user_create_session(client):
    response = client.post("/sessions/", json={"id": "id", "study_id": "study id", "participant_id": "id", "scheduled_time": "2023-01-01T10:00:00"})
    
    assert response.status_code == 401

#! Test Delete endpoint

#! Test delete session with admin
 
def test_delete_session(authorized_admin, test_session):
    response = authorized_admin.delete(f"/sessions/{test_session[0].id}")
    
    assert response.status_code == 204
    
#! Test delete session with unauthorized user
    
def test_unauthorized_user_delete_session(client):
    response = client.delete("/sessions/session_create_test1_org1")

    assert response.status_code == 401

#! Test delete non existent session

def test_delete_non_existent_session(authorized_admin):
    response = authorized_admin.delete("/sessions/0")
    
    assert response.status_code == 404
    
#! Test update endpoint

#! Test update session with admin

def test_update_session_time(authorized_admin, test_session):
    testing_datetime = datetime(2025, 2, 17, 10, 15, 0)
    data = {
        "scheduled_time": f"{testing_datetime.isoformat()}"
    }
    response = authorized_admin.put(f"/sessions/{test_session[0].id}", json=data)
    
    updated_session = schemas.SessionEdit(**response.json())
    assert response.status_code == 200
    assert updated_session.scheduled_time.replace(tzinfo=None) == testing_datetime

def test_update_session_participant(authorized_admin, test_session, test_user_participant2):
    data = {
        "participant_id": f"{test_user_participant2["id"]}"
    }
    
    response = authorized_admin.put(f"/sessions/{test_session[0].id}", json=data)
    
    updated_session = schemas.SessionEdit(**response.json())
    assert response.status_code == 200
    assert updated_session.participant_id == data["participant_id"]

#! Test unauthorized user update session
   
def test_unauthorized_user_update_session(client):
    response = client.put("/sessions/0")
    
    assert response.status_code == 401

#! Test update non existent session

def test_update_non_existent_session(authorized_admin):
    response = authorized_admin.put("/sessions/0", json={"participant_id": "1"})
    
    assert response.status_code == 404

#! Test update session with research assistant

def test_update_session_research_assistant(authorized_client, test_user_research_assistant1, test_user_participant1_2, test_session):
    testing_datetime = datetime(2025, 2, 17, 10, 15, 0)
    data = {
        "participant_id": f"{test_user_participant1_2["id"]}",
        "scheduled_time": f"{testing_datetime.isoformat()}"
    }
    
    authorized_research_assistant = authorized_client(test_user_research_assistant1["id"])
    response = authorized_research_assistant.put(f"/sessions/{test_session[0].id}", json=data)

    updated_session = schemas.SessionEdit(**response.json())
    
    assert response.status_code == 200
    assert updated_session.participant_id == data["participant_id"]
    assert updated_session.scheduled_time.replace(tzinfo=None) == testing_datetime

#! Test update session with study coordinator

def test_update_session_study_coordinator(authorized_client, test_user_coordinator1, test_user_participant1, test_session):
    testing_datetime = datetime(2025, 2, 17, 10, 15, 0)
    data = {
        "participant_id": f"{test_user_participant1["id"]}",
        "scheduled_time": f"{testing_datetime.isoformat()}"
    }
    
    authorized_study_coordinator = authorized_client(test_user_coordinator1["id"])
    response = authorized_study_coordinator.put(f"/sessions/{test_session[0].id}", json=data)

    updated_session = schemas.SessionEdit(**response.json())
    
    assert response.status_code == 200
    assert updated_session.participant_id == data["participant_id"]
    assert updated_session.scheduled_time.replace(tzinfo=None) == testing_datetime
