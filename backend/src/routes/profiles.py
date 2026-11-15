from fastapi import APIRouter,Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.controllers.dependencies import current_user,writers
from src.models import ModelProfile
from src.schemas.profile import ProfileInput
from src.services.profiles import create_profile
from src.utils.serialize import row
router=APIRouter()
@router.get('/profiles')
def profiles(db:Session=Depends(get_db),user=Depends(current_user)):return [row(p) for p in db.scalars(select(ModelProfile).order_by(ModelProfile.id.desc()))]
@router.post('/profiles')
def create(data:ProfileInput,db:Session=Depends(get_db),user=Depends(writers)):return create_profile(db,data,user.email)
