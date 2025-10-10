import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import schemas
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
    
    org1 = models.Organization(
        id = "org1",
        name = "Organization1"
    )
    
    org2 = models.Organization(
        id = "org2",
        name = "Organization1"
    )
    sysadmin.password = utils.hash(sysadmin.password)
    session.add_all([sysadmin, org1, org2])
    session.commit()
    
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


"""
    #! Test users data
"""


"""
    #! Research Assistant
"""


@pytest.fixture
def test_user_research_assistant1(client):
    user_data = {
        "id": "assistant_test1",
        "email": "assistant_test1@gmail.com",
        "password": "123",
        "role": RoleEnum.research_assistant,
        "organization_id": "org1",
    }

    response = client.post("/users/", json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user_research_assistant2(client):
    user_data = {
        "id": "assistant_test2",
        "email": "assistant_test2@gmail.com",
        "password": "123",
        "role": RoleEnum.research_assistant,
        "organization_id": "org2",
    }

    response = client.post("/users/", json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


"""
    #! Study Coordinator
"""


@pytest.fixture
def test_user_coordinator1(client):
    user_data = {
        "id": "coordinator_test1",
        "email": "coordinator_test1@gmail.com",
        "password": "123",
        "role": RoleEnum.study_coordinator,
        "organization_id": "org1",
    }

    response = client.post("/users/", json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user_coordinator2(client):
    user_data = {
        "id": "coordinator_test2",
        "email": "coordinator_test2@gmail.com",
        "password": "123",
        "role": RoleEnum.study_coordinator,
        "organization_id": "org2",
    }

    response = client.post("/users/", json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


"""
    #! Participant
"""


@pytest.fixture
def test_user_participant1(client):
    user_data = {
        "id": "participant_test1",
        "email": "participant_test1@gmail.com",
        "password": "123",
        "role": RoleEnum.participant,
        "organization_id": "org1",
    }

    response = client.post("/users/", json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user_participant2(client):
    user_data = {
        "id": "participant_test2",
        "email": "participant_test2@gmail.com",
        "password": "123",
        "role": RoleEnum.participant,
        "organization_id": "org2",
    }

    response = client.post("/users/", json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


"""
    Token
"""

@pytest.fixture
def authorized_admin(client):
    response = client.post(
        "/login", data={"username": "sysadmin_test", "password": "123"}
    )

    login_response = schemas.Token(**response.json())
    return login_response.access_token

@pytest.fixture
def token():
    return create_access_token({"user_id": "sysadmin"})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client


@pytest.fixture
def test_study(session):
    study_data = [
        {
            "id": "study_test_1",
            "title": "Study test org 1",
            "description": "description test",
            "organization": "org1",
        },
        {
            "id": "study_test_2",
            "title": "Study test org 2",
            "description": "description test",
            "organization": "org2",
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


@pytest.fixture
def test_session(session, test_user_participant1, test_user_participant2):
    session_data = [
        {
            "id": "session_test_1",
            "study_id": "study_test_1",
            "participant_id": test_user_participant1["id"],
            "scheduled_time": "01-01-2000",
        },
        {
            "id": "session_test_2",
            "study_id": "study_test_2",
            "participant_id": test_user_participant2["id"],
            "scheduled_time": "01-01-2000",
        },
    ]

    def create_session_model(session):
        return models.Session(**session)

    session_map = map(create_session_model, session_data)
    sessions = list(session_map)

    session.add_all(sessions)
    session.commit()

    sessions = session.query(models.Session).all()
    return sessions
