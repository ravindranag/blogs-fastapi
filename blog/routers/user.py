from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..hashing import Hash


router = APIRouter()


@router.post('/users/create', response_model=schemas.ShowUser, tags=['users'])
def create_new_user(request: schemas.User, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt(request.password)
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/users/{id}', response_model=schemas.ShowUserWithBlogs,tags=['users'])
def get_user_by_id(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user does not exist')
    return user