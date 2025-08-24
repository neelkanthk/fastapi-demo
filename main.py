from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get('/')
def read_root():
    return JSONResponse(content="Posts API", status_code=status.HTTP_200_OK)


class Post:
    id: int
    title: str
    description: str
    author: str

    def __init__(self, title: str, description: str, author: str):
        self.id = int(posts[-1].id) + 1 if len(posts) > 0 else 1
        self.title = title
        self.description = description
        self.author = author


posts = list()


@app.get('/posts')
def index():
    return posts


class NewPostRequest(BaseModel):
    title: str
    description: str
    author: str


@app.post('/posts')
def save(payload: NewPostRequest):
    post = Post(payload.title, payload.description, payload.author)
    posts.append(post)
    return post


@app.get('/posts/{id}')
def show(id: int):
    for post in posts:
        if post.id == id:
            return post
    return JSONResponse(
        content={},
        status_code=status.HTTP_404_NOT_FOUND
    )


@app.delete('/posts/{id}')
def delete(id: int):
    for index, post in enumerate(posts):
        if post.id == id:
            posts.pop(index)
            return JSONResponse(
                content=f"Post {id} has been deleted.",
                status_code=status.HTTP_204_NO_CONTENT
            )
    return JSONResponse(
        content=None,
        status_code=status.HTTP_404_NOT_FOUND
    )


@app.put('/posts/{id}')
def update(id: int, payload: NewPostRequest):
    for index, post in enumerate(posts):
        if post.id == id:
            post.title = payload.title
            post.description = payload.description
            post.author = payload.author
            posts[index] = post
            return JSONResponse(content=f"Post {id} has been updated.", status_code=status.HTTP_200_OK)

    return JSONResponse(
        content=None,
        status_code=status.HTTP_404_NOT_FOUND
    )
