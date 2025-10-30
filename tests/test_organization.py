from app import schemas


#! Test get organizations

def test_get_organizations(authorized_admin, test_organization):
    response = authorized_admin.get("/organizations/")
    
    assert len(response.json()) == len(test_organization)
    assert response.status_code == 200
    
def test_get_organization(authorized_admin, test_organization):
    response = authorized_admin.get(f"/organizations/{test_organization[0].id}")
    
    organization = schemas.OrganizationBase(**response.json())
    
    assert response.status_code == 200
    assert organization.id ==  test_organization[0].id
    assert organization.name ==  test_organization[0].name
    
#! Test get organizations with research assistant
def test_get_organizations_with_research_assistant(authorized_client, test_user_research_assistant1, test_organization):
    authorized_research_assistant = authorized_client(test_user_research_assistant1["id"])
    response = authorized_research_assistant.get("/organizations/")
    
    assert response.status_code == 404
    
def test_get_organization_with_research_assistant(authorized_client, test_user_research_assistant1, test_organization):
    authorized_research_assistant = authorized_client(test_user_research_assistant1["id"])
    
    response = authorized_research_assistant.get("/organizations/org1")
    assert response.status_code == 404
    
#! Test get organizations with study coordinator
def test_get_organizations_with_study_coordinator(authorized_client, test_user_coordinator1, test_organization):
    authorized_study_coordinator = authorized_client(test_user_coordinator1["id"])
    response = authorized_study_coordinator.get("/organizations/")
    
    assert response.status_code == 404
    
def test_get_organization_with_study_coordinator(authorized_client, test_user_coordinator1, test_organization):
    authorized_study_coordinator = authorized_client(test_user_coordinator1["id"])
    
    response = authorized_study_coordinator.get("/organizations/org1")
    assert response.status_code == 404
    
#! Test get organizations with participant
def test_get_organizations_with_participant(authorized_client, test_user_participant1, test_organization):
    authorized_participant = authorized_client(test_user_participant1["id"])
    response = authorized_participant.get("/organizations/")
    
    assert response.status_code == 404
    
def test_get_organization_with_participant(authorized_client, test_user_participant1, test_organization):
    authorized_participant = authorized_client(test_user_participant1["id"])
    
    response = authorized_participant.get("/organizations/org1")
    assert response.status_code == 404

#! Test create organization

#! Test create organization with admin
def test_create_organization_with_admin(authorized_admin):
    data = {
        "id": "org3",
        "name": "organization2"
    }
    
    response = authorized_admin.post("/organizations/", json=data)
    created_organization = schemas.OrganizationCreate(**response.json())
    
    assert response.status_code == 201
    assert created_organization.id == data["id"]
    assert created_organization.name == data["name"]
    
#! Test create organization with research assistant
def test_create_organization_with_research_assistant(authorized_client, test_user_research_assistant1):
    data = {
        "id": "org3",
        "name": "organization2"
    }
    
    authorized_assistant = authorized_client(test_user_research_assistant1["id"])
    response = authorized_assistant.post("/organizations/", json=data)
    
    assert response.status_code == 404
    
#! Test create organization with study coordinator
def test_create_organization_with_study_coordinator(authorized_client, test_user_coordinator1):
    data = {
        "id": "org3",
        "name": "organization2"
    }
    
    authorized_coordinator = authorized_client(test_user_coordinator1["id"])
    response = authorized_coordinator.post("/organizations/", json=data)
    
    assert response.status_code == 404
    
#! Test create organization with participant
def test_create_organization_with_participant(authorized_client, test_user_participant1):
    data = {
        "id": "org3",
        "name": "organization2"
    }
    
    authorized_participant = authorized_client(test_user_participant1["id"])
    response = authorized_participant.post("/organizations/", json=data)
    
    assert response.status_code == 404
    
#! Test update organization
    
#! Test update organization with admin
def test_update_organization_with_admin(authorized_admin, test_organization):
    data = {
        "name": "edited name"
    }
    
    response = authorized_admin.put(f"/organizations/{test_organization[0].id}", json=data)
    updated_organization = schemas.OrganizationEdit(**response.json())
    
    assert response.status_code == 200
    assert updated_organization.name == data["name"]
    
#! Test update organization with research assistant
def test_update_organization_with_research_assistant(authorized_client, test_user_research_assistant1, test_organization):
    data = {
        "name": "edited name"
    }
    
    authorized_assistant = authorized_client(test_user_research_assistant1["id"])
    response = authorized_assistant.put("/organizations/org1", json=data)
    
    assert response.status_code == 404
    
#! Test update organization with study coordinator
def test_update_organization_with_study_coordinator(authorized_client, test_user_coordinator1, test_organization):
    data = {
        "name": "edited name"
    }
    
    authorized_coordinator = authorized_client(test_user_coordinator1["id"])
    response = authorized_coordinator.put("/organizations/org1", json=data)
    
    assert response.status_code == 404
    
#! Test update organization with participant
def test_update_organization_with_participant(authorized_client, test_user_participant1, test_organization):
    data = {
        "name": "edited name"
    }
    
    authorized_participant = authorized_client(test_user_participant1["id"])
    response = authorized_participant.put("/organizations/org1", json=data)
    
    assert response.status_code == 404
    
#! Test delete organization

#! Test delete organization with admin
def test_delete_organization_with_admin(authorized_admin, test_organization):
    response = authorized_admin.delete(f"/sessions/{test_organization[0].id}")
    
    response.status_code == 204
    
#! Test delete organization with research assistant
def test_delete_organization_with_research_assistant(authorized_client, test_user_research_assistant1):
    authorized_assistant = authorized_client(test_user_research_assistant1["id"])
    response = authorized_assistant.delete("/sessions/org1")
    
    response.status_code == 404
    
#! Test delete organization with study coordinator
def test_delete_organization_with_study_coordinator(authorized_client, test_user_coordinator1):
    authorized_coordinator = authorized_client(test_user_coordinator1["id"])
    response = authorized_coordinator.delete("/sessions/org1")
    
    response.status_code == 404
    
#! Test delete organization with participant
def test_delete_organization_with_(authorized_client, test_user_participant1):
    authorized_participant= authorized_client(test_user_participant1["id"])
    response = authorized_participant.delete("/sessions/org1")
    
    response.status_code == 404
    
