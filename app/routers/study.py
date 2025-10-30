from typing import List

from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..utils import check_user_role
from ..database import get_db

router = APIRouter(tags=["Studies"])


@router.get("/studies", response_model=List[schemas.StudyOut])
def get_studies(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    user_role = current_user.role

    query = db.query(models.Study)

    if user_role == schemas.RoleEnum.admin:
        pass
    elif user_role in [
        schemas.RoleEnum.research_assistant,
        schemas.RoleEnum.study_coordinator,
    ]:
        query = query.filter(models.Study.organization_id == current_user.organization_id)
    elif user_role == schemas.RoleEnum.participant:
        query = query.join(
            models.Session, models.Study.id == models.Session.study_id
        ).filter(models.Study.organization_id == current_user.organization_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions!"
        )

    return query.all()


@router.get("/studies/{id}", response_model=schemas.StudyOut)
def get_study(
    id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    user_role = current_user.role

    query = db.query(models.Study).filter(models.Study.id == id)

    if user_role == schemas.RoleEnum.admin:
        pass
    elif user_role in [
        schemas.RoleEnum.research_assistant,
        schemas.RoleEnum.study_coordinator,
    ]:
        query = query.filter(models.Study.organization_id == current_user.organization_id)
    elif user_role == schemas.RoleEnum.participant:
        query = query.join(
            models.Session, models.Study.id == models.Session.study_id
        ).filter(models.Session.participant_id == current_user.id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions!"
        )

    study = query.first()

    if not study:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No study with the following id: {id}, was found!",
        )

    return study


@router.post(
    "/studies", status_code=status.HTTP_201_CREATED, response_model=schemas.StudyOut
)
def create_study(
    study_data: schemas.StudyCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    user_role = current_user.role

    if user_role not in [schemas.RoleEnum.admin, schemas.RoleEnum.study_coordinator]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions!"
        )
    if user_role == schemas.RoleEnum.study_coordinator and current_user.organization_id != study_data.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Current user is not part of this organization!",
        )

    new_study = models.Study(**study_data.model_dump())
    db.add(new_study)
    db.commit()
    db.refresh(new_study)

    return new_study


@router.delete("/studies/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_study(
    id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    check_user_role(current_user.role, schemas.RoleEnum.admin)

    query = db.query(models.Study).filter(models.Study.id == id)

    db_study = query.first()
    
    if not db_study:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No study with the following id: {id}, was found!",
        )

    query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/studies/{id}",
    response_model=schemas.StudyOut,
)
def update_study(
    id: str,
    study_data: schemas.StudyEdit,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    user_role = current_user.role
    
    query = db.query(models.Study).filter(models.Study.id == id)
    
    if user_role not in [schemas.RoleEnum.admin, schemas.RoleEnum.study_coordinator]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions!"
        )

    db_study = query.first()
    
    if not db_study:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No study with the following id: {id}, was found",
        )
    
    if user_role == schemas.RoleEnum.study_coordinator and current_user.organization_id != db_study.organization_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study not found!",
        )

    query.update(
        study_data.model_dump(exclude_none=True, exclude_unset=True),
        synchronize_session=False,
    )
    db.commit()

    return query.first()
