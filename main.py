from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.get('/blogs')
def get_all_blogs(limit: int = 10, published: bool = True, sortby: Optional[str] = None):
    if published:
        return {
            'data': f'{limit} published blogs from db'
        }
    else:
        return {
            'data': f'{limit} blogs from db'
        }
    

@app.post('/blogs')
def create_new_blog(request: Blog):
    return {
        'data': 'blog created'
    }

    
@app.get('/blogs/unpublished')
def get_all_unpublished_blogs():
    # TODO get all unpublished blogs
    return {
        'data': 'all unpublished blogs'
    }
    
    
@app.get('/blogs/{id}')
def get_blog_by_id(id: int):
    return {
        'data': f'blog {id}'
    }
    
    
@app.get('/blogs/{id}/comments')
def get_comments_of_blog(id: int):
    # TODO fetch comments of blog
    return {
        'data': f'blog {id} comments'
    }