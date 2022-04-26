from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import models, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blogs', status_code=status.HTTP_201_CREATED)
def create_new_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title = request.title,
        body = request.body,
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blogs', response_model=List[schemas.ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
    all_blogs = db.query(models.Blog).all()
    return all_blogs



@app.get('/blogs/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_blog_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='Blog does not exist')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {
        #     'message': 'Blog not found'
        # }
        
    return blog


@app.delete('/blogs/{id}', status_code= status.HTTP_200_OK)
def delete_blog_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog {id} does not exist')
    
    blog.delete(synchronize_session=False)
    db.commit()
    return {
        'message': f'Blog {id} deleted successfully'
    }
    
@app.put('/blogs/{id}')
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    try:
        blog = db.query(models.Blog).filter(models.Blog.id == id)
        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog {id} does noy exist')
        blog.update(request.dict())
        db.commit()
        return {
            'detail': {
                'msg': 'updated'
            }
        }
    except Exception as err:
        print(err)
        return 'error'
    
    
@app.post('/users/create')
def create_new_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=request.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user