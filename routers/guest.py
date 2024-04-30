from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List , Optional
from schema import (
    RequestSchema,
    ResponseSchema,
    TokenResponse,
    UserSigupSchema,
    UserSiginSchema,
    Updatescheduleperiodstatus,
    Insertcustomerinterest
)
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from respository.web_repository import JWTRepo, JWTBearer,Ex_Decode
from passlib.context import CryptContext
from respository.repo_guest import BaseRepo

from model import (
     Users , 
     Sta_station ,
     Stat_customer,
     Sta_station_schedule,
     Stat_customer_action_detail,
     Stat_customer_interest
     

     )
from datetime import datetime, timedelta
import pdb
from minio_handler import MinioHandler
from minio import Minio


router = APIRouter(
              prefix="",
              tags=['guest'],
              responses ={404:{
                            'message' : "Not found"
              }}
              
)

