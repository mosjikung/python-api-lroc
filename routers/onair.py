from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List , Optional
from schema import (
    RequestSchema,
    ResponseSchema,
    TokenResponse,
    UserSigupSchema,
    UserSiginSchema,
    Insertplaylistactivity,
    Insertplaylistcomment,
    Insertstationmember,
    Deleteactivity,
    Updateprocessstatus,
    Findperiod,
    Updateperiodstatusid
)
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from respository.repository import JWTRepo, JWTBearer, UsersRepo ,Ex_Decode
from respository.repo_onair import BaseRepo

from model import (
     Users ,
     Member,
     Sta_station ,
     Sta_station_schedule,

     Sta_station_schedule_user,
     Sta_station_playlist_activities,
     Sta_station_playlist_comments,
     Sta_station_period,
     Sta_station_playlist,
     Sta_station_schedule_activitie,
     Sta_station_playlist_history
     )
from datetime import datetime, timedelta
import pdb

from minio_handler import MinioHandler
from minio import Minio



router = APIRouter(
              prefix="",
              tags=['onair'],
              responses ={404:{
                            'message' : "Not found"
              }}

)


# encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""
    Authentication Router
"""
def check_type_value(val1,val2):
      if val1 is not None and val2 is None:
                   results = 'users'
      if val1 is None and val2 is not None:
                  results = 'members'
      if val1 is None and val2 is None:
                   results = 'Not found Data'
      
      return results


# @router.get("/set-station-schedule-user",)
# async def get_all_station_schedule_user(db: Session = Depends(get_db)):
#      _station_user = UsersRepo.get_data_station_user(db, Sta_station_schedule_user)


#      return ResponseSchema(
#         code="200", status="Ok", message="Sucess retrieve data", result=_station_user
#     ).dict(exclude_none=True)

@router.post("/create-station-playlist-comment",dependencies=[Depends(JWTBearer())])
async def create_station_playlist_comment(request:Insertplaylistcomment, token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
            time_update = datetime.now()
            is_deleted = False
            decode_token = Ex_Decode.decode_token(token)
            user_id = decode_token["id"]
            username = decode_token['sub']

            check_user_type = BaseRepo.check_type(db,user_id,username,Users)
            check_member_type = BaseRepo.check_type(db,user_id,username,Member)

            results_check = check_type_value(check_user_type,check_member_type)

          
            #insert user to db
            if request.reply_id != 0:
                  _station_member = Sta_station_playlist_comments(
                              is_deleted = is_deleted,
                              created=time_update,
                              created_by=user_id,
                              description = request.description,
                              station_playlist_id=request.station_playlist_id,
                              reply_id=request.reply_id,
                              user_id = user_id,
                              type_user= results_check
                        )
                  BaseRepo.insert(db, _station_member)
            else:
                  _station_member = Sta_station_playlist_comments(
                              is_deleted = is_deleted,
                              created=time_update,
                              created_by=user_id,
                              description = request.description,
                              station_playlist_id=request.station_playlist_id,
                              user_id = user_id,
                              type_user= results_check
                        )
                  BaseRepo.insert(db, _station_member)
                   
            return ResponseSchema(
            code="200", status="Ok", message="Success save data"
             ).dict(exclude_none=True)
      
@router.post("/create-station-playlist-activity",dependencies=[Depends(JWTBearer())])
async def create_station_activity(request:Insertplaylistactivity,token: str = Depends(JWTBearer()),  db: Session = Depends(get_db)):
        time_update = datetime.now()
        decode_token = Ex_Decode.decode_token(token)
        user_id = decode_token["id"]

        
        
        select_update = BaseRepo.update_status_edit(db,
                                             Sta_station_playlist,
                                             request.station_playlist_id)
        
        results_update = BaseRepo.update(db,select_update)


        # insert user to db
        _station_member = Sta_station_playlist_activities(
                    created=time_update,
                    created_by=user_id,
                    description = request.description,
                    start_time = request.start_time,
                    station_playlist_id = request.station_playlist_id
            )

        BaseRepo.insert(db, _station_member)
        return ResponseSchema(
            code="200", status="Ok", message="Success save data"
             ).dict(exclude_none=True)


@router.delete("/delete-station-playlist-activity",dependencies=[Depends(JWTBearer())])
async def delete_station_playlist_activity(id:Optional[int]=None, token: str = Depends(JWTBearer()),  db: Session = Depends(get_db)):
      decode_token = Ex_Decode.decode_token(token)
      user_id = decode_token["id"]
      update_time = datetime.now()
      is_deleted = True

      update_status = BaseRepo.update_status_activity(db,
                                          id,
                                          user_id,
                                          update_time,
                                          Sta_station_playlist_activities
                                        )
      BaseRepo.update(db, update_status)

      id_station_playlist = update_status.station_playlist_id
      
      select_list_station_playlist_id = BaseRepo.check_count_playlist_activity(db,
                                           Sta_station_playlist_activities,
                                           id_station_playlist)
     
      if select_list_station_playlist_id == 0:
             prepair_data_rollback = BaseRepo.rollback_playlist_data(db,
                                                                     Sta_station_playlist,
                                                                     id_station_playlist)
             BaseRepo.update(db, prepair_data_rollback)

      
      return ResponseSchema(
            code="200", status="Ok", message="Success save data"
             ).dict(exclude_none=True)

@router.delete("/delete-station-playlist-comment",dependencies=[Depends(JWTBearer())])
async def create_station_activity(id:Optional[int]=None, token: str = Depends(JWTBearer()),  db: Session = Depends(get_db)):
      decode_token = Ex_Decode.decode_token(token)
      user_id = decode_token["id"]
      update_time = datetime.now()

      update_status_comment = BaseRepo.update_status_comment(db,
                                          id,
                                          user_id,
                                          update_time,
                                          Sta_station_playlist_comments
                                        )

      BaseRepo.update(db, update_status_comment)
      
      return ResponseSchema(
            code="200", status="Ok", message="Success save data"
             ).dict(exclude_none=True)



@router.patch("/update-station-period-process-status",dependencies=[Depends(JWTBearer())])
async def update_station_schedule_process_status(request:Updateprocessstatus,token: str = Depends(JWTBearer()),db: Session = Depends(get_db)):
      decode_token = Ex_Decode.decode_token(token)
      user_id = decode_token["id"]
      update_time = datetime.now()
      is_deleted = False
      update_station_schedule_status = BaseRepo.update_station_schedule_status(db,
                                          request.period_id,
                                          request.period_status_id,
                                          request.user_id,
                                          user_id,
                                          update_time,
                                          Sta_station_period
                                        )

      BaseRepo.update(db, update_station_schedule_status)

      name = "อัพเดทรายการ"
      description = "consider"
      object =  "station_period"
      

      results_find_schedule = BaseRepo.find_schedule(db,
                                           request.period_id,
                                           Sta_station_schedule
                                           )
      
      results_schedule = results_find_schedule[0].id


      create_data = Sta_station_schedule_activitie(
                        is_deleted = is_deleted,
                        created=update_time,
                        created_by=user_id,
                        station_schedule_id = results_schedule,
                        name=name,
                        description = description,
                        object= object,
                        status_id = request.period_id,
                        reference_id = request.period_id,
                        type_user = "user"
                  )
      BaseRepo.insert(db, create_data)

      return ResponseSchema(
            code="200", status="Ok", message="Update data Success"
             ).dict(exclude_none=True)



@router.get("/get-detail-station-schedule",dependencies=[Depends(JWTBearer())])
async def get_detail_station_schedule(id:Optional[int]=None,db: Session = Depends(get_db)):
      results_find_period = BaseRepo.find_period(db,
                                           id,
                                           Sta_station_period
                                           )
      results_period = results_find_period[0].station_schedule_id
      results_find_schedule = BaseRepo.find_schedule(db,
                                           results_period,
                                           Sta_station_schedule
                                           )
      
      results_schedule = results_find_schedule[0].station_id
      results_schedule_id = results_find_schedule[0].id
      
      results_find_station = BaseRepo.find_station(db,
                                           results_schedule,
                                           Sta_station
                                           )

     
      results_find_activity = BaseRepo.find_activity_real(db,
                                                    id,
                                                    Sta_station_schedule_activitie)
      
      
      all_activity = []
      for sta_station_schedule_activities in results_find_activity:
            
            if sta_station_schedule_activities.type_user is None or sta_station_schedule_activities.type_user == '':
                   sta_station_schedule_activities.type_user = "member"
            data_created_by = {}
            if sta_station_schedule_activities.type_user == "user":
                  find_user = BaseRepo.find_user_activity(db,sta_station_schedule_activities.created_by,Users)
                  for users in find_user:
                        if users.object_key is None:
                               users.object_key = "28-04-2023_17-13-51___1.jpg"
                        print(users.object_key)
                        bucket_name = 'member'
                        object_name = users.object_key

                        url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
                        data_created_by = {
                        'id':users.id,
                        'name':users.username,
                        'avatar_img':url,
                        'type_user':sta_station_schedule_activities.type_user
                        }
                        
                        
              
            elif sta_station_schedule_activities.type_user == "member":
                  
                   find_user = BaseRepo.find_user_activity(db,sta_station_schedule_activities.created_by,Member)
                   
                   for members in find_user:
                        
                        bucket_name = 'member'
                        object_name = members.object_key
                        
                        url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
                        data_created_by ={
                        'id':members.id,
                        'name':members.username,
                        'avatar_img':url,
                        'type_user':sta_station_schedule_activities.type_user
                        }
                        
                       
                        
                        
            
                        
            all_activity.append({
                  'id':sta_station_schedule_activities.id,
                  'name':sta_station_schedule_activities.name,
                  'description':sta_station_schedule_activities.description,
                  'created':sta_station_schedule_activities.created,
                  'status_id':sta_station_schedule_activities.status_id,
                  'created_by':data_created_by,
                  
            })

            
      
      results_find_playlist = BaseRepo.find_playlist(db,
                                                    id,
                                                    Sta_station_playlist)

      

      
      all_playlist = []
      for sta_station_playlists in  results_find_playlist:
            if sta_station_playlists.object_key is None:
                   sta_station_playlists.object_key = "20-03-2023_16-19-46___list-1.mp4"
            # Set bucket name and object name
            bucket_name = 'member'
            object_name = sta_station_playlists.object_key

            # Generate presigned URL for the object
            url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)


            all_playlist.append({
                  'id':sta_station_playlists.id,
                  'file_name':sta_station_playlists.file_name,
                  'file_path':url,
                  'file_type':sta_station_playlists.file_type,
                  'file_size':sta_station_playlists.file_size,
                  'time_duration':sta_station_playlists.time_duration,
                  'station_playlist_status_id':sta_station_playlists.station_playlist_status_id
            })


      result_all = {
                'id':results_find_period[0].id,
                'name':results_find_period[0].name,
                'period_status_id':results_find_period[0].period_status_id,
                'icon_path':results_find_period[0].icon_path,
                'period_time_start':results_find_period[0].period_time_start,
                'period_time_end':results_find_period[0].period_time_end,
                'user_id':results_find_period[0].user_id,
                'modified':results_find_period[0].modified,
                'schedule':{
                    'id':results_find_schedule[0].id,
                    'schedule_number':results_find_schedule[0].schedule_number,
                    'schedule_date':results_find_schedule[0].schedule_date
                },
                'station':{
                    'id':results_find_station[0].id,
                    'name':results_find_station[0].name,
                    'icon_path':results_find_station[0].icon_path
                },
                'all_activity':all_activity,
                'all_playlist':all_playlist
        }




      return ResponseSchema(
            code="200", status="Ok", message="Success save data",result=result_all
      ).dict(exclude_none=True)


# @router.get("/get-all-station-playlist-comment-old")
# async def get_detail_station_schedule(id:Optional[int]=None,db: Session = Depends(get_db)):

#     results_all = []
#     results_find_playlist_activity = BaseRepo.find_playlist_activity(db,
#                                                                      id,
#                                                                      Sta_station_playlist_activities)
#     all_activity = []
#     for sta_station_playlist_activities in results_find_playlist_activity:
#           all_activity.append({
#                 'id':sta_station_playlist_activities.id,
#                 'name':sta_station_playlist_activities.name,
#                 'description':sta_station_playlist_activities.description,
#                 'created':sta_station_playlist_activities.created,
#                 'start_time':sta_station_playlist_activities.start_time

#           })

   
#     results_find_playlist_history = BaseRepo.find_playlist_history(db,
#                                                                      id,
#                                                                      Sta_station_playlist_history)
    
#     all_history = []
#     for sta_station_playlist_histories in results_find_playlist_history:
#           all_history.append({
#                 'id':sta_station_playlist_histories.id,
#                 'file_name':sta_station_playlist_histories.file_name,
#                 'file_size':sta_station_playlist_histories.file_size,
#                 'time_duration':sta_station_playlist_histories.time_duration,
#                 'created':sta_station_playlist_histories.created
#           })

#     results_find_playlist_comments = BaseRepo.find_playlist_comments(db,
#                                                                      id,
#                                                                      Sta_station_playlist_comments)
    
    
    
 
#     all_comments = []
    
    
#     for x in results_find_playlist_comments:
      

#       message_reply = []
      
#       reply_id = x.id
      
#       results_reply = BaseRepo.find_reply(db,
#                                           reply_id ,
#                                           Sta_station_playlist_comments)
     
#       for sta_station_playlist_comments in results_reply: #reply
                  
                 
                  
#                   if sta_station_playlist_comments.type_user == 'user':
#                         results_find_user = BaseRepo.find_user_activity(db,
#                                           sta_station_playlist_comments.user_id,
#                                           Users)
                  
#                         for users in results_find_user:
#                               user_data = []
#                               bucket_name = 'member'
#                               object_name = users.object_key
#                               url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
                              
#                               user_data = {
#                                     'id':users.id,
#                                     'display_name':users.first_name,
#                                     'avatar_img':url
#                                     }
                              
                  
                              
                  
#                   elif sta_station_playlist_comments.type_user == 'member':
#                         results_find_user = BaseRepo.find_user_activity(db,
#                                           sta_station_playlist_comments.user_id,
#                                           Member)
                        
#                         for members in results_find_user:
                              
#                               user_data = []
#                               bucket_name = 'member'
#                               object_name = members.object_key
#                               url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
                              
#                               user_data = {
#                                     'id':users.id,
#                                     'display_name':users.first_name,
#                                     'avatar_img':url
#                                     }


#                   message_reply.append({
#                                     'id':sta_station_playlist_comments.id,
#                                     'name':sta_station_playlist_comments.name,
#                                     'description':sta_station_playlist_comments.description,
#                                     'created':sta_station_playlist_comments.created,
#                                     'member':user_data
#                                     })
                              
                  
                  
                                                    

          
      
#       if x.type_user == 'user':
#                   results_find_user = BaseRepo.find_user_activity(db,
#                                                           x.user_id,
#                                                           Users)
            
#                   for users in results_find_user:
#                    bucket_name = 'member'
#                    object_name = users.object_key
#                    url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)

                   

#                    all_comments.append({
#                         'id':x.id,
#                         'name':x.name,
#                         'description':x.description,
#                         'created':x.created,
#                         'member':{
#                           'id':users.id,
#                           'display_name':users.first_name,
#                           'avatar_img':url
#                         },
#                         'reply_message':message_reply
#                         })
                   
#       elif x.type_user == 'member':
#                   results_find_user = BaseRepo.find_user_activity(db,
#                                                           x.type_user,
#                                                           Member)
#                   for members in results_find_user:
#                    bucket_name = 'member'
#                    object_name = members.object_key

#                    url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
#                    all_comments.append({
#                         'id':x.id,
#                         'name':x.name,
#                         'description':x.description,
#                         'created':x.created,
#                         'member':{
#                           'id': members.id,
#                           'display_name': members.first_name,
#                           'avatar_img':url
#                         },
#                         'reply_message':message_reply
#                         })

#     results_all ={
#           'id':id,
#           'activity':all_activity,
#           'history':all_history,
#           'comments':all_comments,
#           #'member':data_member
#     }

#     return ResponseSchema(
#             code="200", status="Ok", message="Success save data",result=results_all
#       ).dict(exclude_none=True)



@router.get("/get-all-station-schedule-period-playlists-by-id",dependencies=[Depends(JWTBearer())])
async def get_detail_station_schedule(id:Optional[int]=None,db: Session = Depends(get_db)):

      results1 = BaseRepo.get_all_period_data(db,
                                              Sta_station,
                                              Sta_station_schedule,
                                              Sta_station_period,
                                              id)
      

      results2 = BaseRepo.get_all_schedule_data(db,
                                              Sta_station,
                                              Sta_station_schedule,
                                              Sta_station_period,
                                              id)
      get_schedule = []
      for sta_stations,sta_station_schedules,sta_station_periods in results2:
             object_name = sta_station_schedules.object_key
             bucket_name = 'stations'
             if sta_station_schedules.object_key is not None:
                object_name = sta_station_schedules.object_key
                url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
             else:
                url = None
            
             get_schedule.append({
                    'id':sta_station_schedules.id,
                    'schedule_number':sta_station_schedules.schedule_number,
                    'schedule_date':sta_station_schedules.schedule_date,        
                    })
             
      results3 = BaseRepo.get_all_station_data(db,
                                              Sta_station,
                                              Sta_station_schedule,
                                              Sta_station_period,
                                              id)
      
      get_station = []
      for sta_stations,sta_station_schedules,sta_station_periods in results3:
             
             get_station.append({
                   'id':sta_stations.id,
                   'name':sta_stations.name,
                   'icon_path':sta_stations.icon_path
             })

      results4 = BaseRepo.get_all_playlist_data(db,
                                              Sta_station,
                                              Sta_station_schedule,
                                              Sta_station_period,
                                              Sta_station_playlist,
                                              id)
      get_playlist = []
      for sta_stations,sta_station_schedules,sta_station_periods, sta_station_playlists in results4:
             
             get_playlist.append({
                   'id':sta_station_playlists.id,
                   'file_name':sta_station_playlists.file_name,
                   'file_path':sta_station_playlists.file_path,
                   'file_type':sta_station_playlists.file_type,
                   'file_size':sta_station_playlists.file_size,
                   'time_duration':sta_station_playlists.time_duration,
                   'playlist_status_id':sta_station_playlists.station_playlist_status_id,
             })


      get_main = []
      for sta_stations,sta_station_schedules,sta_station_periods,broadcast_status_name,period_status_name in results1:
             
             get_main.append({
                   'id':sta_station_periods.id,
                   'period_status_id':sta_station_periods.period_status_id,
                   'user_id':sta_station_periods.user_id,
                   'name':sta_station_periods.name,
                   'icon_path':sta_station_periods.icon_path,
                   'period_time_start':sta_station_periods.period_time_start, 
                   'period_time_end':sta_station_periods.period_time_end,
                   'broadcast_url':sta_station_periods.broadcast_url,
                   'schdule':get_schedule,
                   'station':get_station,
                   'all_playlist':get_playlist
                    
             })


      

      return ResponseSchema(
            code="200", status="Ok", message="Success save data", result=get_main
      ).dict(exclude_none=True)





@router.get("/get-all-station-playlist-comment",dependencies=[Depends(JWTBearer())])
async def get_detail_station_schedule(id:Optional[int]=None,db: Session = Depends(get_db)):
      results1 = BaseRepo.get_all_station_playlist_data(db,
                                              Sta_station_playlist_comments,
                                              Member,
                                              Users,
                                              id)
      get_station_playlist_comments = []
      get_all_main = []
      
      for sta_station_playlist_comments, members , users, first_name_case, last_name_case,object_key_case,username_case in results1:
          
           
            
            bucket_name = 'member'
            if object_key_case is not None:
                        object_name = object_key_case
                        url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
            else:
                        url = None
          
            
            if sta_station_playlist_comments.type_user == 'members':
                   user_id = members.id
            else:
                   user_id = users.id

            get_station_playlist_comments.append({
            'id':sta_station_playlist_comments.id,
            'reply_id':sta_station_playlist_comments.reply_id,
            'description':sta_station_playlist_comments.description,
            'first_name':first_name_case,
            'last_name':last_name_case,
            'is_deleted':sta_station_playlist_comments.is_deleted,
            'name':sta_station_playlist_comments.name,
            'created':sta_station_playlist_comments.created,
            'created_by':sta_station_playlist_comments.created_by,
            'modified':sta_station_playlist_comments.modified,
            'modified_by':sta_station_playlist_comments.modified_by,
            'station_playlist_id':sta_station_playlist_comments.station_playlist_id,
            'station_playlist_history_id':sta_station_playlist_comments.station_playlist_history_id,
            'user_id':user_id,
            'type_user':sta_station_playlist_comments.type_user,
            'avatar_img':url,
            'username':username_case,
            'object_key':object_key_case

            })

      results2 = BaseRepo.get_all_station_playlist_activity_data(db,
                                                                       Sta_station_playlist_activities,
                                                                       id)
      get_playlist_activity = []
      for sta_station_playlist_activities in results2:
                  get_playlist_activity.append({
                        'id':sta_station_playlist_activities.id,
                        'is_deleted':sta_station_playlist_activities.is_deleted,
                        'created':sta_station_playlist_activities.created,
                        'modified':sta_station_playlist_activities.modified,
                        'modified_by':sta_station_playlist_activities.modified_by,
                        'name':sta_station_playlist_activities.name,
                        'description':sta_station_playlist_activities.description,
                        'start_time':sta_station_playlist_activities.start_time,
                        'end_time':sta_station_playlist_activities.end_time,
                        'station_playlist_id':sta_station_playlist_activities.station_playlist_id,
                        'station_playlist_history_id':sta_station_playlist_activities.station_playlist_history_id,
                        'station_playlist_status_id':sta_station_playlist_activities.station_playlist_status_id,
                  })
                  
            
            

      results3 = BaseRepo.get_all_station_playlist_history_data(db,
                                                                       Sta_station_playlist_history,
                                                                       id)
            
      get_playlist_history = []
      for sta_station_playlist_histories in results3:
                  bucket_name = 'stations'
                  if sta_station_playlist_histories.object_key is not None:
                        object_name = sta_station_playlist_histories.object_key
                        url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
                  else:
                        url = None
                  get_playlist_history.append({
                        'id':sta_station_playlist_histories.id,
                        'is_deleted':sta_station_playlist_histories.is_deleted,
                        'created':sta_station_playlist_histories.created,
                        'created_by':sta_station_playlist_histories.created_by,
                        'modified':sta_station_playlist_histories.modified,
                        'modified_by':sta_station_playlist_histories.modified_by,
                        'station_playlist_id':sta_station_playlist_histories.station_playlist_id,
                        'file_name':sta_station_playlist_histories.file_name,
                        'file_path':url,
                        'file_type':sta_station_playlist_histories.file_type,
                        'file_size':sta_station_playlist_histories.file_size,
                        'time_duration':sta_station_playlist_histories.time_duration,
                        'object_key':sta_station_playlist_histories.object_key
                  })

                  
            
      get_all_main =[{
                  'activity':get_playlist_activity,
                  'comments':get_station_playlist_comments,
                  'history':get_playlist_history
      }]


      return ResponseSchema(
            code="200", status="Ok", message="Data Found", result=get_all_main
      ).dict(exclude_none=True)



      
@router.patch("/update-period-status-by-id",dependencies=[Depends(JWTBearer())])
async def update_station_schedule_process_status(request:Updateperiodstatusid,token: str = Depends(JWTBearer()),db: Session = Depends(get_db)):
      decode_token = Ex_Decode.decode_token(token)
      user_id = decode_token["id"]
      update_time = datetime.now()
      results = BaseRepo.select_update_data(db,
                                            Sta_station_period,
                                            request.id,
                                            request.period_status_id,
                                            user_id,
                                            update_time)

      try:
            results_update = BaseRepo.update(db,results)
      except Exception as e:
            results_update = db.rollback()


      if results_update == True:
                            if request.period_status_id == 1:
                                   name = "กำลังดำเนินการ"
                                   icon = "icon-stopwatch.svg"
                            elif request.period_status_id == 2:
                                   name = "ปิดงาน"
                                   icon = "icon-message-check.svg"
                            elif request.period_status_id == 3:
                                   name = "ขอให้ปรับแก้"
                                   icon = "icon-alert-triangle.svg"
                            elif request.period_status_id == 4:
                                   name = "ส่งผลการแก้ไข"
                                   icon = "icon-arrow-repeat.svg"
                            elif request.period_status_id == 5:
                                   name = "ปิดงานแก้ไข"
                                   icon = "icon-message-check.svg"
                            insert_suspend = Sta_station_schedule_activitie(
                                                        is_deleted = False,
                                                        created=update_time,
                                                        created_by=user_id,
                                                        name=name,
                                                        description="รายการ" + ' ' + str(results.name),
                                                        reference_id = request.id,
                                                        station_schedule_id = results.station_schedule_id,
                                                        object = "station_periods",
                                                        icon = icon,
                                                        type_user = "users",
                                                        type_activity = "examine"
                    
                                                )
                            results_insert = BaseRepo.insert(db,insert_suspend)

      if request.period_status_id == 3:
            station_playlist_status_id = 3
            results2x = BaseRepo.select_update_playlist(db,
                                                      Sta_station_playlist,
                                                      request.id)
      
            for x in results2x:
                  
                  results2 = BaseRepo.update_playlist(db,
                                                      Sta_station_playlist,
                                                      x.id,
                                                      station_playlist_status_id)
      

                  try:
                        results_update = BaseRepo.update(db,results2)
                  except Exception as e:
                        results_update = db.rollback()

                  if results_update == True:
                                    insert_suspend = Sta_station_schedule_activitie(
                                                                  is_deleted = False,
                                                                  created=update_time,
                                                                  created_by=user_id,
                                                                  name="ข้อให้ปรับแก้รายการ",
                                                                  description="รายการ" + ' '+ str(results2.file_name) ,
                                                                  reference_id = request.id,
                                                                  station_schedule_id = results.station_schedule_id,
                                                                  object = "station_playlists",
                                                                  icon = icon,
                                                                  type_user = "users"
                              
                                                            )
                                    results_insert = BaseRepo.insert(db,insert_suspend)
      
      if request.period_status_id == 5:
            station_playlist_status_id = 5
            
            results2x = BaseRepo.select_update_playlist_2(db,
                                                      Sta_station_playlist,
                                                      request.id)
            
            for x in results2x:
                 
                  results2 = BaseRepo.update_playlist(db,
                                                      Sta_station_playlist,
                                                      x.id,
                                                      station_playlist_status_id)
      

                  try:
                        results_update = BaseRepo.update(db,results2)
                  except Exception as e:
                        results_update = db.rollback()

                  if results_update == True:
                                    insert_suspend = Sta_station_schedule_activitie(
                                                                  is_deleted = False,
                                                                  created=update_time,
                                                                  created_by=user_id,
                                                                  name="ปิดงานแก้ไข",
                                                                  description="รายการ" + ' '+ str(results2.file_name) ,
                                                                  reference_id = request.id,
                                                                  station_schedule_id = results.station_schedule_id,
                                                                  object = "station_playlists",
                                                                  icon = icon,
                                                                  type_user = "users"
                              
                                                            )
                                    results_insert = BaseRepo.insert(db,insert_suspend)

      return ResponseSchema(
            code="200", status="Ok", message="Update Success"
      ).dict(exclude_none=True)

      