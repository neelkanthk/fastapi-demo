from app import models, database
from app.schemas.requests import VoteRequest
from app.schemas.responses import PostResponse
from sqlalchemy.orm import Session
from fastapi import status, Depends, HTTPException, APIRouter
import app.utils as utils

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(payload: VoteRequest, db: Session = Depends(database.get_db), logged_in_user=Depends(utils.get_current_user)):
    user_id = logged_in_user.id
    post_id = payload.post_id
    vote_dir = payload.direction
    vote_exists = db.query(models.Vote).filter(models.Vote.post_id == post_id, models.Vote.user_id == user_id).first()

    if vote_dir == 0:
        if not vote_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote not found.")
        db.query(models.Vote).filter(models.Vote.user_id == user_id, models.Vote.post_id == post_id).delete()
        db.commit()
    else:
        new_vote = models.Vote()
        new_vote.user_id = user_id
        new_vote.post_id = post_id
        db.add(new_vote)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in saving vote.")

    # calculate vote count
    vote_count = db.query(models.Vote).filter(models.Vote.post_id == post_id).count()
    return dict({"post_id": post_id, "vote_count": vote_count})
