import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models, utils
from app.schemas import RoleEnum


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/test_{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    sysadmin = models.User(
        id="sysadmin_test",
        email="sysadmin_test@gmail.com",
        password="123",
        role=RoleEnum.admin,
        organization=None,
    )

    sysadmin.password = utils.hash(sysadmin.password)
    session.add_all([sysadmin])
    session.commit()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


"""
    Token
"""


@pytest.fixture
def admin_token():
    return create_access_token({"user_id": "sysadmin_test"})


@pytest.fixture
def authorized_admin(client, admin_token):
    client.headers = {**client.headers, "Authorization": f"Bearer {admin_token}"}

    return client

"""

    #! Orgs

"""


@pytest.fixture
def test_organization(session):
    org_data = [
        {
            "id": "org1",
            "name": "Organization1"
        },
        {
            "id": "org2",
            "name": "Organization2"
        }
    ]
    
    def create_org_model(orgs):
        return models.Organization(**orgs)
    
    org_map = map(create_org_model, org_data)
    organizations = list(org_map)

    session.add_all(organizations)
    session.commit()

    organizations = session.query(models.Organization).all()
    return organizations
    

"""

    #! Study

"""

@pytest.fixture
def test_study(session, test_organization):
    study_data = [
        {
            "id": "study_test_org1",
            "title": "Study test org 1",
            "description": "description test",
            "organization_id": "org1",
        },
        {
            "id": "study_test_org2",
            "title": "Study test org 2",
            "description": "description test",
            "organization_id": "org2",
        },
    ]

    def create_study_model(study):
        return models.Study(**study)

    study_map = map(create_study_model, study_data)
    studies = list(study_map)

    session.add_all(studies)
    session.commit()

    studies = session.query(models.Study).all()
    return studies

 
"""

    #! Sessions

"""


@pytest.fixture
def test_session(session, test_user_participant1, test_user_participant2, test_study):
    session_data = [
        {
            "id": "session_test_1",
            "study_id": "study_test_org1",
            "participant_id": test_user_participant1["id"],
            "scheduled_time": "2023-01-01T10:00:00",
        },
        {
            "id": "session_test_2",
            "study_id": "study_test_org2",
            "participant_id": test_user_participant2["id"],
            "scheduled_time": "2023-01-01T10:00:00",
        },
    ]

    def create_session_model(sessions):
        return models.Session(**sessions)

    session_map = map(create_session_model, session_data)
    sessions = list(session_map)

    session.add_all(sessions)
    session.commit()

    sessions = session.query(models.Session).all()
    return sessions


"""
    #! Test users data
"""

"""
    #! Research Assistant
"""


@pytest.fixture
def test_user_research_assistant1(authorized_admin, test_organization):
    user_data = {
        "id": "assistant_test1",
        "email": "assistant_test1@gmail.com",
        "password": "123",
        "role": RoleEnum.research_assistant,
        "organization_id": "org1",
    }

    response = authorized_admin.post("/users/", json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user_research_assistant2(authorized_admin, test_organization):
    user_data = {
        "id": "assistant_test2",
        "email": "assistant_test2@gmail.com",
        "password": "123",
        "role": RoleEnum.research_assistant,
        "organization_id": "org2",
    }

    response = authorized_admin.post("/users/", json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


"""
    #! Study Coordinator
"""


@pytest.fixture
def test_user_coordinator1(authorized_admin, test_organization):
    user_data = {
        "id": "coordinator_test1",
        "email": "coordinator_test1@gmail.com",
        "password": "123",
        "role": RoleEnum.study_coordinator,
        "organization_id": test_organization[0].id,
    }

    response = authorized_admin.post("/users/", json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user_coordinator2(authorized_admin, test_organization):
    user_data = {
        "id": "coordinator_test2",
        "email": "coordinator_test2@gmail.com",
        "password": "123",
        "role": RoleEnum.study_coordinator,
        "organization_id": "org2",
    }

    response = authorized_admin.post("/users/", json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


"""
    #! Participant
"""


@pytest.fixture
def test_user_participant1(authorized_admin, test_organization):
    user_data = {
        "id": "participant_test1",
        "email": "participant_test1@gmail.com",
        "password": "123",
        "role": RoleEnum.participant,
        "organization_id": "org1",
    }

    response = authorized_admin.post("/users/", json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user_participant1_2(authorized_admin, test_organization):
    user_data = {
        "id": "participant_test1_2",
        "email": "participant_test1_2@gmail.com",
        "password": "123",
        "role": RoleEnum.participant,
        "organization_id": "org1",
    }

    response = authorized_admin.post("/users/", json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user_participant2(authorized_admin, test_organization):
    user_data = {
        "id": "participant_test2",
        "email": "participant_test2@gmail.com",
        "password": "123",
        "role": RoleEnum.participant,
        "organization_id": "org2",
    }

    response = authorized_admin.post("/users/", json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user_participant2_2(authorized_admin, test_organization):
    user_data = {
        "id": "participant_test2_2",
        "email": "participant_test2_2@gmail.com",
        "password": "123",
        "role": RoleEnum.participant,
        "organization_id": "org2",
    }

    response = authorized_admin.post("/users/", json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


def token(user_id: str):
    return create_access_token({"user_id": user_id})


@pytest.fixture
def authorized_client(client):
    def _authorized_client(user_id: str):
        user_token = token(user_id)
        fresh_client = TestClient(app)
        fresh_client.headers = {"Authorization": f"Bearer {user_token}"}

        return fresh_client

    return _authorized_client
# @pytest.fixture
# def authorized_participant1(client, test_user_participant1):
#     user_token = token(test_user_participant1["id"])
#     client.headers = {**client.headers, "Authorization": f"Bearer {user_token}"}

#     return client