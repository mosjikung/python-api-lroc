from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, null,or_ ,func , cast ,Date ,asc,case


from datetime import datetime, timedelta ,date
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM


from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from model import (Sta_station , 
                   Sta_station_schedule ,
                   Member,
                   Users,
                   Sta_station_period,
                   Sta_station_playlist_activities,
                   Sta_station_playlist_comments,
                   )

import pdb




T = TypeVar("T")



class BaseRepo:
 
 @staticmethod
 def count_type_1(db: Session,
                         Sta_station_schedule:Sta_station_schedule,
                         Sta_station_period:Sta_station_period,
                         Users):
    broadcast_status_case = case(
                                            
                                        (Sta_station_period.broadcast_status_id == 3, 'รอออกอากาศ')
                                           
                                        ).label('broadcast_status')
               
    process_status_case  = case(
                                        
                                            (Sta_station_period.period_status_id == 3, 'ส่งออกอากาศ'),
                                            (Sta_station_period.period_status_id== 6, 'ขอให้ปรับแก้'),
                                            (Sta_station_period.period_status_id == 7, 'ส่งผลการแก้ไข'),
                                            (Sta_station_period.period_status_id == 8, 'ปิดงานแก้ไข')
                                        
                                        ).label('period_status')
    
    results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 2)
                            .filter(Sta_station_period.broadcast_type_id == 1)
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .count()
                    )
    return results
 
 @staticmethod
 def count_type_2(db: Session,
                         Sta_station_schedule:Sta_station_schedule,
                         Sta_station_period:Sta_station_period,
                         Users):
     
     
    broadcast_status_case = case(
                                            
                                        (Sta_station_period.broadcast_status_id == 3, 'รอออกอากาศ')
                                           
                                        ).label('broadcast_status')
               
    process_status_case  = case(
                                        
                                            (Sta_station_period.period_status_id == 3, 'ส่งออกอากาศ'),
                                            (Sta_station_period.period_status_id== 6, 'ขอให้ปรับแก้'),
                                            (Sta_station_period.period_status_id == 7, 'ส่งผลการแก้ไข'),
                                            (Sta_station_period.period_status_id == 8, 'ปิดงานแก้ไข')
                                        
                                        ).label('period_status')
    
    results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 3)
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .count()
                    )
    return results
 

 @staticmethod
 def count_type_3(db: Session,
                         Sta_station_schedule:Sta_station_schedule,
                         Sta_station_period:Sta_station_period,
                         Users):
     
     
    broadcast_status_case = case(
                                            
                                        (Sta_station_period.broadcast_status_id == 3, 'รอออกอากาศ')
                                           
                                        ).label('broadcast_status')
               
    process_status_case  = case(
                                        
                                            (Sta_station_period.period_status_id == 3, 'ส่งออกอากาศ'),
                                            (Sta_station_period.period_status_id== 6, 'ขอให้ปรับแก้'),
                                            (Sta_station_period.period_status_id == 7, 'ส่งผลการแก้ไข'),
                                            (Sta_station_period.period_status_id == 8, 'ปิดงานแก้ไข')
                                        
                                        ).label('period_status')
    
    results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 4)
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .count()
                    )
    return results
 
 @staticmethod
 def count_type_4(db: Session,
                         Sta_station_schedule:Sta_station_schedule,
                         Sta_station_period:Sta_station_period,
                         Users):
     
     
    broadcast_status_case = case(
                                            
                                        (Sta_station_period.broadcast_status_id == 3, 'รอออกอากาศ')
                                           
                                        ).label('broadcast_status')
               
    process_status_case  = case(
                                        
                                            (Sta_station_period.period_status_id == 3, 'ส่งออกอากาศ'),
                                            (Sta_station_period.period_status_id== 6, 'ขอให้ปรับแก้'),
                                            (Sta_station_period.period_status_id == 7, 'ส่งผลการแก้ไข'),
                                            (Sta_station_period.period_status_id == 8, 'ปิดงานแก้ไข')
                                        
                                        ).label('period_status')
    
    results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 5)
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .count()
                    )
    return results



 def find_all_station_schedule(db: Session,
                         Sta_station:Sta_station,
                         Sta_station_schedule:Sta_station_schedule,
                         Sta_station_period:Sta_station_period,
                         Users,
                         offset,
                         limit:int,
                         type:str,
                         order_direction:str,
                         keyword:str):

               if keyword is not None:
                 search = "%{}%".format(keyword)
               if keyword == '':
                keyword = None
               if order_direction is None:
                 order_direction = 'asc'
               if type is None:
                 type = 'onair'
                
               broadcast_status_case = case(
                                            
                                        (Sta_station_period.broadcast_status_id == 3, 'รอออกอากาศ')
                                           
                                        ).label('broadcast_status')
               
               process_status_case  = case(
                                        
                                            (Sta_station_period.period_status_id == 3, 'ส่งออกอากาศ'),
                                            (Sta_station_period.period_status_id== 6, 'ขอให้ปรับแก้'),
                                            (Sta_station_period.period_status_id == 7, 'ส่งผลการแก้ไข'),
                                            (Sta_station_period.period_status_id == 8, 'ปิดงานแก้ไข')
                                        
                                        ).label('period_status')
               
               if  type == 'onair' and keyword is None:
                    print("1")
                    results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 2)
                            .filter(Sta_station_period.broadcast_type_id == 1)
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.schedule_number),asc(Sta_station_period.period_time_start))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               elif type == 'onair' and keyword is not None:
                   
                    results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 2)
                            .filter(Sta_station_period.broadcast_type_id == 1)
                            .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search)))
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_period.period_time_start),asc(Sta_station_schedule.schedule_number))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               

               elif type == 'edit'  and keyword is None:
                    print("5")
                    print("1")
                    results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 3)
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.schedule_number),asc(Sta_station_period.period_time_start))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               elif type == 'edit' and keyword is not None:
                   results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 3)
                            .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search)))
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.schedule_number),asc(Sta_station_period.period_time_start))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )

               

               elif type == 'send_edit' and keyword is None:
                    results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 4)
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.schedule_number),asc(Sta_station_period.period_time_start))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               elif type == 'send_edit' and keyword is not None:
                   results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 4)
                            .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search)))
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.schedule_number),asc(Sta_station_period.period_time_start))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )

               

               elif type == 'close_edit' and keyword is None:
                    print("13")
                    results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 5)
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.schedule_number),asc(Sta_station_period.period_time_start))
                    .limit(limit)
                    .all()
                    )
               elif type == 'close_edit' and keyword is not None:
                   print("14")
                   results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 5)
                            .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search)))
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.schedule_number),asc(Sta_station_period.period_time_start))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )

               

               return results


 @staticmethod
 def count_all_station_schedule(db: Session,
                         Sta_station_schedule:Sta_station_schedule,
                         Sta_station_period:Sta_station_period,
                         Users,
                         type:str,
                         keyword:str):

               if keyword is not None:
                 search = "%{}%".format(keyword)
               if keyword == '':
                keyword = None
               if type is None:
                 type = 'onair'

               broadcast_status_case = case(
                                            
                                        (Sta_station_period.broadcast_status_id == 3, 'รอออกอากาศ')
                                           
                                        ).label('broadcast_status')
               
               process_status_case  = case(
                                        
                                            (Sta_station_period.period_status_id == 3, 'ส่งออกอากาศ'),
                                            (Sta_station_period.period_status_id== 6, 'ขอให้ปรับแก้'),
                                            (Sta_station_period.period_status_id == 7, 'ส่งผลการแก้ไข'),
                                            (Sta_station_period.period_status_id == 8, 'ปิดงานแก้ไข')
                                        
                                        ).label('period_status')
                
             
               if  type == 'onair' and keyword is None:
                    print("1")
                    results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 2)
                            .filter(Sta_station_period.broadcast_type_id == 1)
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .count()
                    )
               elif type == 'onair' and keyword is not None:
                   print("2")
                   results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 2)
                            .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search)))
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .count()
                    )
                   

               elif type == 'edit' and keyword is None:
                    print("5")
                    results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 3)
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .count()
                    )
               elif type == 'edit' and keyword is not None:
                   print("6")
                   results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 3)
                            .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search)))
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .count()
                    )

              
               elif type == 'send_edit' and keyword is None:
                    results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 4)
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .count()
                    )
               elif type == 'send_edit' and keyword is not None:
                   print("10")
                   results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 4)
                            .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search)))
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .count()
                    )
                   
               elif type == 'close_edit' and keyword is None:
                   results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 5)
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .count()
                    )
                   
               elif type == 'close_edit' and keyword is not None:
                   print("14")
                   results = (db.query(Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                            .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .outerjoin(Users, Sta_station_period.user_id == Users.id)
                            .filter(Sta_station_period.broadcast_status_id == 3)
                            .filter(Sta_station_period.period_status_id == 5)
                            .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search)))
                            .group_by(  Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.object_key,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.name,
                                        broadcast_status_case,
                                        process_status_case,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.user_id,
                                        Users.first_name,
                                        Users.last_name,
                                        Sta_station_period.period_time_start,
                                        Sta_station_period.period_time_end,
                                        Sta_station_period.id,
                                        Sta_station_period.name,
                                        Sta_station_period.broadcast_status_id,
                                        Sta_station_period.period_status_id
                                        )
                    .count()
                    )

               


               return results
 


 def update_owner_user(db: Session,
                         id:int,
                         user_id:int,
                         update_time:datetime,
                         Sta_station_schedule:Sta_station_schedule):
            sql = db.query(Sta_station_schedule).filter(Sta_station_schedule.id == id).first()
            sql.user_id = user_id,
            sql.modified_by = user_id,
            sql.modified = update_time

            

            return sql
 


 @staticmethod
 def insert(db: Session, model: Generic[T]):
        db.add(model)
        db.commit()
        db.refresh(model)


 @staticmethod
 def update(db: Session, model: Generic[T]):

        db.commit()
        db.refresh(model)

 @staticmethod
 def delete(db: Session, model: Generic[T]):
        db.delete(model)
        db.commit()




