from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List , Optional
from schema import (
    RequestSchema,
    ResponseSchema,
    TokenResponse,
    UserSigupSchema,
    UserSiginSchema,
)
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from respository.repository import JWTRepo, JWTBearer, UsersRepo, BaseRepo

from model import (
     Users , 
     Sta_period_types ,
     Sta_categories , 
     Sta_station , 
     Sta_station_schedule,
     Sta_audit_statuses,
     Sta_process_statuses,
     Sta_broadcast_statuses,
     Sta_period_times,
     Sta_station_statuses
     )
from datetime import datetime, timedelta
import pdb
import json


router = APIRouter()

# encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""
    Authentication Router
"""




"""
    Users Router
"""


@router.get("/getstation")
async def retrieve_all(db: Session = Depends(get_db)):
    station = UsersRepo.retrieve_all(db,Sta_station)
    return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=station

    )



@router.get("/Join_3_table_station/{offset}/{limit}")
async def all_3_table_limit(offset:int , limit:int , keyword:Optional[str] = None ,  db: Session = Depends(get_db)):
    results = BaseRepo.join_3_table_limit(db,Sta_station_schedule, Sta_station ,Sta_categories , Sta_station_statuses , offset , limit, keyword)

    results_dict =[]
    for sta_station_schedules, sta_stations, sta_categories , sta_station_statuses  in results:
            results_dict.append({
                'name_schedule':sta_station_schedules.name,
                'schedule_time':sta_station_schedules.schedule_time,
                'station_id':sta_stations.id,
                'station_name':sta_stations.name,
                'category_name':sta_categories.name,
                'code':sta_stations.code,
                'status_station':sta_station_statuses.name
            })

    
    return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=results_dict 
    ).dict(exclude_none=True)

