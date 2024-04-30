from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List , Optional
from schema import (
    RequestSchema,
    ResponseSchema,
    TokenResponse,
    UserSigupSchema,
    UserSiginSchema,
    Updatescheduleperiodstatus
)
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from respository.repository import JWTRepo, JWTBearer, UsersRepo ,Ex_Decode
from passlib.context import CryptContext
from respository.repobroadcast import BaseRepo

from model import (
     Users , 
     Sta_station , 
     Sta_station_schedule,
     Sta_broadcast,
     Sta_station_period,
     Sta_station_playlist,
     Sta_station_schedule_activitie
     

     )
from datetime import datetime, timedelta
import pdb
from minio_handler import MinioHandler
from minio import Minio


router = APIRouter(
              prefix="",
              tags=['broadcast'],
              responses ={404:{
                            'message' : "Not found"
              }}
              
)


# encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""
    Authentication Router
"""


@router.get("/get-station-schedule-broadcast")
async def get_station_schedule_broadcast(offset:Optional[str]=None,
                                         limit:Optional[int]=None,
                                         keyword:Optional[str]=None,
                                         order_direction:Optional[str]=None,
                                         db: Session = Depends(get_db)):
    results_record = []
    results_last=[]
    results = BaseRepo.get_data_broadcast(db,Sta_station,Sta_station_schedule,Sta_station_period,offset,limit,order_direction,keyword)
    results2 = BaseRepo.get_count_data_broadcast(db,Sta_station,Sta_station_schedule,Sta_station_period,offset,limit,order_direction,keyword)

    for item in results:
        bucket_name = 'stations'
        if item[1] is not None:
                object_name = item[1]
                url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
        else:
                url = None

        object_name2 = item[12]
        bucket_name2 = 'stations'
        if item[12] is not None:
                object_name2 = item[12]
                url2 = MinioHandler().get_instance().presigned_get_object(bucket_name2, object_name2)
        else:
                url2 = None


        
        results_record.append({
             'id':item[0],
             'station_icon_path':url,
             'name':item[2],
             'is_enabled':item[3],
             'suspend_comment':item[4],
             'suspend_date_start':item[5],
             'suspend_date_end':item[6],
             'disable_comment':item[7],
             'schedule_station_id':item[8],
             'schedule_date':item[9],
             'schedule_id':item[11],
             'schedule_number':item[12],
             'schedule_icon_path':url2,
             'schedule_count_like':item[14],
             'schedule_count_share':item[15],
             'schedule_count_play':item[16],
             'schedule_count_comment':item[17],
             'time_min':item[18],
             'time_max':item[19],
             'last_check':item[20],
             'broadcast_status_id':item[21],
             'broadcast_type_id':item[22]
            

        })
        results_last= [
              {
              'count_query':results2,
              'data':results_record
              }
              

        ]
        
    return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=results_last
    ).dict(exclude_none=True)

@router.get("/get-detail-station-schedule-broadcast-old",dependencies=[Depends(JWTBearer())])
async def get_detail_station_schedule_broadcast(id:Optional[int]=None,db: Session = Depends(get_db)):
    get_data_station_schedule = BaseRepo.get_data_schedule_x(db,
                                                           id,
                                                           Sta_station_schedule)

    

    sta_station_id = get_data_station_schedule[0].station_id

    get_data_station = BaseRepo.get_data_station(db,
                                                 sta_station_id,
                                                 Sta_station)
    data_station = {}
    for sta_stations in get_data_station:
        
        data_station = {
            'id':sta_stations.id,
            'name':sta_stations.name,
            'icon_path':sta_stations.icon_path,
            'count_like':sta_stations.count_like,
            'count_share':sta_stations.count_share,
            'count_listen':sta_stations.count_listen
        }

    
    get_data_periods = BaseRepo.get_data_period(db,
                                               id,
                                               Sta_station_period)
    
    all_get_data_period={}
    get_data_period = []
    for sta_station_periods in get_data_periods:
        
        get_data_period.append({
            'id':sta_station_periods.id,
            'name':sta_station_periods.name,
            'period_status_id':sta_station_periods.period_status_id,
            'icon_path':sta_station_periods.icon_path,
            'period_time_start':sta_station_periods.period_time_start,
            'period_time_end':sta_station_periods.period_time_end,
            'broadcast_url':sta_station_periods.broadcast_url
        })
        data_period_id = sta_station_periods.id

    
    
    last_results = {
        'id':get_data_station_schedule[0].id,
        'broadcast_status_id':get_data_station_schedule[0].broadcast_status_id,
        'schedule_date':get_data_station_schedule[0].schedule_date,
        'schedule_time_start':get_data_station_schedule[0].schedule_time_start,
        'schedule_time_end':get_data_station_schedule[0].schedule_time_end,
        'broadcast_url':get_data_station_schedule[0].broadcast_url,
        'station':data_station,
        'period':get_data_period,
        
    }

    return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=last_results
    ).dict(exclude_none=True)


@router.delete("/delete-station-schedule-broadcast",dependencies=[Depends(JWTBearer())])
async def get_detail_station_schedule_broadcast(id:Optional[int]=None,token: str = Depends(JWTBearer()),db: Session = Depends(get_db)):
    decode_token = Ex_Decode.decode_token(token)
    user_id = decode_token["id"]
    update_time = datetime.now()
    delete_station_broadcast = BaseRepo.delete_schedule_broadcast(db,
                                                         id,
                                                         user_id,
                                                         update_time,
                                                         Sta_station_schedule
                                                         )
    results = BaseRepo.update(db,delete_station_broadcast)

    delete_station_period = BaseRepo.delete_schedule_period(db,
                                                         id,
                                                         user_id,
                                                         update_time,
                                                         Sta_station_period
                                                         )
    results = BaseRepo.update(db,delete_station_period)

    return ResponseSchema(
        code="200", status="Ok", message="Update data Successfull"
    ).dict(exclude_none=True)


@router.get("/get-broadcast-schedule-main-by-id",dependencies=[Depends(JWTBearer())])
async def get_detail_station_schedule_broadcast(id:Optional[int]=None,db: Session = Depends(get_db)):
    get_data_station_schedule = BaseRepo.get_data_schedule(db,
                                                           Sta_station_schedule,
                                                           Sta_station_period,
                                                           id
                                                           )
    results_all = []
    for sta_station_schedules , sta_station_periods in get_data_station_schedule:
         results_all.append({
              'time_start':sta_station_periods.period_time_start,
              'time_end':sta_station_periods.period_time_end,
              'period_name':sta_station_periods.name,
              'broadcast_url':sta_station_periods.broadcast_url,
              'broadcast_status_id':sta_station_periods.broadcast_status_id,
              'broadcast_type_id':sta_station_periods.broadcast_type_id
              
         })
    

    return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=results_all
    ).dict(exclude_none=True)



@router.get("/get-detail-station-schedule-broadcast",dependencies=[Depends(JWTBearer())])
async def get_station_schedule_broadcast(id:Optional[int]=None,
                                         db: Session = Depends(get_db)):
    results_record = []
    results = BaseRepo.get_data_schedule_broadcast(db,Sta_station,Sta_station_schedule,Sta_station_period,id)
    for item in results:
        bucket_name = 'stations'
        if item[1] is not None:
                object_name = item[1]
                url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
        else:
                url = None


        results_record.append({
             'id':item[0],
             'station_icon_path':url,
             'name':item[2],
             'station_count_like':item[3],
             'station_count_share':item[4],
             'station_count_listen':item[5],
             'station_count_comment':item[6],
             'schedule_broadcast_url':item[7],
             'schedule_schedule_date':item[8],
             'schedule_broadcast_status_id':item[9],
             'time_min':item[11],
             'time_max':item[12]


        })
        
    return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=results_record
    ).dict(exclude_none=True)

    
dependencies=[Depends(JWTBearer())]
    

    


@router.patch("/update-schedule-period-status-id",dependencies=[Depends(JWTBearer())])
async def get_all_summary_dashboard(request:Updatescheduleperiodstatus,
                                    token: str = Depends(JWTBearer()),
                                    db: Session = Depends(get_db)):

    time_update = datetime.now()
    decode_token = Ex_Decode.decode_token(token)
    user_id = decode_token["id"]



    check_station_schedule = BaseRepo.check_station(db,
                                           Sta_station_schedule,
                                           request.id,
                                           request.broadcast_status_id,
                                           user_id,
                                           time_update)
    
    
    try:
            results_update = BaseRepo.update(db,check_station_schedule)
    except Exception as e:
            results_update = db.rollback()
    
    if results_update == True:
          insert_suspend = Sta_station_schedule_activitie(
                                                        is_deleted = False,
                                                        created=time_update,
                                                        created_by=user_id,
                                                        name="ระงับการใช้งาน",
                                                        description="รายการ" + ' ' + str(check_station_schedule.name),
                                                        reference_id = request.id,
                                                        station_schedule_id = check_station_schedule.id,
                                                        object = "station_schedules",
                                                        type_user = "users",
                    
                                                )
          results_insert = BaseRepo.insert(db,insert_suspend)



    get_all_data_check_period = BaseRepo.get_all_data_check_period(db,
                                                                   Sta_station_period,
                                                                   request.id)
    
    for x in get_all_data_check_period:
        check_period = BaseRepo.check_period(db,
                                            Sta_station_period,
                                            x.id,
                                            request.broadcast_status_id,
                                            user_id,
                                            time_update)
        
        
        try:
            results_update = BaseRepo.update(db,check_period)
        except Exception as e:
            results_update = db.rollback()

        if results_update == True:
          insert_suspend = Sta_station_schedule_activitie(
                                                        is_deleted = False,
                                                        created=time_update,
                                                        created_by=user_id,
                                                        name="ระงับการใช้งาน",
                                                        description="รายการ" + ' ' + str(check_period.name),
                                                        reference_id = request.id,
                                                        station_schedule_id = check_period.station_schedule_id,
                                                        object = "station_periods",
                                                        type_user = "users",
                    
                                                )
          results_insert = BaseRepo.insert(db,insert_suspend)


    if check_station_schedule is None:
         return ResponseSchema(
         code="200", status="Ok", message="ID Station not found"
         ).dict(exclude_none=True)
    
    elif check_period is None:
         return ResponseSchema(
         code="200", status="Ok", message="ID Period not found"
         ).dict(exclude_none=True)
    
    else:
         return ResponseSchema(
         code="200", status="Ok", message="Update Successfull!!"
         ).dict(exclude_none=True)
    

    

