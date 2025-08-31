from typing import List
from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..utils import check_user_role
from ..database import get_db

router = APIRouter(tags=["Session"])

@router.get("/sessions", response_model=List[schemas.SessionOut])
def get_sessions(
    db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)
):

    user_role = current_user.role

    query = db.query(models.Session)

    if user_role == schemas.RoleEnum.admin:
        pass
    elif user_role in [
        schemas.RoleEnum.research_assistant,
        schemas.RoleEnum.study_coordinator,
    ]:
        query = query.join(
            models.Study, models.Session.study_id == models.Study.id
        ).filter(models.Study.org == current_user.org)
    elif user_role == schemas.RoleEnum.participant:
        query = query.filter(models.Session.participant_id == current_user.id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    return query.all()


@router.get("/sessions/{id}", response_model=schemas.SessionOut)
def get_session(
    id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):

    user_role = current_user.role

    query = db.query(models.Session).filter(models.Session.id == id)

    if user_role == schemas.RoleEnum.admin:
        pass
    elif user_role in [
        schemas.RoleEnum.research_assistant,
        schemas.RoleEnum.study_coordinator,
    ]:
        query = query.join(
            models.Study, models.Session.study_id == models.Study.id
        ).filter(models.Study.org == current_user.org)
    elif user_role == schemas.RoleEnum.participant:
        query = query.filter(models.Session.participant_id == current_user.id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    session = query.first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with the following id: {id}, does not exist",
        )

    return session


@router.post(
    "/sessions", status_code=status.HTTP_201_CREATED, response_model=schemas.SessionOut
)
def create_session(
    org: schemas.SessionCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):

    check_user_role(current_user.role, schemas.RoleEnum.admin)

    new_session = models.Session(**org.model_dump())
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session


@router.delete("/sessions/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_study(
    id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    check_user_role(current_user.role, schemas.RoleEnum.admin)

    session_query = db.query(models.Session).filter(models.Session.id == id)

    if session_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with the following id: {id}, does not exist",
        )

    session_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/sessions/{id}", response_model=schemas.SessionOut)
def update_study(
    id: str,
    org: schemas.SessionEdit,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):

    user_role = current_user.role

    query = db.query(models.Session).filter(models.Session.id == id)

    if user_role == schemas.RoleEnum.admin:
        pass
    elif user_role in [
        schemas.RoleEnum.research_assistant,
        schemas.RoleEnum.study_coordinator,
    ]:
        query = query.join(
            models.Study, models.Session.study_id == models.Study.id
        ).filter(models.Study.org == current_user.org)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    session = query.first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with the following id: {id}, does not exist",
        )

    db.query(models.Session).filter(models.Session.id == id).update(
        org.model_dump(exclude_none=True, exclude_unset=True), synchronize_session=False
    )

    db.commit()

    return session
