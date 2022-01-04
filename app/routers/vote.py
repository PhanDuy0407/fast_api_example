from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import oauth, schemas, models, utils
from ..database import engine, get_db


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_200_OK)
def vote_direction(vote: schemas.VoteIn, db: Session = Depends(get_db),
                   current_user: schemas.TokenData = Depends(oauth.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    results = db.query(models.Post).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
    print(results)
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    founded_vote = vote_query.first()

    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Post with id: {vote.post_id} not exist")
    #
    # if vote.vote_dir == 1:
    #     if founded_vote:
    #         raise HTTPException(status_code=status.HTTP_409_CONFLICT,
    #                             detail=f"User with id: {current_user.id} has already voted on post {vote.post_id}")
    #
    #     new_vote = models.Vote(user_id=current_user.id, **vote.dict())

    return {"a":"a"}