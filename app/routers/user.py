from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db
from ..utils import check_user_role

router = APIRouter(tags=["user"])


@router.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: str, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    if id != current_user.id and current_user.role != schemas.RoleEnum.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Current user doesn't have enough permitions!")
    
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user with the following id: {id}, was found!",
        )

    return user


@router.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut
)
def create_user(user_data: schemas.UserCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    check_user_role(current_user.role, schemas.RoleEnum.admin)

    hashed_password = utils.hash(user_data.password)
    user_data.password = hashed_password
    
    new_user = models.User(**user_data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: str, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    if id == current_user.id:
        raise(HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="A user cannot delete itself! If you want to be removed, request it to an admin"))
    
    check_user_role(current_user.role, schemas.RoleEnum.admin)

    user_query = db.query(models.User).filter(models.User.id == id)

    if user_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist",
        )

    user_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/users/{id}", response_model=schemas.UserOut)
def update_user(
    id: str,
    user_data: schemas.UserEdit,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):

    check_user_role(current_user.role, schemas.RoleEnum.admin)

    user_query = db.query(models.User).filter(models.User.id == id)

    db_user = user_query.first()

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user with the following id: {id}, was found!")

    user_query.update(
        user_data.model_dump(exclude_none=True, exclude_unset=True), synchronize_session=False
    )
    db.commit()

    return user_query.first()
