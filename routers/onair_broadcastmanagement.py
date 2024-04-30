from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List , Optional
from respository.repository import JWTRepo, JWTBearer, UsersRepo ,Ex_Decode
from schema import (
    Updateowneruser,
    ResponseSchema,
    Updatesetperioduser
    

)
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from respository.repo_onairbroadcastma import BaseRepo
from minio_handler import MinioHandler

from model import (
     Users, 
     Sta_station , 
     Sta_station_schedule,
     Sta_broadcast,
     Sta_broadcast_history_status,
     Sta_station_activities,
     Sta_station_schedule_activitie,
     Member,
     Sta_station_period

     )
from datetime import datetime, timedelta
import pdb

router = APIRouter(
              prefix="",
              tags=['onair_broadcast_management'],
              responses ={404:{
                            'message' : "Not found"
              }}
              
)


@router.get("/get-all-station-broadcast-manage",dependencies=[Depends(JWTBearer())])
async def get_all_station_schedule_check(offset:Optional[int]=None,
                                         limit:Optional[int]=None,
                                         type:Optional[str]=None,
                                         order_direction:Optional[str]=None,
                                         keyword:Optional[str]=None,
                                         db: Session = Depends(get_db)):
     
     results = [] 
     results_dict = []
     count_type_1 = BaseRepo.count_type_1(db,Sta_station,Sta_station_schedule,Member)
     count_type_2 = BaseRepo.count_type_2(db,Sta_station,Sta_station_schedule,Member)
     count_type_3 = BaseRepo.count_type_3(db,Sta_station,Sta_station_schedule,Member)
     count_type_4 = BaseRepo.count_type_4(db,Sta_station,Sta_station_schedule,Member)
     station_schedule = BaseRepo.find_all_station_schedule(db,Sta_station,Sta_station_schedule,Member,offset,limit,type,order_direction,keyword)

     station_schedule_count = BaseRepo.count_all_station_schedule(db,Sta_station,Sta_station_schedule,Member,offset,limit,type,order_direction,keyword)
     if type is None:
          type = 'total'

     for sta_stations,sta_station_schedules,members in station_schedule:

          object_name = sta_station_schedules.object_key
          bucket_name = 'stations'
          if sta_station_schedules.object_key is not None:
                object_name = sta_station_schedules.object_key
                url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
          else:
                url = None

          bucket_name2 = 'stations'
          if sta_stations.object_key is not None:
                object_name2 = sta_stations.object_key
                url2 = MinioHandler().get_instance().presigned_get_object(bucket_name2, object_name2)
          else:
                url2 = None
          results.append({
               'schedule_id':sta_station_schedules.id,
               'schedule_name':sta_station_schedules.name,
               'schedule_number':sta_station_schedules.schedule_number,
               'schedule_date':sta_station_schedules.schedule_date,
               'station_name':sta_stations.name,
               'schedule_broadcast_status_id':sta_station_schedules.broadcast_status_id,
               'broadcast_url':sta_station_schedules.broadcast_url,
               'code':sta_stations.code,
               'modified':sta_station_schedules.modified,
               'icon_path_schedule':url,
               'icon_path_station':url2,
               'status':type,
               'member_username':members.username,
               'member_name':str(members.first_name) + ' ' +  str(members.last_name)
          })

     if type is None or type == 'total' and keyword is None:
          print("Chose this")
          results_dict=[{
            'count_total':count_type_1,
            'count_onair':count_type_2,
            'count_waiting':count_type_3,
            'count_history':count_type_4,
            'data':results
        }]
          
     elif type == 'total' and keyword is not None:
          results_dict=[{
            'count_total':station_schedule_count,
            'count_onair':count_type_2,
            'count_waiting':count_type_3,
            'count_history':count_type_4,
            'data':results
        }]
     
     elif type == 'onair' and keyword is not None:
          results_dict=[{
            'count_total':count_type_1,
            'count_onair':station_schedule_count,
            'count_waiting':count_type_3,
            'count_history':count_type_4,
            'data':results
        }]
     
     elif type == 'waiting' and keyword is not None:
          results_dict=[{
            'count_total':count_type_1,
            'count_onair':count_type_2,
            'count_waiting':station_schedule_count,
            'count_history':count_type_4,
            'data':results
        }]
     
     elif type == 'history' and keyword is not None:
          results_dict=[{
            'count_total':count_type_1,
            'count_onair':count_type_2,
            'count_waiting':count_type_3,
            'count_history':station_schedule_count,
            'data':results
        }]
     else:
          results_dict=[{
            'count_total':count_type_1,
            'count_onair':count_type_2,
            'count_waiting':count_type_3,
            'count_history':count_type_4,
            'data':results
        }]
          
     
     return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=results_dict
     ).dict(exclude_none=True)
     
   

@router.get("/get-schedule-activity-by-id",dependencies=[Depends(JWTBearer())])
async def get_schedule_activity(id:Optional[int]=None,
                                object:Optional[str]=None,
                               db: Session = Depends(get_db)):
     
     results = BaseRepo.get_schedule_activity(db,
                                              Sta_station_schedule_activitie,
                                              Member,
                                              Users,
                                              id,
                                              object)
     
     results_dict = []

     for item in results:
          if item[11] == 'members':
               object_name = item[9]
               
               bucket_name = 'member'
               if item[9] is not None:
                object_name = item[9]
                url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
               else:
                url = None
          else:
               object_name = item[10]
               bucket_name = 'member'
               if item[10] is not None:
                object_name = item[10]
                url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
               else:
                url = None
          results_dict.append({
               'id':item[0],
               'created':item[1],
               'first_name':item[2],
               'last_name':item[3],
               'name':item[4],
               'description':item[5],
               'created_by':item[6],
               'type_user':item[7],
               'status_id':item[8],
               'avatar_img':url
          })
          
     
     return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=results_dict
     ).dict(exclude_none=True)


@router.post("/set-period-user-by-id",dependencies=[Depends(JWTBearer())])
async def set_period_user_by_id(request:Updatesetperioduser,
                               token: str = Depends(JWTBearer()),
                               db: Session = Depends(get_db)):
    time_update = datetime.now()
    decode_token = Ex_Decode.decode_token(token)
    user_id = decode_token["id"]

    results = BaseRepo.update_period_user(db,
                                          Sta_station_period,
                                          user_id,
                                          request.id,
                                          time_update)
    
    

    try:
            results_update = BaseRepo.update(db,results)
    except Exception as e:
            results_update = db.rollback()

    icon = "icon-clock.svg"
    if results_update  == True :
          insert_suspend = Sta_station_schedule_activitie(
                                                                 is_deleted = False,
                                                                 created=time_update,
                                                                 created_by=user_id,
                                                                 name="ตรวจสอบ",
                                                                 description="รายการ" + ' ' + str(results.name),
                                                                 reference_id = request.id,
                                                                 station_schedule_id = results.station_schedule_id,
                                                                 object = "station_periods",
                                                                 icon = icon,
                                                                 type_user = "users",
                                                                 type_activity = "examine"
                              
                                                       )
          results_insert = BaseRepo.insert(db,insert_suspend)

    return ResponseSchema(
        code="200", status="Ok", message="Update Success"
     ).dict(exclude_none=True)



@router.get("/get-schedule-activity-onair-by-id",dependencies=[Depends(JWTBearer())])
async def get_schedule_activity(id:Optional[int]=None,
                               db: Session = Depends(get_db)):
     
     results = BaseRepo.get_schedule_activity_onair(db,
                                              Sta_station_schedule_activitie,
                                              Member,
                                              Users,
                                              id)
     
     results_dict = []

     for item in results:
          if item[11] == 'members':
               object_name = item[9]
               
               bucket_name = 'member'
               if item[9] is not None:
                object_name = item[9]
                url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
               else:
                url = None
          else:
               object_name = item[10]
               bucket_name = 'member'
               if item[10] is not None:
                object_name = item[10]
                url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
               else:
                url = None
          results_dict.append({
               'id':item[0],
               'created':item[1],
               'first_name':item[2],
               'last_name':item[3],
               'name':item[4],
               'description':item[5],
               'created_by':item[6],
               'type_user':item[7],
               'status_id':item[8],
               'avatar_img':url
          })
          
     
     return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=results_dict
     ).dict(exclude_none=True)






   
  