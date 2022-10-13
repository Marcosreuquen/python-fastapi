from .. import schemas, models, oauth2
from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from uuid import UUID
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = "",
):
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(offset)
        .all()
    )
    return results


@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(id: UUID, response: Response, db: Session = Depends(get_db)):
    # cursor.execute(sql.SQL("""SELECT * FROM posts WHERE id = %s """), [id])
    # post = cursor.fetchone()
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} was not found"
        )
    return post


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
async def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    new_post.owner_id = user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: UUID,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     sql.SQL("""DELETE FROM posts WHERE id = %s returning *"""), [id])
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} does not exist"
        )

    if post.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(
    id: UUID,
    data: schemas.PostCreate,
    db: Session = Depends(
        get_db,
    ),
    user: models.User = Depends(oauth2.get_current_user),
):
    # cursor.execute(sql.SQL("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *"""), [
    #                post.title, post.content, post.published, id])
    # updated_post = cursor.fetchone()
    # conn.commit()
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} does not exist"
        )
    if post.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    query.update(data.dict(), synchronize_session=False)
    db.commit()
    return query.first()
