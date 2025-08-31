from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
from ..utils import check_user_role

router = APIRouter(tags=["user"])


@router.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    
    check_user_role(current_user.role, schemas.RoleEnum.admin)

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/users/{id}", response_model=schemas.UserOut)
def get_users(id: str, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    
    check_user_role(current_user.role, schemas.RoleEnum.admin)
    
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found!",
        )

    return user


@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: str, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    
    check_user_role(current_user.role, schemas.RoleEnum.admin)

    print("to delete user id: ", id)

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
    org: schemas.UserEdit,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):

    check_user_role(current_user.role, schemas.RoleEnum.admin)

    user_query = db.query(models.User).filter(models.User.id == id)

    print(user_query)

    db_user = user_query.first()

    print(db_user)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id {id} does not exist")

    user_query.update(
        org.model_dump(exclude_none=True, exclude_unset=True), synchronize_session=False
    )
    db.commit()

    return user_query.first()
