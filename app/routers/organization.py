from typing import List
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..utils import check_user_role
from ..database import get_db

router = APIRouter(tags=["Orgs"])

@router.get("/organizations", response_model=List[schemas.Organization])
def get_orgs(
    db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)
):
    check_user_role(current_user.role, schemas.RoleEnum.admin)
    orgs = db.query(models.Organization).all()

    return orgs


@router.get("/organizations/{id}", response_model=schemas.Organization)
def get_org(
    id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    check_user_role(current_user.role, schemas.RoleEnum.admin)
    org = db.query(models.Organization).filter(models.Organization.id == id).first()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No organization with the following id: {id}, was found!",
        )

    return org


@router.post(
    "/organizations",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Organization,
)
def create_org(
    org: schemas.OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):

    check_user_role(current_user.role, schemas.RoleEnum.admin)

    new_org = models.Organization(**org.model_dump())
    db.add(new_org)
    db.commit()
    db.refresh(new_org)

    return new_org


@router.put(
    "/organizations/{id}",
    response_model=schemas.Organization,
)
def update_org(
    id: str,
    org_data: schemas.OrganizationEdit,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):

    check_user_role(current_user.role, schemas.RoleEnum.admin)

    org_query = db.query(models.Organization).filter(models.Organization.id == id)

    db_org = org_query.first()

    if db_org is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No organization with the following id: {id}, was found!"
        )

    org_query.update(org_data.model_dump(), synchronize_session=False)
    db.commit()

    return org_query.first()
