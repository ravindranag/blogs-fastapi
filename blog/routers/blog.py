from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from..database import get_db

router = APIRouter()


@router.get('/blogs', response_model=List[schemas.ShowBlog], tags=['blogs'])
def get_all_blogs(db: Session = Depends(get_db)):
    all_blogs = db.query(models.Blog).all()
    return all_blogs

@router.post('/blogs', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create_new_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title = request.title,
        body = request.body,
        user_id = 1
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog




@router.get('/blogs/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['blogs'])
def get_blog_by_id(id: int, db: Session = Depends(get_db)):
    
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='Blog does not exist')
        
    return blog


@router.delete('/blogs/{id}', status_code= status.HTTP_200_OK, tags=['blogs'])
def delete_blog_by_id(id: int, db: Session = Depends(get_db), tags=['blogs']):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog {id} does not exist')
    
    blog.delete(synchronize_session=False)
    db.commit()
    return {
        'message': f'Blog {id} deleted successfully'
    }
    
@router.put('/blogs/{id}', tags=['blogs'])
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog {id} does noy exist')
    blog.update(request.dict())
    db.commit()
    return {
        'detail': {
            'msg': 'updated'
        }
    }