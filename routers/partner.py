from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List , Optional
from schema import (
    RequestSchema,
    ResponseSchema,

)
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from respository.web_repository import JWTRepo, JWTBearer,Ex_Decode
from passlib.context import CryptContext
from respository.repo_partner import BaseRepo

from model import (
     Sta_partner
    
     )
from datetime import datetime, timedelta
import pdb
from minio_handler import MinioHandler
from minio import Minio


router = APIRouter(
              prefix="",
              tags=['partner'],
              responses ={404:{
                            'message' : "Not found"
              }}
              
)


@router.get("/get-all-partner-web")
async def get_all_partner_web(db: Session = Depends(get_db)):
              get_data_partner = BaseRepo.get_data_partner(db,
                                                           Sta_partner)
              
              results = []
              for sta_partners in get_data_partner:
                      results.append({
                            'id':sta_partners.id,
                            'name':sta_partners.name,
                            'icon_path':sta_partners.icon_path,
                            'object_ket':sta_partners.object_key,
                            'sort':sta_partners.sort
      
                      })

              return ResponseSchema(
                code="200", status="Ok", message="foundData" ,result=results
                ).dict(exclude_none=True)



               