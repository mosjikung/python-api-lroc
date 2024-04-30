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
    Insertcustomerinterest
)
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from respository.web_repository import JWTRepo, JWTBearer,Ex_Decode
from passlib.context import CryptContext
from respository.repo_after_login import BaseRepo

from model import (
     Users , 
     Sta_station ,
     Stat_customer,
     Sta_station_schedule,
     Stat_customer_action_detail,
     Stat_customer_interest,
     Sta_station_period,
     Member,
     Sta_channel,
     Sta_station_channel
     

     )
from datetime import datetime, timedelta
import pdb
from minio_handler import MinioHandler
from minio import Minio


router = APIRouter(
              prefix="",
              tags=['after_login'],
              responses ={404:{
                            'message' : "Not found"
              }}
              
)


@router.get('/get-all-station-popular-web')
async def get_all_station_popular_web( offset:int , limit:int , keyword:Optional[str] = None, db: Session = Depends(get_db)):

              get_all_data_pop = BaseRepo.get_station_popular(db,
                                                              Sta_station,
                                                              offset,
                                                              limit,
                                                              keyword)
                                                 
              results = []
              for x , TOTAL in get_all_data_pop:
                      
                    results.append({
                            'id':x.id,
                            'name':x.name,
                            'icon_path':x.icon_path,
                            'approve_status_id':x.approve_status_id,
                            'count':TOTAL
                    })
                      
              return ResponseSchema(
            code="200", status="Ok", message="Success save data" ,result=results
             ).dict(exclude_none=True)


@router.get('/get-all-period-popular-web')
async def get_all_station_popular_web(offset:Optional[int]=None,limit:Optional[int]=None,keyword:Optional[str]=None, db: Session = Depends(get_db)):

              get_all_data_pop = BaseRepo.get_period_popular(db,
                                                             Sta_station,
                                                             Sta_station_schedule,
                                                             Sta_station_period,
                                                             offset,
                                                             limit,
                                                             keyword
                                                             )
              results = []
              for sta_stations , sta_station_schedules, sta_station_periods,  TOTAL in get_all_data_pop:
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
                                'display_name':members.display_name,
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
                      bucket_name = 'stations'
                      if sta_station_periods.object_key is not None:
                    
                          object_name = sta_station_periods.object_key
                  
                          url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
                  
                 
                      else:
                          url = None
                      results.append({
                              'station_id':sta_stations.id,
                              'schedule_id':sta_station_schedules.id,
                              'period_id':sta_station_periods.id,
                              'period_name':sta_station_periods.name,
                              'icon_path':url,
                              'count':TOTAL,
                              'member':results_member
                      })
                      
              return ResponseSchema(
            code="200", status="Ok", message="Success save data" ,result=results
             ).dict(exclude_none=True)


@router.post('/insert-customer-interest-web',dependencies=[Depends(JWTBearer())])
async def get_all_station_popular_web(data:List[Insertcustomerinterest], token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
        time_update = datetime.now()
        decode_token = Ex_Decode.decode_token(token)
        user_id = decode_token["id"]
        user_name = decode_token["sub"]
        
        for item in data:
            insert_data = Stat_customer_interest(
                    station_id = item.station_id,
                    schedule_id = item.schedule_id,
                    period_id = item.period_id,
                    customer_id = user_id,
                    is_active = True,
                    created = time_update,
                    created_by = user_id,
                    modified = None,
                    modified_by = None
            )
            results = BaseRepo.insert(db, insert_data)
        if results == True:
            return ResponseSchema(
            code="200", status="Ok", message="Success insert data"
             ).dict(exclude_none=True)
        else:
             return ResponseSchema(
            code="200", status="Ok", message="Can't Insert Data"
             ).dict(exclude_none=True)
        

@router.get("/get-all-period-lastime-web",dependencies=[Depends(JWTBearer())])
async def get_all_station_popular_web(offset:Optional[int]=None , limit:Optional[int]=None , token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
        try:
            time_update = datetime.now()
            decode_token = Ex_Decode.decode_token(token)
            user_id = decode_token["id"]

            get_last_data = BaseRepo.get_lastime_listen(db,
                                                        Stat_customer_action_detail,
                                                        Sta_station,
                                                        user_id,
                                                        offset,
                                                        limit)
            results  = []
            for item in get_last_data:
                results.append({
                        'id':item[0],
                        'name':item[1],
                        'icon_path':item[2],
                        'approve_status_id':item[3],
                        'action_date':item[4],
                })


            return ResponseSchema(
                code="200", status="Ok", message="foundData",result=results
                ).dict(exclude_none=True)
        except Exception as e:
           print(f"Error: {str(e)}")
        


