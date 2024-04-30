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
    Updatechannelstatus
)
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from respository.repository import JWTRepo, JWTBearer, UsersRepo ,Ex_Decode
from passlib.context import CryptContext
from respository.repo_channel import BaseRepo

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
     Sta_channel_periods,
     Sta_channel_playlists,
     Member,
     Countries
     )

from datetime import datetime, timedelta
import pdb
from minio_handler import MinioHandler
from minio import Minio


router = APIRouter(
              prefix="",
              tags=['channel'],
              responses ={404:{
                            'message' : "Not found"
              }}
              
)


# encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""
    Authentication Router
"""


@router.get("/get-all-station-channels",summary="sta_station,sta_channel,members,sta_station_channels",dependencies=[Depends(JWTBearer())])
async def get_station_schedule_broadcast(offset:Optional[str]=None,
                                         limit:Optional[int]=None,
                                         keyword:Optional[str]=None,
                                         db: Session = Depends(get_db)):
    
        
        
        get_data_all_station_channels = BaseRepo.get_data_station_channels(db,
                                                                           Sta_station_channel,
                                                                           Sta_station,
                                                                           Member,
                                                                           Sta_channel,
                                                                           offset,
                                                                           limit,
                                                                           keyword,
                                                                           )
        get_count_data_station_channels = BaseRepo.get_count_data_station_channel(db,
                                                                           Sta_station_channel,
                                                                           Sta_station,
                                                                           Member,
                                                                           Sta_channel,
                                                                           keyword,)
        
        get_count_data_station_channels_delete = BaseRepo.get_count_data_station_channel_delete_none_keyword(db,
                                                                           Sta_station_channel,
                                                                           Sta_station,
                                                                           Member,
                                                                           Sta_channel)
        
        get_count_data_station_channels_cancle = BaseRepo.get_count_data_station_channel_cancle_none_keyword(db,
                                                                           Sta_station_channel,
                                                                           Sta_station,
                                                                           Member,
                                                                           Sta_channel)
        
        results_data = []
        results_all = []
        if get_data_all_station_channels != [] :
              
              for sta_station_channel, sta_station,member,sta_channel in get_data_all_station_channels:
                     results_data.append({
                            'member_id':member.id,
                            'member_username':member.username,
                            'member_first_name':member.first_name,
                            'member_last_name':member.last_name,
                            'member_email_verify':member.email_verify,
                            'member_display_name':member.display_name,
                            'station_id':sta_station.id,
                            'station_name':sta_station.name,
                            'station_icon_path':sta_station.icon_path,
                            'sta_channel_id':sta_channel.id,
                            'sta_channel_name':sta_channel.name,
                            'sta_channel_icon_path':sta_channel.icon_path,
                            'sta_channel_url_channel':sta_channel.url_channel,
                            'sta_station_channel_accept_date':sta_station_channel.accept_date,
                            'member_type_id':member.member_type_id,
                            'member_avatar_img':member.avatar_img,
                            'sta_station_channel_id':sta_station_channel.id
                     })
                     
              results_all = ({
                     'count_station_channel':get_count_data_station_channels,
                     'count_station_channel_deleted':get_count_data_station_channels_delete,
                     'count_station_channel_ban':get_count_data_station_channels_cancle,
                     'data':results_data
              })
              return ResponseSchema(
                 code="200", status="Ok", message="foundData" , result=results_all
                ).dict(exclude_none=True)
        else:
              results_all = ({
                     'count_station_channel':get_count_data_station_channels,
                     'count_station_channel_deleted':get_count_data_station_channels_delete,
                     'count_station_channel_ban':get_count_data_station_channels_cancle,
                     'data':results_data
              }) 
              return ResponseSchema(
                 code="200", status="Ok", message="canNotFoundData" , result=results_all
                ).dict(exclude_none=True)
                

@router.get("/get-all-station-channels_cancle",summary="sta_station,sta_channel,members,sta_station_channels",dependencies=[Depends(JWTBearer())])
async def get_station_schedule_broadcast(offset:Optional[str]=None,
                                         limit:Optional[int]=None,
                                         keyword:Optional[str]=None,
                                         db: Session = Depends(get_db)):
    
        
        
        get_data_all_station_channels = BaseRepo.get_data_station_channels_cancle(db,
                                                                           Sta_station_channel,
                                                                           Sta_station,
                                                                           Member,
                                                                           Sta_channel,
                                                                           offset,
                                                                           limit,
                                                                           keyword,
                                                                           )
        get_count_data_station_channels = BaseRepo.get_count_data_station_channel_none_keyword(db,
                                                                           Sta_station_channel,
                                                                           Sta_station,
                                                                           Member,
                                                                           Sta_channel)
        
        get_count_data_station_channels_delete = BaseRepo.get_count_data_station_channel_delete_none_keyword(db,
                                                                           Sta_station_channel,
                                                                           Sta_station,
                                                                           Member,
                                                                           Sta_channel)
        
        get_count_data_station_channels_cancle = BaseRepo.get_count_data_station_channel_cancle(db,
                                                                           Sta_station_channel,
                                                                           Sta_station,
                                                                           Member,
                                                                           Sta_channel,
                                                                           keyword)
        
        results_data = []
        results_all = []
        if get_data_all_station_channels != [] :
              
              for sta_station_channel, sta_station,member,sta_channel in get_data_all_station_channels:
                     results_data.append({
                            'member_id':member.id,
                            'member_username':member.username,
                            'member_first_name':member.first_name,
                            'member_last_name':member.last_name,
                            'member_email_verify':member.email_verify,
                            'member_display_name':member.display_name,
                            'station_id':sta_station.id,
                            'station_name':sta_station.name,
                            'station_icon_path':sta_station.icon_path,
                            'sta_channel_id':sta_channel.id,
                            'sta_channel_name':sta_channel.name,
                            'sta_channel_icon_path':sta_channel.icon_path,
                            'sta_channel_url_channel':sta_channel.url_channel,
                            'sta_station_channel_accept_date':sta_station_channel.accept_date,
                            'member_type_id':member.member_type_id,
                            'member_avatar_img':member.avatar_img,
                            'sta_station_channel_id':sta_station_channel.id
                     })
                     
              results_all = ({
                     'count_station_channel':get_count_data_station_channels,
                     'count_station_channel_deleted':get_count_data_station_channels_delete,
                     'count_station_channel_ban':get_count_data_station_channels_cancle,
                     'data':results_data
              })
              return ResponseSchema(
                 code="200", status="Ok", message="foundData" , result=results_all
                ).dict(exclude_none=True)
        else:
              results_all = ({
                     'count_station_channel':get_count_data_station_channels,
                     'count_station_channel_deleted':get_count_data_station_channels_delete,
                     'count_station_channel_ban':get_count_data_station_channels_cancle,
                     'data':results_data
              })
              return ResponseSchema(
              code="200", status="Ok", message="canNotFoundData" , result=results_all
              ).dict(exclude_none=True)
                


@router.get("/get-all-station-channels_delete",summary="sta_station,sta_channel,members,sta_station_channels",dependencies=[Depends(JWTBearer())])
async def get_station_schedule_broadcast(offset:Optional[str]=None,
                                         limit:Optional[int]=None,
                                         keyword:Optional[str]=None,
                                         db: Session = Depends(get_db)):
    
        
        
        get_data_all_station_channels = BaseRepo.get_data_station_channels_delete(db,
                                                                           Sta_station_channel,
                                                                           Sta_station,
                                                                           Member,
                                                                           Sta_channel,
                                                                           offset,
                                                                           limit,
                                                                           keyword,
                                                                           )
        get_count_data_station_channels = BaseRepo.get_count_data_station_channel_none_keyword(db,
                                                                           Sta_station_channel,
                                                                           Sta_station,
                                                                           Member,
                                                                           Sta_channel)
        
        get_count_data_station_channels_delete = BaseRepo.get_count_data_station_channel_delete(db,
                                                                           Sta_station_channel,
                                                                           Sta_station,
                                                                           Member,
                                                                           Sta_channel,
                                                                           keyword)
        
        get_count_data_station_channels_cancle = BaseRepo.get_count_data_station_channel_cancle_none_keyword(db,
                                                                           Sta_station_channel,
                                                                           Sta_station,
                                                                           Member,
                                                                           Sta_channel)
        
        results_data = []
        results_all = []
        if get_data_all_station_channels != [] :
              
              for sta_station_channel, sta_station,member,sta_channel in get_data_all_station_channels:
                     results_data.append({
                            'member_id':member.id,
                            'member_username':member.username,
                            'member_first_name':member.first_name,
                            'member_last_name':member.last_name,
                            'member_email_verify':member.email_verify,
                            'member_display_name':member.display_name,
                            'station_id':sta_station.id,
                            'station_name':sta_station.name,
                            'station_icon_path':sta_station.icon_path,
                            'sta_channel_id':sta_channel.id,
                            'sta_channel_name':sta_channel.name,
                            'sta_channel_icon_path':sta_channel.icon_path,
                            'sta_channel_url_channel':sta_channel.url_channel,
                            'sta_station_channel_accept_date':sta_station_channel.accept_date,
                            'member_type_id':member.member_type_id,
                            'member_avatar_img':member.avatar_img,
                            'sta_station_channel_id':sta_station_channel.id
                     })
                     
              results_all = ({
                     'count_station_channel':get_count_data_station_channels,
                     'count_station_channel_deleted':get_count_data_station_channels_delete,
                     'count_station_channel_ban':get_count_data_station_channels_cancle,
                     'data':results_data
              })
              return ResponseSchema(
                 code="200", status="Ok", message="foundData" , result=results_all
                ).dict(exclude_none=True)
        else:
              results_all = ({
                     'count_station_channel':get_count_data_station_channels,
                     'count_station_channel_deleted':get_count_data_station_channels_delete,
                     'count_station_channel_ban':get_count_data_station_channels_cancle,
                     'data':results_data
              })
              return ResponseSchema(
              code="200", status="Ok", message="canNotFoundData" , result=results_all
              ).dict(exclude_none=True)
        

@router.patch("/update-channels-status-cancel",summary="sta_station_channels",dependencies=[Depends(JWTBearer())])
async def get_station_schedule_broadcast(
                                         request:Updatechannelstatus,
                                         token: str = Depends(JWTBearer()),
                                         db: Session = Depends(get_db)):
       
              update_time = datetime.now()
              decode_token = Ex_Decode.decode_token(token)
              user_id = decode_token['id']
              prepair_data_update = BaseRepo.get_data_prepair_update_cancel(db,
                                                                     Sta_channel,
                                                                     request.sta_station_channel_id,
                                                                     user_id,
                                                                     update_time
                                                                     )
              
              if prepair_data_update is not None:
                            results_update = BaseRepo.update(db,prepair_data_update)

                            if results_update == True:
                                    return ResponseSchema(
                                          code="200", status="Ok", message="upDateDataSuccess"
                                          ).dict(exclude_none=True)
                            else:
                                    return ResponseSchema(
                                          code="200", status="Ok", message="upDateDataNotSuccess"
                                          ).dict(exclude_none=True)
              
              else:
                      
                            return ResponseSchema(
                            code="200", status="Ok", message="canNotFoundData"
                            ).dict(exclude_none=True)
              
@router.patch("/update-channels-status-delete",summary="sta_station_channels",dependencies=[Depends(JWTBearer())])
async def get_station_schedule_broadcast(
                                         request:Updatechannelstatus,
                                         token: str = Depends(JWTBearer()),
                                         db: Session = Depends(get_db)):
       
              update_time = datetime.now()
              decode_token = Ex_Decode.decode_token(token)
              user_id = decode_token['id']
              prepair_data_update = BaseRepo.get_data_prepair_update_delete(db,
                                                                     Sta_channel,
                                                                     request.sta_station_channel_id,
                                                                     user_id,
                                                                     update_time
                                                                     )
              
              if prepair_data_update is not None:
                            results_update = BaseRepo.update(db,prepair_data_update)

                            if results_update == True:
                                    return ResponseSchema(
                                          code="200", status="Ok", message="upDateDataSuccess"
                                          ).dict(exclude_none=True)
                            else:
                                    return ResponseSchema(
                                          code="200", status="Ok", message="upDateDataNotSuccess"
                                          ).dict(exclude_none=True)
              
              else:
                      
                            return ResponseSchema(
                            code="200", status="Ok", message="canNotFoundData"
                            ).dict(exclude_none=True)
                            
       

@router.get("/get-channel-by-id",summary="sta_station_channels,sta_channel,sta_station,member,sta_playlist")
async def get_station_schedule_broadcast(
                                         channel_id:int,
                                         #token: str = Depends(JWTBearer()),
                                         db: Session = Depends(get_db)):
       
       results = []
       get_all_data_by_id = BaseRepo.get_data_channel_by_id(db,
                                                            Sta_station_channel,
                                                            Sta_channel,
                                                            Countries,
                                                            channel_id)
      
       for station_channel , channel , country in get_all_data_by_id:
              
              
              station_id = station_channel.station_id
              results_station = []
              get_data_station = BaseRepo.get_data_station(db,
                                                           Sta_station,
                                                           station_id)
              for item in get_data_station:
                     results_station.append({
                            'id':item.id,
                            'name':item.name,
                            'image':item.icon_path
                     })
              
              results_member = []
              member_id = station_channel.created_by
              get_data_member = BaseRepo.get_data_station(db,
                                                         Member,
                                                         member_id)
              for item in get_data_member:
                     results_member.append({
                            'id':item.id,
                            'username':item.username,
                            'display_name':item.display_name,
                            'first_name':item.first_name,
                            'last_name':item.last_name,
                            'image':item.avatar_img,
                            'email':item.email_verify,
                            'phone_number':item.phone_number
                     })

              sta_channel_id = channel.id
              get_data_period = BaseRepo.get_data_period(db,
                                                         Sta_channel_periods,
                                                         sta_channel_id)
              
              for item in get_data_period:
                     channel_playlist_id = item.id
                     results_playlist = []
                     get_data_playlist = BaseRepo.get_data_playlist(db,
                                                                  Sta_channel_playlists,
                                                                  channel_playlist_id)
                     for playlist in get_data_playlist:
                            results_playlist.append({
                                    'id':playlist.id,
                                    'name':playlist.file_name,
                                    'image':item.icon_path,
                                    'file':playlist.file_path,
                                    'created_date':playlist.created,
                                    'modified_date':playlist.modified
                            })

              results.append({
                     'id':channel.id,
                     'name':channel.name,
                     'description':channel.description,
                     'image':channel.icon_path,
                     'country_name':country.name,
                     'count_like':channel.count_like,
                     'count_share':channel.count_share,
                     'count_listen':channel.count_listen,
                     'count_comment':channel.count_comment,
                     'invite_date':station_channel.invite_date,
                     'accept_date':station_channel.accept_date,
                     'created_date':station_channel.created,
                     'modified_date':station_channel.modified,
                     'station':results_station,
                     'created_by':results_member,
                     'playlist':results_playlist

              })

              if results != []:
                     return ResponseSchema(
                     code="200", status="Ok", message="foundData" , result=results
                     ).dict(exclude_none=True)
              

              

              
              

       
       
