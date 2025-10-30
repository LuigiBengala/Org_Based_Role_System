from app import schemas

#! Test get endpoint

#! Test admin get studies
def test_admin_get_all_studies(authorized_admin, test_study):
    response = authorized_admin.get("/studies/")
    
    assert len(response.json()) == len(test_study)
    assert response.status_code == 200
    
def test_admin_get_one_study(authorized_admin, test_study):
    response = authorized_admin.get(f"/studies/{test_study[0].id}")
    study = schemas.StudyOut(**response.json())
    
    assert response.status_code == 200
    assert study.title == test_study[0].title
    assert study.description == test_study[0].description
    assert study.organization_id == test_study[0].organization_id
    
#! Test study coordinator get studies
def test_study_coordinator_get_all_studies(authorized_client, test_user_coordinator1,test_study):
    authorized_coordinator = authorized_client(test_user_coordinator1["id"])
    response = authorized_coordinator.get("/studies/")

    assert response.status_code == 200
    
def test_study_coordinator_get_one_study(authorized_client, test_user_coordinator1, test_study):
    authorized_coordinator = authorized_client(test_user_coordinator1["id"])
    response = authorized_coordinator.get(f"/studies/{test_study[0].id}")
    study = schemas.StudyOut(**response.json())
    
    assert response.status_code == 200
    assert study.title == test_study[0].title
    assert study.description == test_study[0].description
    assert study.organization_id == test_study[0].organization_id

#! Test research assistant get studies

def test_research_assistant_get_all_studies(authorized_client, test_user_research_assistant1, test_study):
    authorized_research_assistant = authorized_client(test_user_research_assistant1["id"])
    response = authorized_research_assistant.get("/studies/")

    assert response.status_code == 200
    
def test_research_assistant_get_one_study(authorized_client, test_user_research_assistant1, test_study):
    authorized_research_assistant = authorized_client(test_user_research_assistant1["id"])
    response = authorized_research_assistant.get(f"/studies/{test_study[0].id}")
    study = schemas.StudyOut(**response.json())
    
    assert response.status_code == 200
    assert study.title == test_study[0].title
    assert study.description == test_study[0].description
    assert study.organization_id == test_study[0].organization_id

#! Test unauthorized get studies

def test_unauthorized_get_studies(client, test_study):
    response = client.get("/sessions/")
    
    assert response.status_code == 401
    
def test_unauthoried_get_one_study(client, test_study):
    response = client.get(f"/sessions/{test_study[0].id}")
    
    assert response.status_code == 401
    
#! Test non existent study
def test_get_non_existent_study(authorized_admin, test_study):
    response = authorized_admin.get("/sessions/0")
    
    assert response.status_code == 404
    
#! Test get study from other organization
def test_get_study_from_other_org(authorized_client, test_user_coordinator1, test_study):
    authorized_coordinator= authorized_client(test_user_coordinator1["id"])
    response = authorized_coordinator.get(f"/studies/{test_study[1].id}")
    
    assert response.status_code == 404
    
#! Test study creation

#! Test admin study creation
def test_admin_create_study(authorized_admin, test_organization):
    data = {
        "id": "study_test_org1_2",
        "title": "Study test org1 2",
        "description": "description test",
        "organization_id": "org1"
    }
    
    response = authorized_admin.post("/studies/", json=data)
    
    created_study = schemas.StudyOut(**response.json())
    assert response.status_code == 201
    assert created_study.title == data["title"]
    assert created_study.description == data["description"]
    assert created_study.organization_id == data["organization_id"]
    
#! Test study Coordinator study creation
def test_study_coordinator_create_study(authorized_client, test_user_coordinator1, test_organization):
    data = {
        "id": "study_test_org1_3",
        "title": "Study test org1 3",
        "description": "description test",
        "organization_id": "org1"
    }
    
    authorized_coordinator = authorized_client(test_user_coordinator1["id"])
    response = authorized_coordinator.post("/studies/", json=data)
    
    created_study = schemas.StudyOut(**response.json())
    assert response.status_code == 201
    assert created_study.title == data["title"]
    assert created_study.description == data["description"]
    assert created_study.organization_id == data["organization_id"]
    
#! Test unauthorized study creation

#! Test study creation with research assistant
def test_research_assistant_create_study(authorized_client, test_user_research_assistant1):
    authorized_assistant = authorized_client(test_user_research_assistant1["id"])
    response = authorized_assistant.post("/studies/", json={"id": "a", "title": "a", "description": "a", "organization_id": "a"})
    
    assert response.status_code == 403

#! Test study creation with participant
def test_participant_create_study(authorized_client, test_user_participant1):
    authorized_participant = authorized_client(test_user_participant1["id"])
    response = authorized_participant.post("/studies/", json={"id": "a", "title": "a", "description": "a", "organization_id": "a"})
    
    assert response.status_code == 403
    
#! Test unauthenticated study creation
def test_unauthenticated_create_study(client):
    response = client.post("/studies/", json={"id": "a", "title": "a", "description": "a", "organization_id": "a"})
    
    assert response.status_code == 401
    
#! Test put endpoint

#! Test study update with admin
def test_admin_edit_study(authorized_admin, test_study):
    data = {
        "title": "edited title", 
        "description": "edited description"
    }
    
    response = authorized_admin.put(f"/studies/{test_study[0].id}", json=data)
    
    edited_study = schemas.StudyEdit(**response.json())
    assert response.status_code == 200
    assert edited_study.title == data["title"]
    assert edited_study.description == data["description"]
    
#! Test study update with study coordinator
def test_study_coordinator_edit_study(authorized_client, test_user_coordinator1, test_study):
    data = {
        "title": "edited title2", 
        "description": "edited description2"
    }
    
    authorized_coordinator = authorized_client(test_user_coordinator1["id"])
    response = authorized_coordinator.put(f"/studies/{test_study[0].id}", json=data)
    
    edited_study = schemas.StudyEdit(**response.json())
    assert response.status_code == 200
    assert edited_study.title == data["title"]
    assert edited_study.description == data["description"]
    

#! Test study update with session manager
def test_research_assistant_edit_study(authorized_client, test_user_research_assistant1, test_session):
    data = {
        "title": "edited title2", 
        "description": "edited description2"
    }
    
    authorized_assistant = authorized_client(test_user_research_assistant1["id"])
    response = authorized_assistant.put(f"/studies/{test_session[0].id}", json=data)
    
    assert response.status_code == 403
    
#! Test study update with participant
def test_participant_edit_study(authorized_client, test_user_participant1, test_session):
    data = {
        "title": "edited title2", 
        "description": "edited description2"
    }
    
    authorized_participant = authorized_client(test_user_participant1["id"])
    response = authorized_participant.put(f"/studies/{test_session[0].id}", json=data)
    
    assert response.status_code == 403
    
#! Test study update with anauthenticated user
def test_unauthorized_user_edit_study(client, test_session):
    data = {
            "title": "edited title2", 
            "description": "edited description2"
        }
    
    response = client.put(f"/studies/{test_session[0].id}", json=data)
    
    assert response.status_code == 404
    
#! Test Delete Enpoint

#! Test admin delete study
def test_admin_delete_study(authorized_admin, test_study):
    response = authorized_admin.delete(f"/studies/{test_study[0].id}")
    
    assert response.status_code == 204
    
#! Test study coordinator delete study
def test_study_coordinator_delete_study(authorized_client, test_user_coordinator1, test_study):
    authorized_coordinator = authorized_client(test_user_coordinator1["id"])
    response = authorized_coordinator.delete(f"/studies/{test_study[0].id}")
    
    assert response.status_code == 404
    
#! Test research assistant delete study
def test_research_assistant_delete_study(authorized_client, test_user_research_assistant1, test_study):
    authorized_assistant = authorized_client(test_user_research_assistant1["id"])
    response = authorized_assistant.delete(f"/studies/{test_study[0].id}")
    
    assert response.status_code == 404
    
#! Test participant delete study
def test_participant_delete_study(authorized_client, test_user_participant1, test_study):
    authorized_participant = authorized_client(test_user_participant1["id"])
    response = authorized_participant.delete(f"/studies/{test_study[0].id}")
    
    assert response.status_code == 404