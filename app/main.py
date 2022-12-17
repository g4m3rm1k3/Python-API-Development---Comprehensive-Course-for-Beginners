from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import json
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None


while True:
    try:
        conn = psycopg2.connect(
            host='localhost', database='fastapi', user='postgres', password='N0th!ng1', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was sucessful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print(f"Error: {error}")
        time.sleep(2)


my_posts = [{"title": "title of post 1",
             "content": "Content of post 1", "id": 1}, {"title": "favourite foods", "content": "I like pizza", "id": 2}]


def find_post(id):
    # return [d for d in my_posts if d['id'] == id][0] or None
    for p in my_posts:
        if p["id"] == id:
            return p


@app.get("/")
async def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM post""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


# @app.post("/posts")
# def create_posts(post: Post):  # (payload: dict = Body(...)):
#     print(post)  # print(payload)
#     print(post.dict())
#     # "new_posts": f"title {payload['title']} content: {payload['content']}"}
#     return {"data": "new post"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = len(my_posts)+1
    my_posts.append(post_dict)
    return {"data": post_dict}
    # title str, content str


@app.post("/save-data")
def save_data(data: dict):
    # Save the data to a JSON file
    with open('data.json', 'w') as f:
        json.dump(data, f)

    return {"message": "Data saved successfully"}


@app.get("/load-data")
def load_data():
    # Load the data from the JSON file
    with open('data.json', 'r') as f:
        data = json.load(f)

    return data


@app.get("/posts/{id}")
def get_posts(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting posts
    global my_posts
    # [d for d in my_posts if d['id'] != id]
    my_posts = list(filter(lambda x: (x['id'] != id), my_posts))
    print(my_posts)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    print(post)
    global my_posts
    post_dict = post.dict()
    my_posts = list(filter(lambda x: (x['id'] != id), my_posts))
    post_dict['id'] = id
    my_posts.append(post_dict)
    return {"message": post_dict}
