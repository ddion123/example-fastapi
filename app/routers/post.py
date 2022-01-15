from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
#from pydantic.main import ModelMetaclass
#from sqlalchemy.sql.functions import mode
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
            current_user: int = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0, search: Optional[str] = ""):
    ##cursor.execute("""SELECT * FROM posts """)
    ##posts = cursor.fetchall()
    #conn.commit()
    #cur.close()
    #conn.close()
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    #print(limit)

    #posts = db.query(models.Post).all()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

#def create_posts(payLoad: dict = Body(...)):
    #print (payLoad)
    #return {"new_post": f"title {payLoad['title']} content {payLoad['content']}"}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    #print (new_post.rating)
    #print(post)
    #print(post.dict())
    #post_dict = post.dict()
    #post_dict['id'] = randrange(3, 1000000)
    #my_posts.append(post_dict)

    ##cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) 
    ##RETURNING * """, (post.title, post.content, post.published))
    ##conn.commit()
    ##new_post = cursor.fetchone()
    
    #print(**post.dict())
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    

#title str, content str

#@app.get("/posts/latest")
#def get_latest_post():
#    post = my_posts[len(my_posts)-1]
#    return{"details": post}

#def get_post(id: int, response : Response):
    #print(id)
    #return{"post detail": f"here is the post {id}"}
    #print(type(id))

@router.get("/{id}", response_model=schemas.PostOut) #always return as a str
def get_post(id: int, db: Session = Depends(get_db), 
            current_user: int = Depends(oauth2.get_current_user)):
    ##cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    ##post = cursor.fetchone()
    #post = find_post(id)
    
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    #post = db.query(models.Post).filter(models.Post.id == id).filter(models.Post.owner_id == current_user.id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return{"message": f"post with id: {id} was not found"}

#    if post.owner_id != current_user.id:
#        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform this action")

    return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # delete post
    # find the index in the array of that id
    # my_posts.pop(id)
    #index = find_index_post(id)

    ##cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    ##deleted_post = cursor.fetchone()
    ##conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
   
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    #my_posts.pop(index)

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform this action")

    post_query.delete(synchronize_session=False)
    db.commit()

    #return{"message": "the post was successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_posts(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    #print(post)
    #index = find_index_post(id)

    ##cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s 
    ##WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    ##updated_post = cursor.fetchone()
    ##conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    #post_dict = post.dict()
    #post_dict['id'] = id
    #my_posts[index] = post_dict

    #post_query.update({'title' : 'title update', 'content' : 'content update'}, synchronize_session=False)

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform this action")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    ####no db.refresh(post_query)
    return post_query.first()


