from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List , Optional
from schema import (
    RequestSchema,
    ResponseSchema,
    Createscheduletype,
    Updatescheduletype
)
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from respository.repository import JWTRepo, JWTBearer, UsersRepo, BaseRepo ,Ex_Decode
from respository.repodatastation import BaseRepo
from model import (Sta_schedule_catagorie,
                   Sta_period_categories,
                   Sta_station_period
                   )
from datetime import datetime, timedelta
import pdb


router = APIRouter(
              prefix="",
              tags=['Data Station Manage'],
              responses ={404:{
                            'message' : "Not found"
              }}
              
)

# encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@router.get("/get-all-station-schedule-type",dependencies=[Depends(JWTBearer())])
async def get_all_schedule_categoreis(offset:Optional[int]=None,
                                      limit:Optional[int]=None,
                                      order_direction:Optional[str]=None,
                                      keyword:Optional[str]=None,
                                      db: Session = Depends(get_db)):
    results = BaseRepo.get_all_schedule_catagories(db,Sta_period_categories,offset,limit,order_direction,keyword)
    results2 = BaseRepo.get_all_schedule_catagories_count(db,Sta_period_categories,offset,limit,order_direction,keyword)
    
    all_data_results1 = []
    last_results = []
    for x in results:
        results3 = BaseRepo.get_all_station_period_count(db,Sta_station_period,x.id)
        all_data_results1.append({
            'id':x.id,
            'name':x.name,
            'created':x.created,
            'description':x.description,
            'amount':results3
        })

    last_results = [
        {
            'count':results2,
            'data':all_data_results1,
           
        }
    ]

    return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=last_results
    )


@router.post("/create-station-schedule-type",dependencies=[Depends(JWTBearer())])
async def create_schedule_categories_type(request:Createscheduletype,token: str = Depends(JWTBearer()),
                                      db: Session = Depends(get_db)):
    update_time = datetime.now()
    decode_token = Ex_Decode.decode_token(token)
    user_id = decode_token["id"]
    schedule_categories = Sta_period_categories(
                    created=update_time,
                    created_by=user_id,
                    name=request.name,
                    description=request.description,
                    is_deleted = False
            )
    
    results = BaseRepo.insert(db,schedule_categories)
    return ResponseSchema(
              code="200", status="Ok", message="Insert Data Successfull"
              )


@router.put("/update-station-schedule-type",dependencies=[Depends(JWTBearer())])
async def update_station_schedule_types(request:Updatescheduletype,token: str = Depends(JWTBearer()),
                                      db: Session = Depends(get_db)):
    update_time = datetime.now()
    decode_token = Ex_Decode.decode_token(token)
    user_id = decode_token["id"]
    update_schedule_type = BaseRepo.update_station_schedule_type(db,
                                                        Sta_period_categories,
                                                        request.id,
                                                        update_time,
                                                        user_id,
                                                        request.name,
                                                        request.description)
    
    results = BaseRepo.update(db,update_schedule_type)
    return ResponseSchema(
              code="200", status="Ok", message="Update data Successfull"
              )

@router.delete("/delete-station-schedule-type",dependencies=[Depends(JWTBearer())])
async def delete_station_schedule_type(id:Optional[int] = None ,token: str = Depends(JWTBearer()),db: Session = Depends(get_db)):
    update_time = datetime.now()
    decode_token = Ex_Decode.decode_token(token)
    user_id = decode_token["id"]
    delete_data = BaseRepo.delete_station_schedule_type(db,
                                                        Sta_period_categories,
                                                        id,
                                                        user_id,
                                                        update_time)
    
    
    results = BaseRepo.update(db,delete_data)
    return ResponseSchema(
              code="200", status="Ok", message="Update staus Deleted"
              )
    

