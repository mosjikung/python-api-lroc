from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List , Optional
from schema import (
    Updateowneruser,
    ResponseSchema

)
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from respository.repo_onairma import BaseRepo
from respository.repository import JWTRepo, JWTBearer, UsersRepo, Ex_Decode
from minio_handler import MinioHandler
from minio import Minio

from model import (
     Users, 
     Sta_station , 
     Sta_station_schedule,
     Sta_broadcast,
     Sta_station_schedule_user,
     Sta_station_period,
     Sta_period_status,
     Sta_station_period_user,
     Sta_station_activities,
     Sta_station_schedule_activitie
     )
from datetime import datetime, timedelta
import pdb

router = APIRouter(
              prefix="",
              tags=['onair_management'],
              responses ={404:{
                            'message' : "Not found"
              }}
              
)


@router.get("/get-all-period",dependencies=[Depends(JWTBearer())])
async def get_all_station_schedule_check(offset:Optional[int]=None,
                                         limit:Optional[int]=None,
                                         type:Optional[str]=None,
                                         order_direction:Optional[str]=None,
                                         keyword:Optional[str]=None,
                                         db: Session = Depends(get_db)):
     
     if type is None:
          type = 'onair'
     
     results = [] 
     results_dict = []
     count_type_1 = BaseRepo.count_type_1(db,
                                        Sta_station_schedule,
                                        Sta_station_period,
                                        Users)
     count_type_2 = BaseRepo.count_type_2(db,
                                        Sta_station_schedule,
                                        Sta_station_period,
                                        Users)
     count_type_3 = BaseRepo.count_type_3(db,
                                        Sta_station_schedule,
                                        Sta_station_period,
                                        Users)
     count_type_4 = BaseRepo.count_type_4(db,
                                        Sta_station_schedule,
                                        Sta_station_period,
                                        Users)
     station_schedule = BaseRepo.find_all_station_schedule(db,
                                                           Sta_station,
                                                           Sta_station_schedule,
                                                           Sta_station_period,
                                                           Users,
                                                           offset,
                                                           limit,
                                                           type,
                                                           order_direction,
                                                           keyword)
     station_schedule_count = BaseRepo.count_all_station_schedule(db,
                                                           Sta_station_schedule,
                                                           Sta_station_period,
                                                           Users,
                                                           type,
                                                           keyword)

     for item in station_schedule:
          bucket_name = 'stations'
          if item[2] is not None:
                
                object_name = item[2]
                url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
          else:
                url = None

          bucket_name2 = 'stations'
          if item[5] is not None:
                
                object_name2 = item[5]
                url2 = MinioHandler().get_instance().presigned_get_object(bucket_name2, object_name2)
          else:
                url2 = None
          results.append({
               'station_id':item[0],
               'station_name':item[1],
               'icon_path_station':url,
               'id':item[3],
               'schedule_number':item[4],
               'icon_path_schedule':url2,
               'schedule_name':item[6],
               'broadcast_status_id_str':item[7],
               'process_status_id_str':item[8],
               'schedule_date':item[9],
               'user_id':item[10],
               'first_name':item[11],
               'last_name':item[12],
               'time_min':item[13],
               'time_max':item[14],
               'period_id':item[15],
               'period_name':item[16],
               'broadcast_status_id':item[17],
               'period_status_id':item[18]
          })

          

     

     if type is None or type == '':
          results_dict=[{
            'count_onair':count_type_1,
            'count_edit':count_type_2,
            'count_send_edit':count_type_3,
            'count_close_edit':count_type_4,
            'data':results
        }]
     elif type == 'onair' and keyword is not None:
           results_dict=[{
            'count_onair':station_schedule_count,
            'count_edit':count_type_2,
            'count_send_edit':count_type_3,
            'count_close_edit':count_type_4,
            'data':results
        }] 
     elif type == 'edit' and keyword is not None:
          results_dict=[{
            'count_onair':count_type_1,
            'count_edit':station_schedule_count,
            'count_send_edit':count_type_3,
            'count_close_edit':count_type_4,
            'data':results
        }] 
     elif type == 'send_edit' and keyword is not None:
          results_dict=[{
            'count_onair':count_type_1,
            'count_edit':count_type_2,
            'count_send_edit':station_schedule_count,
            'count_close_edit':count_type_4,
            'data':results
        }] 
     elif type == 'close_edit' and keyword is not None:
          results_dict=[{
            'count_onair':count_type_1,
            'count_edit':count_type_2,
            'count_send_edit':count_type_3,
            'count_close_edit':station_schedule_count,
            'data':results
        }] 
     else:
          results_dict=[{
            'count_onair':count_type_1,
            'count_edit':count_type_2,
            'count_send_edit':count_type_3,
            'count_close_edit':count_type_4,
            'data':results
        }]
     
     return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=results_dict
     ).dict(exclude_none=True)

@router.post("/set-station-schedule-user" , dependencies=[Depends(JWTBearer())])

async def update_station_schedule_owner_user(request:Updateowneruser,token: str = Depends(JWTBearer()) , 
                                         db: Session = Depends(get_db)):
     decode_token = Ex_Decode.decode_token(token)
     user_id = decode_token["id"]
     is_delete = False
     update_time = datetime.now()
     update_user = BaseRepo.update_owner_user(db,
                                          request.schedule_id,
                                          user_id,
                                          update_time,
                                          Sta_station_schedule
                                        )
     inster_station_schedule_user = Sta_station_period_user(
          is_deleted =is_delete,
          created = update_time,
          created_by = user_id,
          station_schedule_id = request.id,
          station_period_id = request.schedule_id,
          user_id = user_id,
          process_status_id = 7
     )
     
     results  = BaseRepo.insert(db, inster_station_schedule_user)
     if update_user is not None:
          return ResponseSchema(
          code="200", status="Ok", message="Update Data Successfull"
          ).dict(exclude_none=True)

 
# @router.get("/get-detail-station-schedule-period")
# async def get_station_schedule_broadcast(id:Optional[int]=None,
#                                          db: Session = Depends(get_db)):
#     results_record = []
#     results = BaseRepo.get_data_schedule_period(db,Sta_station,Sta_station_schedule,Sta_station_period,id)
#     for item in results:
#         bucket_name = 'stations'
#         if item[1] is not None:
#                 object_name = item[1]
#                 url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
#         else:
#                 url = None


     
     
     

   
  