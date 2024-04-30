from fastapi import APIRouter, Depends , Header
from fastapi.responses import JSONResponse
from typing import List , Optional
from schema import (
    RequestSchema,
    ResponseSchema,
    TokenResponse,
    UserSigupSchema,
    UserSiginSchema,
    Updatescheduleperiodstatus,
    Insertcustomerinterest,
    Createcustomeractionweb
)
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from respository.web_repository import JWTRepo, JWTBearer,Ex_Decode
from passlib.context import CryptContext
from respository.repo_member import BaseRepo

from model import (
     Users , 
     Sta_station ,
     Stat_customer,
     Sta_station_schedule,
     Stat_customer_action_detail,
     Stat_customer_interest,
     Sta_station_period,
     Sta_channel,
     Member,
     Sta_station_channel,
     Sta_period_categories,
     Sta_broadcast_type,
     Countries,
     Sta_period_categories,
     Sta_categories
     

     )
from datetime import datetime, timedelta
import pdb
from minio_handler import MinioHandler
from minio import Minio


router = APIRouter(
              prefix="",
              tags=['member'],
              responses ={404:{
                            'message' : "Not found"
              }}
              
)

@router.get("/get-customer-interests-web",dependencies=[Depends(JWTBearer())])
async def get_customer_interests_web(token: str = Depends(JWTBearer()),db: Session = Depends(get_db)):
    try:
        decode_token = Ex_Decode.decode_token(token)
        user_id = decode_token["id"]
        get_all_data = BaseRepo.get_all_guest(db,
                                                Sta_station,
                                                Stat_customer_interest,
                                                user_id)
        
        results = []
        for item in get_all_data:
                results.append({
                'id':item[0],
                'icon_path':item[2],
                'station_approve_id':item[3],
                'name':item[1]
                })
        
        return ResponseSchema(
                code="200", status="Ok", message="Success save data" ,result=results
                ).dict(exclude_none=True)
    except Exception as e:
        print (f"Error: {str(e)}")
@router.get("/get-list-schedule-period-web-top")
async def get_schedule_period_web(id:Optional[int]=None,db: Session = Depends(get_db)):
        get_data_station = BaseRepo.select_station_data(db,
                                                        Sta_station,
                                                        id)
        
        
        results = [] 
        bucket_name = 'stations'
        if get_data_station.object_key is not None:
                            object_name = get_data_station.object_key
                            url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
        else:
                            url = None
        results.append({
                'id':get_data_station.id,
                'name':get_data_station.name,
                'count_like':get_data_station.count_like,
                'count_share':get_data_station.count_share,
                'count_listen':get_data_station.count_listen,
                'station_img':url
        })

        return ResponseSchema(
              code="200", status="Ok", message="foundData" ,result=results
             ).dict(exclude_none=True)

@router.get("/get-list-schedule-period-web-bottom")
async def get_schedule_period_web(id:Optional[int]=None,db: Session = Depends(get_db)):
    update_time = datetime.now()
    current_date = update_time.date()
    get_all_data = BaseRepo.get_all_schedule_period(db,
                                                     Sta_station_schedule,
                                                     Sta_station_period,
                                                     Sta_station,
                                                     Sta_broadcast_type,
                                                     Sta_period_categories,
                                                     id,
                                                     current_date)
    results = []

    for sta_station_schedules , sta_station_periods, sta_stations ,sta_broadcast_types, sta_period_categories in get_all_data:
              

              bucket_name = 'stations'
        
        
              if sta_stations.object_key is not None:
                            object_name = sta_stations.object_key
                            url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
              else:
                            url = None

              
              if sta_station_schedules.object_key is not None:
                            object_name2 = sta_station_schedules.object_key
                            url2 = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name2)
              else:
                            url2 = None

              if sta_station_periods.object_key is not None:
                            object_name3 = sta_station_periods.object_key
                            url3 = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name3)
              else:
                            url3 = None

              if sta_station_periods.station_channel_id is not None:
                results_member = []
                channel_id = sta_station_periods.station_channel_id
           
                member_detail = BaseRepo.get_produce(db,
                                                     Sta_station_channel,
                                                     Sta_channel,
                                                     Member,
                                                     channel_id
                                                )
           
                for sta_station_channels , sta_channels, members in member_detail:
                        results_member.append({
                        'id':members.id,
                        'first_name':members.first_name,
                        'last_name':members.last_name,
                        'display_name':members.display_name
                        })

                
          
        
        
              else:
            
                        member_id  = sta_station_periods.created_by
                        results_member = []
                        member_detail = BaseRepo.get_produce_none(db,
                                                                Member,
                                                                member_id)
                        
                        results_member.append({
                        'id':member_detail.id,
                        'first_name':member_detail.first_name,
                        'last_name':member_detail.last_name,
                        'display_name':member_detail.display_name
                        })
              
             
              results.append({
                   'schedule_id':sta_station_schedules.id,
                   'schedule_station_id':sta_station_schedules.station_id,
                   'station_name':sta_stations.name,
                   'station_img':url,
                   'schedule_img':url2,
                   'period_img':url3,
                   'period_description':sta_station_periods.description,
                   'station_count_like':sta_stations.count_like,
                   'station_count_share':sta_stations.count_share,
                   'station_count_listen':sta_stations.count_listen,
                   'schedule_date':sta_station_schedules.schedule_date,
                   'broadcast_type_id':sta_station_periods.broadcast_type_id,
                   'broadcast_type_name':sta_broadcast_types.name,
                   'period_id':sta_station_periods.id,
                   'period_name':sta_station_periods.name,
                   'period_time_start':sta_station_periods.period_time_start,
                   'period_time_end':sta_station_periods.period_time_end,
                   'categories_id':sta_period_categories.id,
                   'categories_name':sta_period_categories.name,
                   'member':results_member
              })

    return ResponseSchema(
              code="200", status="Ok", message="foundData" ,result=results
    ).dict(exclude_none=True)
                   



@router.get("/get-period-broadcast-web")
async def get_period_broadcast_web(id:Optional[int]=None,db: Session = Depends(get_db)):
        get_data_broadcast = BaseRepo.period_broadcast_web(db,
                                                           Sta_station_schedule,
                                                           Sta_station_period,
                                                           id)
        results = []
        for sta_station_schedules , sta_station_periods in get_data_broadcast:
                results.append({
                        'schedule_id':sta_station_schedules.id,
                        'period_id':sta_station_periods.id,
                        'schedule_date':sta_station_schedules.schedule_date,
                        'period_name':sta_station_periods.name,
                        'period_broadcast_url':sta_station_periods.broadcast_url
                })

        return ResponseSchema(
              code="200", status="Ok", message="Success save data" ,result=results
             ).dict(exclude_none=True)

@router.get("/get-period-broadcast-live-web")
async def get_period_live_web(id:Optional[int]=None,period_id:Optional[int]=None,db: Session = Depends(get_db)):
        get_data_period_live = BaseRepo.get_period_live_web(db,
                                                            Sta_station_schedule,
                                                            Sta_station_period,
                                                            Sta_station,
                                                            Sta_period_categories,
                                                            id,
                                                            period_id)
        
        results = []
        for sta_station_schedules , sta_station_periods, sta_stations , sta_period_categories in get_data_period_live:
                  
            if sta_station_periods.station_channel_id is not None:
                results_member = []
                channel_id = sta_station_periods.station_channel_id
           
                member_detail = BaseRepo.find_channel(db,
                                                     Sta_station_channel,
                                                     Sta_channel,
                                                     Member,
                                                     channel_id
                                                )
           
                for sta_station_channels , sta_channels, members in member_detail:
                        results_member.append({
                        'id':members.id,
                        'first_name':members.first_name,
                        'last_name':members.last_name,
                        'display_name':members.display_name
                        })

            else:
            
                member_id  = sta_station_periods.created_by
                results_member = []
                member_detail = BaseRepo.find_channel_none(db,
                                                        Member,
                                                        member_id)
            
                results_member.append({
                'id':member_detail.id,
                'first_name':member_detail.first_name,
                'last_name':member_detail.last_name,
                'display_name':member_detail.display_name
                })
            results.append({
                        'schedule_id':sta_station_schedules.id,
                        'station_name':sta_stations.name,
                        'schedule_date':sta_station_schedules.schedule_date,
                        'period_id':sta_station_periods.id,
                        'period_name':sta_station_periods.name,
                        'period_time_start':sta_station_periods.period_time_start,
                        'period_time_end':sta_station_periods.period_time_end,
                        'categories_id':sta_period_categories.id,
                        'categories.name':sta_period_categories.name,
                        'period_img':sta_station_periods.icon_path,
                        'period_description':sta_station_periods.description,
                        'broadcast_url':sta_station_periods.broadcast_url,
                        'station_img':sta_stations.icon_path,
                        'broadcast_type_id':sta_station_periods.broadcast_type_id,
                        'member':results_member
                })
        return ResponseSchema(
              code="200", status="Ok", message="Success save data" ,result=results
             ).dict(exclude_none=True)

@router.get("/get-list-period-listen-top-web")
async def get_list_period_listen_top_web(id:Optional[int]=None,db: Session = Depends(get_db)):
        get_listen_top_web = BaseRepo.get_listen_top(db,
                                                     Sta_station_schedule,
                                                     Sta_station_period,
                                                     Sta_station,
                                                     Sta_period_categories,
                                                     id)
        
        results = []
        for sta_station_schedules , sta_station_periods, sta_stations , sta_period_categories in get_listen_top_web:

                if sta_station_periods.station_channel_id is not None:
                        results_member = []
                        channel_id = sta_station_periods.station_channel_id
                
                        member_detail = BaseRepo.find_channel(db,
                                                        Sta_station_channel,
                                                        Sta_channel,
                                                        Member,
                                                        channel_id
                                                )
           
                        for sta_station_channels , sta_channels, members in member_detail:
                                results_member.append({
                                'id':members.id,
                                'first_name':members.first_name,
                                'last_name':members.last_name,
                                'display_name':members.display_name
                                })

                else:
            
                        member_id  = sta_station_periods.created_by
                        results_member = []
                        member_detail = BaseRepo.find_channel_none(db,
                                                                Member,
                                                                member_id)
                
                        results_member.append({
                        'id':member_detail.id,
                        'first_name':member_detail.first_name,
                        'last_name':member_detail.last_name,
                        'display_name':member_detail.display_name
                        })
                results.append({
                        'schedule_id':sta_station_schedules.id,
                        'station_name':sta_stations.name,
                        'schedule_date':sta_station_schedules.schedule_date,
                        'period_id':sta_station_periods.id,
                        'period_name':sta_station_periods.name,
                        'period_time_start':sta_station_periods.period_time_start,
                        'period_time_end':sta_station_periods.period_time_end,
                        'categories_id':sta_period_categories.id,
                        'categories.name':sta_period_categories.name,
                        'station_id':sta_stations.id,
                        'schedule_number':sta_station_schedules.schedule_number,
                        'period_img':sta_station_periods.icon_path,
                        'station_img':sta_stations.icon_path,
                        'broadcast_url':sta_station_periods.broadcast_url,
                        'broadcast_type_id':sta_station_periods.broadcast_type_id,
                        'member':results_member
                })
        return ResponseSchema(
              code="200", status="Ok", message="Success save data" ,result=results
             ).dict(exclude_none=True)

@router.get("/get-list-program-schedule-period-web")
async def get_list_program_schedule_period_web(id:Optional[int]=None,type:Optional[str]=None,db: Session = Depends(get_db)):
        #type today , yesterday , tomorrow
        update_time = datetime.now()
        if type is None:
                type = 'today' 
                update_time = update_time.strftime("%Y-%m-%d")
        elif type == 'today':
                update_time = update_time.strftime("%Y-%m-%d")
        elif type == 'yesterday':
                update_time = update_time - timedelta(days=1)
                update_time = update_time.strftime("%Y-%m-%d")
        elif type == 'tomorrow':
                update_time = update_time + timedelta(days=1)
                update_time = update_time.strftime("%Y-%m-%d")
        
       
        get_list_program = BaseRepo.get_list_programe_schedule(db,
                                                     Sta_station_schedule,
                                                     Sta_station_period,
                                                     Sta_station,
                                                     Sta_broadcast_type,
                                                     Sta_period_categories,
                                                     id,
                                                     update_time)
        
        results = []
        for sta_station_schedules , sta_station_periods, sta_stations ,sta_broadcast_types, sta_period_categories in get_list_program:
                if sta_station_periods.station_channel_id is not None:
                        results_member = []
                        channel_id = sta_station_periods.station_channel_id
                
                        member_detail = BaseRepo.get_produce(db,
                                                        Sta_station_channel,
                                                        Sta_channel,
                                                        Member,
                                                        channel_id
                                                        )
                
                        for sta_station_channels , sta_channels, members in member_detail:
                                results_member.append({
                                'id':members.id,
                                'first_name':members.first_name,
                                'last_name':members.last_name,
                                'display_name':members.display_name
                                })

                else:
                
                        member_id  = sta_station_periods.created_by
                        results_member = []
                        member_detail = BaseRepo.get_produce_none(db,
                                                                Member,
                                                                member_id)
                
                        results_member.append({
                        'id':member_detail.id,
                        'first_name':member_detail.first_name,
                        'last_name':member_detail.last_name,
                        'display_name':member_detail.display_name
                        })
                
                results.append({
                        'schedule_id':sta_station_schedules.station_id,
                        'station_name':sta_stations.name,
                        'schedule_date':sta_station_schedules.schedule_date,
                        'period_id':sta_station_periods.id,
                        'period_name':sta_station_periods.name,
                        'period_time_start':sta_station_periods.period_time_start,
                        'period_time_end':sta_station_periods.period_time_end,
                        'categories_id':sta_period_categories.id,
                        'categories_name':sta_period_categories.name,
                        'broadcast_type_name':sta_broadcast_types.name,
                        'period_icon_path':sta_station_periods.icon_path,
                        'station_icon_path':sta_stations.icon_path,
                        'member':results_member

                })
        return ResponseSchema(
              code="200", status="Ok", message="Success save data" ,result=results
             ).dict(exclude_none=True)

@router.get("/get-stations-detail-web")
async def get_list_program_schedule_period_web(id:Optional[int]=None,db: Session = Depends(get_db)):
        bucket_name = 'stations'
        get_station_detail_web = BaseRepo.get_detail_web(db,
                                                         Sta_station,
                                                         Countries,
                                                         id)
        
        results = []
        for sta_stations , countries in get_station_detail_web:
                if sta_stations.object_key is not None:
                            object_name = sta_stations.object_key
                            url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
                else:
                            url = None
                results.append({
                        'id':sta_stations.id,
                        'name':sta_stations.name,
                        'description':sta_stations.description,
                        'count_like':sta_stations.count_like,
                        'count_share':sta_stations.count_share,
                        'count_listen':sta_stations.count_listen,
                        'approve_date':sta_stations.approve_date,
                        'country_name':countries.name,
                        'station_img':url
                })

        return ResponseSchema(
              code="200", status="Ok", message="Success save data" ,result=results
             ).dict(exclude_none=True)
        

@router.post("/process-customer-action-web",dependencies=[Depends(JWTBearer())])
async def create_customer_action_web(request:Createcustomeractionweb,token: str = Depends(JWTBearer()),db: Session = Depends(get_db)):
        current_date = datetime.now()
        formatted_time = current_date.strftime("%H:%M:%S")
        decode_token = Ex_Decode.decode_token(token)
        user_id = decode_token["id"]
        user_name = decode_token["sub"]
        
        
        
        if request.action_type == 5:

                if request.schedule_id == 0:
                        request.schedule_id = None
                
                if request.period_id == 0:
                        request.period_id = None
                
                if request.period_id is None:
                
                        get_data_like = BaseRepo.update_unlike(db,
                                                        Stat_customer_action_detail,
                                                        user_id,
                                                        request.station_id,
                                                        current_date
                                                        )
                        
                        
                        results_update_like = BaseRepo.update(db, get_data_like)

                        if results_update_like == True:
                                
                                request.action_type = 1
                                value_count = BaseRepo.get_count_like_period_none(db,
                                                                                Stat_customer_action_detail,
                                                                                request.action_type,
                                                                                request.station_id,
                                                                              )
                                
                                
                                if value_count is None:
                                                value_count = 0       
                                update_station = BaseRepo.update_count_station(db,
                                                                                       Sta_station,
                                                                                       value_count,
                                                                                       request.station_id,
                                                                                       request.action_type)
                                if update_station is not None:
                                        results_update = BaseRepo.update(db,update_station)
                                else:
                                        pass
                                
                                if results_update == True:
                                        return ResponseSchema(
                                        code="200", status="Ok", message="updateSuccess"
                                        ).dict(exclude_none=True)
                                else:
                                        return ResponseSchema(
                                        code="200", status="Ok", message="dataHasProblem"
                                        ).dict(exclude_none=True)
                        
                        else:
                                return ResponseSchema(
                                code="200", status="Ok", message="dataHasProblem"
                                ).dict(exclude_none=True)
                        
                else:
                        
                        get_data_like = BaseRepo.update_unlike_period(db,
                                                        Stat_customer_action_detail,
                                                        user_id,
                                                        request.station_id,
                                                        request.period_id,
                                                        current_date
                                                        )
                        
                        results_update_like = BaseRepo.update(db, get_data_like)

                        if results_update_like == True:
                                request.action_type = 1
                                value_count = BaseRepo.get_count_like_period(db,
                                                                                Stat_customer_action_detail,
                                                                                request.action_type,
                                                                                request.station_id,
                                                                                request.period_id)
                                if value_count is None:
                                                value_count = 0        
                                update_period = BaseRepo.update_count_period(db,
                                                                                     Sta_station_period,
                                                                                     value_count,
                                                                                     request.period_id,
                                                                                     request.action_type)
                                if update_period.channel_id is not None:
                                                channel_id = update_period.channel_id

                                                set_update_count_like_channel = BaseRepo.get_data_like_channel(db,
                                                                                                               Sta_channel,
                                                                                                               channel_id,
                                                                                                               value_count)
                                                if set_update_count_like_channel is not None:
                                                        results_update = BaseRepo.update(db,set_update_count_like_channel)
                                
                                if update_period is None:
                                        return ResponseSchema(
                                                code="200", status="Ok", message="notFoundPeriodId"
                                                ).dict(exclude_none=True)

                                else:
                                        results_update = BaseRepo.update(db,update_period)
                                        
                                        if results_update == True:
                                                return ResponseSchema(
                                                code="200", status="Ok", message="updateSuccess"
                                                ).dict(exclude_none=True)
                                        else:
                                                return ResponseSchema(
                                                code="200", status="Ok", message="dataHasProblem"
                                                ).dict(exclude_none=True)
                        
                        else:
                                return ResponseSchema(
                                code="200", status="Ok", message="dataHasProblem"
                                ).dict(exclude_none=True)

        elif request.action_type == 1:
               
                if request.schedule_id == 0:
                        request.schedule_id = None
                
                if request.period_id == 0:
                        request.period_id = None


                


                if request.period_id == None:
                        check_data_action_detail = BaseRepo.check_data_action_detail_period_none(db,
                                                                                            Stat_customer_action_detail,
                                                                                            user_id,
                                                                                            request.action_type,
                                                                                            request.station_id)
                        
                else:
                        check_data_action_detail = BaseRepo.check_data_action_detail_period(db,
                                                                                                 Stat_customer_action_detail,
                                                                                                 user_id,
                                                                                                 request.action_type,
                                                                                                 request.station_id,
                                                                                                 request.period_id)
                        
                        
                
                
                if check_data_action_detail is None:
                        
                        insert_data = Stat_customer_action_detail(
                                station_id = request.station_id,
                                schedule_id = request.schedule_id,
                                period_id = request.period_id,
                                customer_id = user_id,
                                action_type_id = request.action_type,
                                action_date = current_date,
                                action_time = formatted_time,
                                is_active = True,
                                created = current_date,
                                created_by = user_id,
                        )

                        results_insert = BaseRepo.insert(db,insert_data)
                        
                        
                        if results_insert == True:
                                
                                if request.period_id is None:
                                        value_count = BaseRepo.get_count_like_period_none(db,
                                                                                Stat_customer_action_detail,
                                                                                request.action_type,
                                                                                request.station_id,
                                                                              )
                                       
                                        if value_count is None:
                                                value_count = 0
                                        update_station = BaseRepo.update_count_station(db,
                                                                                       Sta_station,
                                                                                       value_count,
                                                                                       request.station_id,
                                                                                       request.action_type)
                                        
                                        if update_station is not None:
                                                results_update = BaseRepo.update(db,update_station)
                                                if results_update == True:
                                                        return ResponseSchema(
                                                        code="200", status="Ok", message="sucessSaveData"
                                                        ).dict(exclude_none=True)
                                                else:
                                                
                                                        return ResponseSchema(
                                                        code="200", status="Ok", message="dataHasProblem"
                                                        ).dict(exclude_none=True)  
                                        else:
                                                
                                                pass
                                else:
                                        
                                        value_count = BaseRepo.get_count_like_period(db,
                                                                                Stat_customer_action_detail,
                                                                                request.action_type,
                                                                                request.station_id,
                                                                                request.period_id)
                                        if value_count is None:
                                                value_count = 0
                                        
                                        update_period = BaseRepo.update_count_period(db,
                                                                                     Sta_station_period,
                                                                                     value_count,
                                                                                     request.period_id,
                                                                                     request.action_type)
                                        
                                        results_update_station = BaseRepo.update(db,update_period)
                                        
                                        if update_period.channel_id is not None:
                                                channel_id = update_period.channel_id
                                                
                                                count_like_channel = BaseRepo.count_all_like_channel(db,
                                                                                            Sta_channel,
                                                                                            channel_id 
                                                                                            )
                                                
                                                if count_like_channel is None:
                                                        score = 0
                                                else:
                                                        score = int(count_like_channel.count_like)+1
                                                
                                                set_update_count_like_channel = BaseRepo.get_data_like_channel(db,
                                                                                                               Sta_channel,
                                                                                                               channel_id,
                                                                                                               score)
                                                
                                                if set_update_count_like_channel is not None:
                                                        results_update = BaseRepo.update(db,set_update_count_like_channel)
                                                        
                                                

                                        
                                        if results_update_station == True:
                                                return ResponseSchema(
                                                code="200", status="Ok", message="sucessSaveData"
                                                ).dict(exclude_none=True)
                                        else:
                                                
                                                return ResponseSchema(
                                                code="200", status="Ok", message="dataHasProblem"
                                                ).dict(exclude_none=True)   
                                
                else:
                        
                       
                        return ResponseSchema(
                        code="200", status="Ok", message="dataHasBeenInsert"
                        ).dict(exclude_none=True)
                
        else:
                
                if request.schedule_id == 0:
                        request.schedule_id = None
                
                if request.period_id == 0:
                        request.period_id = None


                insert_data = Stat_customer_action_detail(
                                station_id = request.station_id,
                                schedule_id = request.schedule_id,
                                period_id = request.period_id,
                                customer_id = user_id,
                                action_type_id = request.action_type,
                                action_date = current_date,
                                action_time = formatted_time,
                                is_active = True,
                                created = current_date,
                                created_by = user_id,
                        )

                results_insert = BaseRepo.insert(db,insert_data)
                
                
                if results_insert == True:
                                
                                if request.period_id is None:
                                        value_count = BaseRepo.get_count_like_period_none(db,
                                                                                Stat_customer_action_detail,
                                                                                request.action_type,
                                                                                request.station_id,
                                                                              )
                                        
                                        if value_count is None:
                                                value_count = 0
                                        update_station = BaseRepo.update_count_station(db,
                                                                                       Sta_station,
                                                                                       value_count,
                                                                                       request.station_id,
                                                                                       request.action_type)
                                        
                                        if update_station is not None:
                                                results_update = BaseRepo.update(db,update_station)
                                                if results_update == True:
                                                        return ResponseSchema(
                                                        code="200", status="Ok", message="sucessSaveData"
                                                        ).dict(exclude_none=True)
                                                else:
                                                
                                                        return ResponseSchema(
                                                        code="200", status="Ok", message="dataHasProblem"
                                                        ).dict(exclude_none=True)  
                                        else:
                                                
                                                pass

                                        
                                else:
                                        value_count = BaseRepo.get_count_like_period(db,
                                                                                Stat_customer_action_detail,
                                                                                request.action_type,
                                                                                request.station_id,
                                                                                request.period_id)
                                        if value_count is None:
                                                value_count = 0
                                        
                                        update_period = BaseRepo.update_count_period(db,
                                                                                     Sta_station_period,
                                                                                     value_count,
                                                                                     request.period_id,
                                                                                     request.action_type)
                                        
                                        results_update_station = BaseRepo.update(db,update_period)

                                        
                                        
                                        if results_update_station == True:
                                                return ResponseSchema(
                                                code="200", status="Ok", message="sucessSaveData"
                                                ).dict(exclude_none=True)
                                        else:
                                                
                                                return ResponseSchema(
                                                code="200", status="Ok", message="dataHasProblem"
                                                ).dict(exclude_none=True)

                        
                        

@router.get("/get-list-period-live-web")
async def get_schedule_period_web(id:Optional[int]=None,db: Session = Depends(get_db)):
        get_data_period_live = BaseRepo.get_list_period_web(db,
                                                            Sta_station_schedule,
                                                            Sta_station_period,
                                                            Sta_station,
                                                            Sta_period_categories,
                                                            id)
        results = []
        results_station = []
        results_schedule = []
        results_member = []
        for sta_station_schedules , sta_station_periods, sta_stations , sta_period_categories in get_data_period_live:

                if sta_station_periods.station_channel_id is not None:
                        results_member = []
                        channel_id = sta_station_periods.station_channel_id
                
                        member_detail = BaseRepo.get_produce(db,
                                                        Sta_station_channel,
                                                        Sta_channel,
                                                        Member,
                                                        channel_id
                                                        )
                
                        for sta_station_channels , sta_channels, members in member_detail:
                                results_member.append({
                                'id':members.id,
                                'first_name':members.first_name,
                                'last_name':members.last_name,
                                'display_name':members.display_name
                                })

                else:
                
                        member_id  = sta_station_periods.created_by
                        results_member = []
                        member_detail = BaseRepo.get_produce_none(db,
                                                                Member,
                                                                member_id)
                
                        results_member.append({
                        'id':member_detail.id,
                        'first_name':member_detail.first_name,
                        'last_name':member_detail.last_name,
                        'display_name':member_detail.display_name
                        })
                if sta_stations.object_key is None:
                        results_station.append({
                                'id':sta_stations.id,
                                'name':sta_stations.name,
                                'image':None
                        })
                else:
                        results_station.append({
                                'id':sta_stations.id,
                                'name':sta_stations.name,
                                'image':sta_stations.icon_path
                        })

                if sta_station_schedules.object_key is None:
                        results_schedule.append({
                                'id':sta_station_schedules.id,
                                'number':sta_station_schedules.schedule_number,
                                'date':sta_station_schedules.schedule_date,
                                'image':None

                        })
                else:   
                        results_schedule.append({
                        'id':sta_station_schedules.id,
                        'number':sta_station_schedules.schedule_number,
                        'date':sta_station_schedules.schedule_date,
                        'image':sta_station_schedules.icon_path

                })
                        
                if sta_station_periods.object_key is None:
                        results.append({
                                'id':sta_station_periods.id,
                                'broadcast_status_id':sta_station_periods.broadcast_status_id,
                                'name':sta_station_periods.name,
                                'description':sta_station_periods.description,
                                'image':None,
                                'time_start':sta_station_periods.period_time_start,
                                'time_end':sta_station_periods.period_time_end,
                                'broadcast_url':sta_station_periods.broadcast_url,
                                'boradcast_type_id':sta_station_periods.broadcast_type_id,
                                'station':results_station,
                                'schedule':results_schedule,
                                'member':results_member
                        })
                else:
                        results.append({
                                'id':sta_station_periods.id,
                                'broadcast_status_id':sta_station_periods.broadcast_status_id,
                                'name':sta_station_periods.name,
                                'description':sta_station_periods.description,
                                'image':sta_station_periods.icon_path,
                                'time_start':sta_station_periods.period_time_start,
                                'time_end':sta_station_periods.period_time_end,
                                'broadcast_url':sta_station_periods.broadcast_url,
                                'boradcast_type_id':sta_station_periods.broadcast_type_id,
                                'station':results_station,
                                'schedule':results_schedule,
                                'member':results_member
                        })
        
        return ResponseSchema(
              code="200", status="Ok", message="Success save data" ,result=results
             ).dict(exclude_none=True)

@router.get("/get-list-like",dependencies=[Depends(JWTBearer())])
async def get_schedule_period_web(token: str = Depends(JWTBearer()),db: Session = Depends(get_db)):
        try:
                decode_token = Ex_Decode.decode_token(token)
                user_id = decode_token["id"]
                get_data_like = BaseRepo.get_data_like_station(db,
                                                Stat_customer_action_detail,
                                                user_id)
                results_all = []
                station_ids = [row[0] for row in get_data_like]


                
                get_data_like_schedule = BaseRepo.get_data_like_schedule(db,
                                                Stat_customer_action_detail,
                                                user_id)
                schedule_ids = [row[0] for row in get_data_like_schedule]
                
                get_data_like_period = BaseRepo.get_data_like_period(db,
                                                Stat_customer_action_detail,
                                                user_id)
                
                period_ids = [row[0] for row in get_data_like_period]
                
                
                

                
                results_all.append({
                        'station':station_ids,
                        'schedule':schedule_ids,
                        'period':period_ids
                })

                return ResponseSchema(
                code="200", status="Ok", message="foundData" ,result=results_all
                ).dict(exclude_none=True)
        except Exception as e:
           print(f"Error: {str(e)}")
        

@router.get("/get-all-period-category-web")
async def get_schedule_period_web(lang: str = Header(None),db: Session = Depends(get_db)):
        
        try:
                get_data_categories = BaseRepo.get_data_cate(db,
                                                        Sta_period_categories)
                
                if lang is None:
                        lang = "th"

                
                        
                
                results = [] 
                for sta_period_categories in get_data_categories:
                        if lang == "th":
                                results.append({
                                        'id':sta_period_categories.id,
                                        'name':sta_period_categories.name_th,
                                        'sort':sta_period_categories.sort
                                })
                        elif lang == "en":
                                results.append({
                                        'id':sta_period_categories.id,
                                        'name':sta_period_categories.name_en,
                                        'sort':sta_period_categories.sort
                                })
                        elif lang == "lo":
                                results.append({
                                        'id':sta_period_categories.id,
                                        'name':sta_period_categories.name_lo,
                                        'sort':sta_period_categories.sort
                                })
                
                return ResponseSchema(
                code="200", status="Ok", message="foundData" ,result=results
                ).dict(exclude_none=True)
        except Exception as e:
           print(f"Error: {str(e)}")
        

@router.get("/get-all-period-category-recommend-web")
async def get_all_period_category_recommend_web(category_id:int ,offset:Optional[int]=None , limit:Optional[int]=None ,lang: str = Header(None), db: Session = Depends(get_db)):
        if lang is None:
                lang = "th"
        get_data_period = BaseRepo.get_period_category_rec(db,
                                                           Sta_station,
                                                           Sta_station_schedule,
                                                           Sta_station_period,
                                                           Sta_period_categories,
                                                           offset,
                                                           limit,
                                                           category_id)
        results = []
        for sta_stations,sta_station_schedules,sta_station_periods,sta_period_categories,TOTAL in get_data_period:
                if sta_station_periods.station_channel_id is not None:
                        results_member = []
                        channel_id = sta_station_periods.station_channel_id
                
                        member_detail = BaseRepo.get_produce(db,
                                                        Sta_station_channel,
                                                        Sta_channel,
                                                        Member,
                                                        channel_id
                                                        )
                
                        for sta_station_channels , sta_channels, members in member_detail:
                                results_member.append({
                                'id':members.id,
                                'first_name':members.first_name,
                                'last_name':members.last_name,
                                'display_name':members.display_name
                                })

                else:
                
                        member_id  = sta_station_periods.created_by
                        results_member = []
                        member_detail = BaseRepo.get_produce_none(db,
                                                                Member,
                                                                member_id)
                
                        results_member.append({
                        'id':member_detail.id,
                        'first_name':member_detail.first_name,
                        'last_name':member_detail.last_name,
                        'display_name':member_detail.display_name
                        })
                if sta_station_periods.object_key is None:
                        if lang == "th":
                                category_name = sta_period_categories.name_th
                        elif lang == "en":
                                category_name = sta_period_categories.name_en
                        elif lang == "lo":
                                category_name = sta_period_categories.name_lo
                        results.append({
                                'period_id':sta_station_periods.id,
                                'period_name':sta_station_periods.name,
                                'period_icon_path':None,
                                'period_category_id':sta_station_periods.period_category_id,
                                'category_id':sta_period_categories.id,
                                'category_name':category_name,
                                'period_broadcast_url':sta_station_periods.broadcast_url,
                                'prtiod_time_start':sta_station_periods.period_time_start,
                                'period_time_end':sta_station_periods.period_time_end,
                                'station_id':sta_stations.id,
                                'station_name':sta_stations.name,
                                'station_icon_path':sta_stations.icon_path,
                                'schedule_id':sta_station_schedules.id,
                                'schedule_number':sta_station_schedules.schedule_number,
                                'schedule_date':sta_station_schedules.shchedule_date,
                                'schedule_image':sta_station_schedules.icon_path,
                                'TOTAL':TOTAL,
                                'member':results_member
                        }) 
                
                else:
                        if lang == "th":
                                category_name = sta_period_categories.name_th
                        elif lang == "en":
                                category_name = sta_period_categories.name_en
                        elif lang == "lo":
                                category_name = sta_period_categories.name_lo

                        results.append({
                                'period_id':sta_station_periods.id,
                                'period_name':sta_station_periods.name,
                                'period_icon_path':sta_station_periods.icon_path,
                                'period_category_id':sta_station_periods.period_category_id,
                                'category_id':sta_period_categories.id,
                                'category_name':category_name,
                                'period_broadcast_url':sta_station_periods.broadcast_url,
                                'prtiod_time_start':sta_station_periods.period_time_start,
                                'period_time_end':sta_station_periods.period_time_end,
                                'station_id':sta_stations.id,
                                'station_name':sta_stations.name,
                                'station_icon_path':sta_stations.icon_path,
                                'schedule_id':sta_station_schedules.id,
                                'schedule_number':sta_station_schedules.schedule_number,
                                'schedule_date':sta_station_schedules.schedule_date,
                                'schedule_image':sta_station_schedules.icon_path,
                                'TOTAL':TOTAL,
                                'member':results_member
                        })

        

        if get_data_period == []:
                return ResponseSchema(
                code="200", status="Ok", message="notFoundData" ,result=results
                 ).dict(exclude_none=True)

        else:

                return ResponseSchema(
                code="200", status="Ok", message="foundData" ,result=results
                ).dict(exclude_none=True)



@router.get("/get-all-period-category-new-web")
async def get_all_period_category_recommend_web(category_id:int,offset:Optional[int]=None , limit:Optional[int]=None , db: Session = Depends(get_db)):               
        
        get_data_period_schedule = BaseRepo.get_period_schedule_cate_rec(db,
                                                           Sta_station_period,
                                                           Sta_station_schedule,
                                                           Sta_period_categories,
                                                           Sta_station,
                                                           offset,
                                                           limit,
                                                           category_id)
        
        
        results = []
        for sta_station_periods,sta_station_schedules,sta_period_categories,sta_stations in get_data_period_schedule:
                if sta_station_periods.station_channel_id is not None:
                                results_member = []
                                channel_id = sta_station_periods.station_channel_id
                        
                                member_detail = BaseRepo.get_produce(db,
                                                                Sta_station_channel,
                                                                Sta_channel,
                                                                Member,
                                                                channel_id
                                                                )
                        
                                for sta_station_channels , sta_channels, members in member_detail:
                                        results_member.append({
                                        'id':members.id,
                                        'first_name':members.first_name,
                                        'last_name':members.last_name,
                                        'display_name':members.display_name
                                        })

                else:
                        
                                member_id  = sta_station_periods.created_by
                                results_member = []
                                member_detail = BaseRepo.get_produce_none(db,
                                                                        Member,
                                                                        member_id)
                        
                                results_member.append({
                                'id':member_detail.id,
                                'first_name':member_detail.first_name,
                                'last_name':member_detail.last_name,
                                'display_name':member_detail.display_name 
                                })

                results.append({
                        'perid_id':sta_station_periods.id,
                        'period_name':sta_station_periods.name,
                        'period_icon_path':sta_station_periods.icon_path,
                        'period_category_id':sta_station_periods.period_category_id,
                        'category_id':sta_period_categories.id,
                        'category_name':sta_period_categories.name,
                        'schedule_date':sta_station_schedules.schedule_date,
                        'period_time_start':sta_station_periods.period_time_start,
                        'period_broadcast_url':sta_station_periods.broadcast_url,
                        'prtiod_time_start':sta_station_periods.period_time_start,
                        'period_time_end':sta_station_periods.period_time_end,
                        'station_id':sta_stations.id,
                        'station_name':sta_stations.name,
                        'station_icon_path':sta_stations.icon_path,
                        'schedule_id':sta_station_schedules.id,
                        'schedule_number':sta_station_schedules.schedule_number,
                        'schedule_date':sta_station_schedules.schedule_date,
                        'schedule_image':sta_station_schedules.icon_path,
                        'member':results_member
                })

        
        if get_data_period_schedule == []:
                return ResponseSchema(
                code="200", status="Ok", message="notFoundData" ,result=results
                 ).dict(exclude_none=True)

        else:

                return ResponseSchema(
                code="200", status="Ok", message="foundData" ,result=results
                ).dict(exclude_none=True)
        

@router.get("/get-all-station-like-web",dependencies=[Depends(JWTBearer())])
async def get_all_station_like_web(offset:Optional[int]=None , limit:Optional[int]=None ,token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
        decode_token = Ex_Decode.decode_token(token)
        user_id = decode_token["id"]
        
        get_data_station = BaseRepo.get_station_like_web(db,
                                                         Stat_customer_action_detail,
                                                         Sta_station,
                                                         offset,
                                                         limit,
                                                         user_id)
        results = []
        for item in get_data_station:
                results.append({
                        'cus_act_action_date':item[0],
                        'station_id':item[1],
                        'station_name':item[2],
                        'station_icon_path':item[3],
                        'station_approve_id':item[4]

                })
        
        if get_data_station == []:
                return ResponseSchema(
                code="200", status="Ok", message="notFoundData" ,result=results
                 ).dict(exclude_none=True)

        else:

                return ResponseSchema(
                code="200", status="Ok", message="foundData" ,result=results
                ).dict(exclude_none=True)
        

@router.get("/get-play-list-station-like-web")
async def get_all_station_like_web(station_id:Optional[int]=None,db: Session = Depends(get_db)):
        get_station_data_broadcast = BaseRepo.get_data_broadcast_by_id(db,
                                                                       Sta_station,
                                                                       Sta_station_schedule,
                                                                       Sta_station_period,
                                                                       station_id)
        results = [] 
        for sta_stations , sta_station_schedules , sta_station_periods in get_station_data_broadcast:
                
                results.append({
                        'id':sta_stations.id,
                        'period_broadcast_status_id':sta_station_periods.broadcast_status_id,
                        'schedule_date':sta_station_schedules.schedule_date,
                        'period_time_start':sta_station_periods.period_time_start
                })

        return ResponseSchema(
                code="200", status="Ok", message="foundData" ,result=results
                ).dict(exclude_none=True)


@router.get("/get-search-all-web")
async def get_search_all_web(keyword:Optional[str]=None,offset:Optional[int]=None,limit:Optional[int]=None,db: Session = Depends(get_db)):
        
        search_data_all = BaseRepo.search_data_all(db,
                                                   Sta_station,
                                                   keyword,
                                                   offset,
                                                   limit)
        
        results = []
        for sta_stations in search_data_all:
                results.append({
                        'id':sta_stations.id,
                        'name':sta_stations.name,
                        'description':sta_stations.description,
                        'code':sta_stations.code,
                        'icon_path':sta_stations.icon_path
                })

        return ResponseSchema(
                code="200", status="Ok", message="foundData" ,result=results
                ).dict(exclude_none=True)
        








        

        
        


        
        