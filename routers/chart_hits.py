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
    Insertcustomerinterest,
    Createcustomeractionweb
)
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from respository.web_repository import JWTRepo, JWTBearer,Ex_Decode
from passlib.context import CryptContext
from respository.repo_chart_hits import BaseRepo

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
              tags=['chart_hits'],
              responses ={404:{
                            'message' : "Not found"
              }}
              
)


@router.get("/get-all-month-charthitz-web")
async def get_all_month_charthitz_web(db: Session = Depends(get_db)):
        try:
                get_data_hitz = BaseRepo.data_month_hitz(db,
                                                        Stat_customer_action_detail)
                results = []

                for item in get_data_hitz:
                        results.append({
                                'month':int(item[0]),
                                'TOTAL':item[1]
                        })


                return ResponseSchema(
                        code="200", status="Ok", message="foundData" ,result=results
                        ).dict(exclude_none=True)
        except Exception as e:
           print(f"Error: {str(e)}")


@router.get("/get-sum-action-month-web")
async def get_sum_action_month_web(month:Optional[int]=None , db: Session = Depends(get_db)):
        get_data_sum = BaseRepo.get_count_action(db,
                                                 Stat_customer_action_detail,
                                                 Sta_station,
                                                 month)
        
        if (get_data_sum[0] == None and get_data_sum[1] == None and  get_data_sum[2] == None):
              return ResponseSchema(
                code="200", status="Ok", message="dataNotFound"
                ).dict(exclude_none=True)

        else:
              results = {
                            'count_listen':int(get_data_sum[0]),
                            'count_like':int(get_data_sum[1]),
                            'count_share':int(get_data_sum[2])
              }


              return ResponseSchema(
                            code="200", status="Ok", message="foundData" ,result=results
                            ).dict(exclude_none=True)


@router.get("/get-list-station-month-web")
async def get_list_station_month_web(month:Optional[int]=None , db: Session = Depends(get_db)):
        
        list_station_month_web = BaseRepo.get_list_station_month(db,
                                                                 Sta_station,
                                                                 Stat_customer_action_detail,
                                                                 month
                                                                 )
        
        
        
        results = []
        for sta_stations , TOTAL in list_station_month_web:
                customer_id = sta_stations.id
                
                results_status = []
                get_status_offline = BaseRepo.get_check_status_offline(db,
                                                                       Sta_station,
                                                                       Sta_station_schedule,
                                                                       Sta_station_period,
                                                                       Stat_customer_action_detail,
                                                                       customer_id,
                                                                       month)
                
                for item in get_status_offline:
                        if get_status_offline is not None:
                                results_status.append({
                                        'id':item[0],
                                        'icon_path':item[1],
                                        'name':item[2],
                                        'status':item[3],
                                        'min_schedule_date':item[4],
                                        'min_period_time_start':item[5],
                                        'max_period_time_end':item[6]
                                })
                        else:
                                results_status.append({
                                        'id':None,
                                        'icon_path':None,
                                        'name':None,
                                        'status':None,
                                        'min_schedule_date':None,
                                        'min_period_time_start':None,
                                        'max_period_time_end':None
                                })
                        
                results.append({
                                'id':sta_stations.id,
                                'icon_path':sta_stations.icon_path,
                                'name':sta_stations.name,
                                'TOTAL':TOTAL,
                                'status':results_status
        })
        
        
        
        return ResponseSchema(
                code="200", status="Ok", message="foundData" ,result=results
                ).dict(exclude_none=True)
        

@router.get("/get-playlist-month-web")
async def get_playlist_month_web(
                                 month:Optional[int]=None ,
                                 station_id:Optional[int]=None,
                                 db: Session = Depends(get_db)):
        
              
              
              
                        get_data_all = BaseRepo.get_playlist_month_only(db,
                                                                     Sta_station,
                                                                     Sta_station_schedule,
                                                                     Sta_station_period,
                                                                     Stat_customer_action_detail,
                                                                     station_id,
                                                                     month)
                            
                        results = []
                            
                        for sta_stations , sta_station_schedules, sta_station_periods   in get_data_all:
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
                                        
                                                        'station_id':sta_stations.id,
                                                        'station_name':sta_stations.name,
                                                        'station_icon_path':sta_stations.icon_path,
                                                        'schedule_id':sta_station_schedules.id,
                                                        'schedule_number':sta_station_schedules.schedule_number,
                                                        'schedule_date':sta_station_schedules.schedule_date,
                                                        'period_id':sta_station_periods.id,
                                                        'period_icon_path':sta_station_periods.icon_path,
                                                        'period_name':sta_station_periods.name,
                                                        'period_time_start':sta_station_periods.period_time_start,
                                                        'period_time_end':sta_station_periods.period_time_end,
                                                        'period_broadcast_url':sta_station_periods.broadcast_url,
                                                        'period_broadcast_status_id':sta_station_periods.broadcast_status_id,
                                                        'period_broadcast_type_id':sta_station_periods.broadcast_type_id,
                                                        'member':results_member
                                          
                                        
                                                })
                                          
                                         

                        return ResponseSchema(
                            code="200", status="Ok", message="foundData" ,result=results
                            ).dict(exclude_none=True)
                      

