from fastapi import APIRouter, Depends
from typing import List , Optional
from sqlalchemy import null
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from respository.repository import JWTRepo, JWTBearer, UsersRepo, BaseRepo
from schema import (
    ResponseSchema,
    ResultsResp
)
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
     Sta_station_statuses,
     Member,
     Customer,
     Sta_station_period,
     Stat_customer
     )
from datetime import datetime, timedelta,date
import pdb
from minio_handler import MinioHandler
from minio import Minio



router = APIRouter(
              prefix="",
              tags=['Dashboard'],
              responses ={404:{
                            'message' : "Not found"
              }}
              
)

# encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@router.get("/get-all-static-realtime",dependencies=[Depends(JWTBearer())])
async def get_all_static_realtime(db: Session = Depends(get_db)):
    all_count = []
    
    member = UsersRepo.find_all_member(db,Member)

    station = UsersRepo.find_all_station(db,Sta_station)

    status_boardcast = UsersRepo.find_all_station_schedule(db,Sta_station_schedule)


    all_count.append({
          'count_member':member,
          'count_station':station,
          'count_broadcast_status':status_boardcast,
          'online_member':30,
          'max_station_active': 20,
          'station_active':5,
          'max_list_active':50,
          'list_active':35
    })
    return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=all_count
    )

@router.get("/get-all-station-schedule",dependencies=[Depends(JWTBearer())])
async def get_all_station_schedule(date: Optional[date]=None,
                                   offset:Optional[int]=None,
                                   limit:Optional[int]=None,
                                   type:Optional[str]=None,
                                   order_by:Optional[str]=None,
                                   order_direction:Optional[str]=None,
                                   keyword:Optional[str]=None,
                                   db: Session = Depends(get_db)):
    result_all = []
    result_all_last = []
    results = BaseRepo.get_all_station_schedule(db , Sta_station_schedule , Member ,Sta_station , date , offset,limit , type , order_by , order_direction,keyword)
    results2 = BaseRepo.find_all_max_schedule_count(db,Sta_station_schedule , Member ,Sta_station , date , offset,limit , type , order_by , order_direction,keyword)
    results3 = BaseRepo.find_all_max_schedule_count_all(db,Sta_station_schedule)
    
    for sta_station_schedules, members ,sta_stations in results:

        bucket_name = 'stations'
        if sta_station_schedules.object_key is not None:
                
                object_name = sta_station_schedules.object_key
                url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
        else:
                url = None

        bucket_name2 = 'stations'
        if  sta_stations.object_key is not None:
                
                object_name2 = sta_stations.object_key
                url2 = MinioHandler().get_instance().presigned_get_object(bucket_name2, object_name2)
        else:
                url2 = None
        result_all.append({
          'id':sta_station_schedules.id,
          'schedule_number':sta_station_schedules.schedule_number,
          'name':sta_station_schedules.name,
          'process_status_id':sta_station_schedules.process_status_id,
          'broadcast_status_id':sta_station_schedules.broadcast_status_id,
          'stations_name':sta_stations.name,
          'member':{
            'first_name':members.first_name,
            'last_name' :members.last_name,
            'username':members.username
          },
          'icon_path_schedule':sta_station_schedules.icon_path,
          'icon_path_station':sta_stations.icon_path,
          'created':sta_station_schedules.created
         })
        
    result_all_last = [
         {
         'count_all':results3,
         'count_query':results2,
         'data':result_all
         }
         
    ]

    if results is None:
        return ResponseSchema(
        code="200", status="Ok", message="Data not Found", result=result_all_last
            ).dict(exclude_none=True)
    else:
        return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=result_all_last
            ).dict(exclude_none=True)
    





@router.get("/get-all-station",dependencies=[Depends(JWTBearer())])
async def get_all_station_schedule_popular(offset:Optional[int]=None,
                                           limit:Optional[int]=None,
                                           order_direction:Optional[str]=None,
                                           type:Optional[str]=None,
                                           keyword:Optional[str]=None, 
                                           db: Session = Depends(get_db)):
    results = BaseRepo.get_all_station_popular(db,Sta_station,Sta_station_statuses,Member,offset,limit,type,order_direction,keyword)
    results_count = BaseRepo.count_all_station_popular(db,Sta_station,Sta_station_statuses,Member,keyword)

    
    results_all = {}

    results_dict =[]
    for sta_stations , sta_station_statuses ,members  in results:
            

            member_id = sta_stations.created_by
            results_member_data = BaseRepo.find_data_member(db,Member,member_id)
            if results_member_data is None:
                data_member = None
            else:
                data_member = results_member_data.username

            
            results_dict.append({
                'id':sta_stations.id,
                'name':sta_stations.name,
                'owner':data_member,
                'icon_path':sta_stations.icon_path,
                'count_like':sta_stations.count_like,
                'count_share':sta_stations.count_share,
                'count_listen':sta_stations.count_listen,
                'station_status_id':sta_stations.station_status_id,
                'suspend_date_start':sta_stations.suspend_date_start,
                'suspend_date_end':sta_stations.suspend_date_end,
                'suspend_comment':sta_stations.suspend_comment,
                'disable_comment':sta_stations.disable_comment,
                'sta_station_statuses_id':sta_station_statuses.id,
                'sta_station_statuses_name':sta_station_statuses.name,
                'description':sta_stations.description,
                'username':members.username,
                'first_name':members.first_name,
                'last_name':members.last_name


            })


    results_all={
        'count_query':results_count,
        'data':results_dict
    }

    
    
    return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=results_all
    ).dict(exclude_none=True)


@router.get("/initial",summary="อย่างเอาอ่ะจารย์") #ข้างบน
async def get_all_initial(db: Session = Depends(get_db)):
    """
    สวัสดีครับ ผมชื่อมอสนะครับ
    """
    #ข้างล่าง
    
    _process_statues = BaseRepo.get_all_initial(db,Sta_process_statuses)
    _broadcast_statues = BaseRepo.get_all_initial_broadcast(db,Sta_broadcast_statuses)
    results = [{
         'process_status':[],
         'broadcast_status':[]
         }
    ]
    results_process = []

    results_broadcast = []
    
    for sta_process_statuses in _process_statues:
        results_process.append({
             'id':sta_process_statuses.id,
             'name':sta_process_statuses.name
        })

    for sta_broadcast_statuses in _broadcast_statues:
        results_broadcast.append({
             'id':sta_broadcast_statuses.id,
             'name':sta_broadcast_statuses.name,
             'style':sta_broadcast_statuses.style
        })
    
    results = [{
         'process_status':results_process,
         'broadcast_status':results_broadcast
    }]

    
    return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=results
    ).dict(exclude_none=True)

@router.get("/get-all-summary-dashboard",dependencies=[Depends(JWTBearer())])
async def get_all_summary_dashboard(db: Session = Depends(get_db)):
     results1 = BaseRepo.count_customer(db,
                                        Customer)
     
     results2 = BaseRepo.count_station(db,
                                      Sta_station)
     
     results3 = BaseRepo.summary_station_onair(db,
                                               Sta_station,
                                               Sta_station_schedule)
     
     results4 = BaseRepo.count_period(db,
                                      Sta_station_period)
     
     results5 = BaseRepo.sum_station_online(db,
                                            Stat_customer)
     
     results6 = BaseRepo.active_6_1(db,
                                               Sta_station,
                                               Sta_station_schedule)
     
     results7 = BaseRepo.active_6_2(db,
                                               Sta_station,
                                               Sta_station_schedule)
     
     results8 = BaseRepo.active_7_1(db,
                                               Sta_station,
                                               Sta_station_schedule)
     
     results9 = BaseRepo.active_7_2(db,
                                               Sta_station,
                                               Sta_station_schedule)
     
     
     results10 = BaseRepo.get_data_period_status_id(db,
                                                   Sta_station_period)
    
     
     results_all = []
     for item in results10:
          results_all.append({
            'period_status_id':item[0],
            'period_status_name':item[1],
            'count':item[2]   
          })
     
     main_results = []
     main_results = [{
          'all_user':results1,
          'all_station':results2,
          'sum_onair':results3,
          'all_period':results4,
          'station_online':results5[0].sum_status_online,
          'first_value_station_active':results6,
          'second_value_station_active':results7,
          'first_value_schedule_active':results8,
          'second_value_schedule_active':results9,
          'update_value':results_all

     }]
          
        
     
     
     return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=main_results
    ).dict(exclude_none=True)

@router.get("/get-all-station-popular",dependencies=[Depends(JWTBearer())])
async def get_all_summary_dashboard(db: Session = Depends(get_db)):
    get_data_popular = BaseRepo.get_data_station_popular(db,
                                Sta_station)
    all_results = []
    
    for item in get_data_popular:
            bucket_name = 'stations'
            if item[2] is not None:
                
                object_name = item[2]
                url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
            else:
                url = None
            all_results.append({
              'id':item[0],
              'name':item[1],
              'icon_path':url,
              'approve_status_id':item[3],
              'popular_score':item[4]
            })
         
    

     
    return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=all_results
    ).dict(exclude_none=True)



@router.get("/get-all-station-lasted",dependencies=[Depends(JWTBearer())])
async def get_all_station_lasted(db: Session = Depends(get_db)):
     get_station_lasted = BaseRepo.get_lasted(db,
                                              Sta_station,
                                              Sta_station_schedule,
                                              Sta_station_period,
                                              Member)
    
     results_all = []
     for sta_stations , sta_station_schedules , sta_station_periods , members ,broadcast_status_name_case in get_station_lasted:
          
          results_all.append({
               'id':sta_stations.id,
               'name':sta_stations.name,
               'icon_path':sta_stations.icon_path,
               'schedule_id':sta_station_schedules.id,
               'schedule_number':sta_station_schedules.schedule_number,
               'schedule_icon_path':sta_station_schedules.icon_path,
               'schedule_name':sta_station_schedules.name,
               'schedule_date':sta_station_schedules.schedule_date,
               'broadcast_status_name_case':broadcast_status_name_case,
               'member_id':members.id,
               'username':members.username,
               'first_name':members.first_name,
               'last_name':members.last_name,
               'process_status_id':sta_station_schedules.process_status_id,
               'broadcast_status_id':sta_station_periods.broadcast_status_id


          })

     return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=results_all
     ).dict(exclude_none=True)
          
     
     












