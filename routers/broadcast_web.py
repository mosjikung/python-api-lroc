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
from respository.repo_broadcast_web import BaseRepo

from model import (
     Users , 
     Sta_station , 
     Sta_station_schedule,
     Sta_broadcast,
     Sta_station_period,
     Sta_station_playlist,
     Sta_station_schedule_activitie,
     Sta_station_channel,
     Sta_channel,
     Member
     

     )
from datetime import datetime, timedelta
import pdb
from minio_handler import MinioHandler
from minio import Minio


router = APIRouter(
              prefix="",
              tags=['broadcast_web'],
              responses ={404:{
                            'message' : "Not found"
              }}
              
)


@router.get("/get-station-schedule-broadcast-web")
async def get_station_schedule_broadcast(
                                         station_id:Optional[int]=None,
                                         offset:Optional[str]=None,
                                         limit:Optional[int]=None,
                                         order_direction:Optional[str]=None,
                                         db: Session = Depends(get_db)):
    try:
        results_record = []
        results_data=[]
        
        results = BaseRepo.get_data_broadcast(db,Sta_station,Sta_station_schedule,Sta_station_period,offset,limit,order_direction,station_id)
        
        for sta_stations , sta_station_schedules , sta_station_periods in results:
                
                
                
                
                
        
                
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
                                'username':members.username,
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
                        'username':member_detail.username,
                        'display_name':member_detail.display_name
                        })

                results_data.append({
                        'station_id':sta_stations.id,
                        'station_name':sta_stations.name,
                        'icon_path':sta_stations.icon_path,
                        'is_enabled':sta_stations.is_enabled,
                        'station_status_id':sta_stations.station_status_id,
                        'disable_comment':sta_stations.disable_comment,
                        'schedule_date':sta_station_schedules.schedule_date,
                        'broadcast_status_id':sta_station_schedules.broadcast_status_id,
                        'schedule_id':sta_station_schedules.id,
                        'schedule_number':sta_station_schedules.schedule_number,
                        'schedule_modified':sta_station_schedules.modified,
                        'schedule_icon_path':sta_station_schedules.icon_path,
                        'period_id':sta_station_periods.id,
                        'period_broadcast_status_id':sta_station_periods.broadcast_status_id,
                        'period_time_start':sta_station_periods.period_time_start,
                        'period_time_end':sta_station_periods.period_time_end,
                        'description':sta_station_periods.description,
                        'period_name':sta_station_periods.name,
                        'period_channel_id':sta_station_periods.channel_id,
                        'period_image':sta_station_periods.icon_path,
                        'period_description':sta_station_periods.description,
                        'broadcast_url':sta_station_periods.broadcast_url,
                        'period_broadcast_type_id':sta_station_periods.broadcast_type_id,
                        'member':results_member
                        })


        return ResponseSchema(
                code="200", status="Ok", message="Sucess retrieve data", result=results_data
        ).dict(exclude_none=True)
    
    except Exception as e:
           print(f"Error: {str(e)}")