from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, null,or_ ,func , cast ,Date ,asc ,case


from datetime import datetime, timedelta ,date
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM


from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from model import (Sta_station , 
                   Sta_station_schedule,
                   Member,
                   Sta_broadcast,
                   Sta_station_period,
                   Sta_station_playlist
                   )

import pdb



T = TypeVar("T")


class BaseRepo:

              @staticmethod
              def get_count_data_broadcast(db: Session,
                         Sta_station:Sta_station,
                         Sta_station_schedule:Sta_station_schedule,
                         Sta_station_period:Sta_station_period,
                         offset:int,
                         limit:int,
                         order_direction:str,
                         keyword:str):
               
              
               if keyword is not None:
                 search = "%{}%".format(keyword)
               if keyword == '':
                keyword = None
               if order_direction is None:
                 order_direction = 'asc'
             
               if  keyword is None:
                    print("1")
                    results = (db.query(Sta_station.id,
                                        Sta_station.object_key,
                                        Sta_station.name,
                                        Sta_station.is_enabled,
                                        Sta_station.suspend_comment,
                                        Sta_station.suspend_date_start,
                                        Sta_station.suspend_date_end,
                                        Sta_station.disable_comment,
                                        Sta_station_schedule.station_id,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.count_like,
                                        Sta_station_schedule.count_share,
                                        Sta_station_schedule.count_play,
                                        Sta_station_schedule.count_comment,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_schedule.modified,
                                        Sta_station_schedule.broadcast_status_id,
                                        Sta_station_period.broadcast_type_id
                                      )
                                                                                                                      
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.broadcast_status_id == 5)
                   .filter(Sta_station_period.broadcast_status_id == 5)
                   .group_by(Sta_station.id,
                             Sta_station.object_key,
                             Sta_station.name,
                             Sta_station.is_enabled,
                             Sta_station.suspend_comment,
                             Sta_station.suspend_date_start,
                             Sta_station.suspend_date_end,
                             Sta_station.disable_comment,
                             Sta_station_schedule.station_id,
                             Sta_station_schedule.schedule_date,
                             Sta_station_schedule.id,
                             Sta_station_schedule.schedule_number,
                             Sta_station_schedule.object_key,
                             Sta_station_schedule.count_like,
                             Sta_station_schedule.count_share,
                             Sta_station_schedule.count_play,
                             Sta_station_schedule.count_comment,
                             Sta_station_period.broadcast_type_id,)
                   .count()
                   )
               elif keyword is not None:
               
                   results = (db.query(Sta_station.id,
                                        Sta_station.object_key,
                                        Sta_station.name,
                                        Sta_station.is_enabled,
                                        Sta_station.suspend_comment,
                                        Sta_station.suspend_date_start,
                                        Sta_station.suspend_date_end,
                                        Sta_station.disable_comment,
                                        Sta_station_schedule.station_id,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.count_like,
                                        Sta_station_schedule.count_share,
                                        Sta_station_schedule.count_play,
                                        Sta_station_schedule.count_comment,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_schedule.modified,
                                        Sta_station_schedule.broadcast_status_id,
                                        Sta_station_period.broadcast_type_id

                                      )
                                                                                                                      
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.broadcast_status_id == 5)
                   .filter(Sta_station_period.broadcast_status_id == 5)
                   .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station.name.like(search)))
                   .group_by(Sta_station.id,
                             Sta_station.object_key,
                             Sta_station.name,
                             Sta_station.is_enabled,
                             Sta_station.suspend_comment,
                             Sta_station.suspend_date_start,
                             Sta_station.suspend_date_end,
                             Sta_station.disable_comment,
                             Sta_station_schedule.station_id,
                             Sta_station_schedule.schedule_date,
                             Sta_station_schedule.id,
                             Sta_station_schedule.schedule_number,
                             Sta_station_schedule.object_key,
                             Sta_station_schedule.count_like,
                             Sta_station_schedule.count_share,
                             Sta_station_schedule.count_play,
                             Sta_station_schedule.count_comment,
                             Sta_station_period.broadcast_type_id,)
                   .count()
                   )

               return results    



              @staticmethod
              def get_data_broadcast(db: Session,
                         Sta_station:Sta_station,
                         Sta_station_schedule:Sta_station_schedule,
                         Sta_station_period:Sta_station_period,
                         offset:int,
                         limit:int,
                         order_direction:str,
                         keyword:str):
               
              
               if keyword is not None:
                 search = "%{}%".format(keyword)
               if keyword == '':
                keyword = None
               if order_direction is None:
                 order_direction = 'asc'
             
               if  keyword is None:
                    print("1")
                    results = (db.query(Sta_station.id,
                                        Sta_station.object_key,
                                        Sta_station.name,
                                        Sta_station.is_enabled,
                                        Sta_station.suspend_comment,
                                        Sta_station.suspend_date_start,
                                        Sta_station.suspend_date_end,
                                        Sta_station.disable_comment,
                                        Sta_station_schedule.station_id,
                                        Sta_station_schedule.schedule_date,
                                        case(
                                        (Sta_station_schedule.broadcast_status_id == 5, 'ON-AIR')
                                        ).label('broadcast_status'),
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.count_like,
                                        Sta_station_schedule.count_share,
                                        Sta_station_schedule.count_play,
                                        Sta_station_schedule.count_comment,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_schedule.modified,
                                        Sta_station_schedule.broadcast_status_id,
                                        Sta_station_period.broadcast_type_id,
                                      )
                                                                                                                      
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.broadcast_status_id == 5)
                   .filter(Sta_station_period.broadcast_status_id == 5)
                   .group_by(Sta_station.id,
                             Sta_station.object_key,
                             Sta_station.name,
                             Sta_station.is_enabled,
                             Sta_station.suspend_comment,
                             Sta_station.suspend_date_start,
                             Sta_station.suspend_date_end,
                             Sta_station.disable_comment,
                             Sta_station_schedule.station_id,
                             Sta_station_schedule.schedule_date,
                             Sta_station_schedule.id,
                             Sta_station_schedule.schedule_number,
                             Sta_station_schedule.object_key,
                             Sta_station_schedule.count_like,
                             Sta_station_schedule.count_share,
                             Sta_station_schedule.count_play,
                             Sta_station_schedule.count_comment,
                             Sta_station.is_enabled,
                             Sta_station.suspend_date_start,
                             Sta_station.suspend_date_end,
                             Sta_station.suspend_comment,
                             Sta_station.station_status_id,
                             Sta_station.disable_comment,
                             Sta_station_period.broadcast_type_id,
                             )
                   .order_by(desc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                    
               elif keyword is not None:
               
                   results = (db.query(Sta_station.id,
                                        Sta_station.object_key,
                                        Sta_station.name,
                                        Sta_station.is_enabled,
                                        Sta_station.suspend_comment,
                                        Sta_station.suspend_date_start,
                                        Sta_station.suspend_date_end,
                                        Sta_station.disable_comment,
                                        Sta_station_schedule.station_id,
                                        Sta_station_schedule.schedule_date,
                                        case(
                                        (Sta_station_schedule.broadcast_status_id == 5, 'ON-AIR')
                                        ).label('broadcast_status'),
                                        Sta_station_schedule.id,
                                        Sta_station_schedule.schedule_number,
                                        Sta_station_schedule.object_key,
                                        Sta_station_schedule.count_like,
                                        Sta_station_schedule.count_share,
                                        Sta_station_schedule.count_play,
                                        Sta_station_schedule.count_comment,
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                        Sta_station_schedule.modified,
                                        Sta_station_schedule.broadcast_status_id,
                                        Sta_station_period.broadcast_type_id
                                      )
                                                                                                                  
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.broadcast_status_id == 5)
                   .filter(Sta_station_period.broadcast_status_id == 5)
                   .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station.name.like(search)))
                   .group_by(Sta_station.id,
                             Sta_station.object_key,
                             Sta_station.name,
                             Sta_station.is_enabled,
                             Sta_station.suspend_comment,
                             Sta_station.suspend_date_start,
                             Sta_station.suspend_date_end,
                             Sta_station.disable_comment,
                             Sta_station_schedule.station_id,
                             Sta_station_schedule.schedule_date,
                             Sta_station_schedule.id,
                             Sta_station_schedule.schedule_number,
                             Sta_station_schedule.object_key,
                             Sta_station_schedule.count_like,
                             Sta_station_schedule.count_share,
                             Sta_station_schedule.count_play,
                             Sta_station_schedule.count_comment,
                             Sta_station_period.broadcast_type_id,)
                   .order_by(desc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
               return results
              

              @staticmethod
              def get_data_schedule_broadcast(db: Session,
                         Sta_station:Sta_station,
                         Sta_station_schedule:Sta_station_schedule,
                         Sta_station_period:Sta_station_period,
                         id:int):
                results = (db.query(Sta_station.id,
                                        Sta_station.object_key,
                                        Sta_station.name,
                                        Sta_station.count_like,
                                        Sta_station.count_share,
                                        Sta_station.count_listen,
                                        Sta_station.count_comment,
                                        Sta_station_schedule.broadcast_url,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.broadcast_status_id,
                                        case(
                                        (Sta_station_schedule.broadcast_status_id == 5, 'ON-AIR')
                                        ).label('broadcast_status'),
                                        func.min(Sta_station_period.period_time_start).label('time_min'),
                                        func.max(Sta_station_period.period_time_end).label('time_max'),
                                      )
                          .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                          .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                          .filter(Sta_station_schedule.broadcast_status_id.isnot(None))     
                          .filter(Sta_station_schedule.id == id)
                          .group_by(Sta_station.id,
                                        Sta_station.object_key,
                                        Sta_station.name,
                                        Sta_station.count_like,
                                        Sta_station.count_share,
                                        Sta_station.count_listen,
                                        Sta_station.count_comment,
                                        Sta_station_schedule.broadcast_url,
                                        Sta_station_schedule.schedule_date,
                                        Sta_station_schedule.broadcast_status_id)      
                          .all()                 
                                    )
                 
                return results
              
              
              @staticmethod
              def find_last_row_schedule(db: Session,
                         Sta_broadcast:Sta_broadcast,
                         id:int
                         ):
                   results = (db.query(Sta_broadcast)
                   .filter(Sta_broadcast.station_schedule_id == id)
                   .order_by(desc(Sta_broadcast.modified))
                   .first()
                   )
                   return results
              
              @staticmethod
              def get_data_schedule(db:Session,
                                    Sta_station_schedule:Sta_station_schedule,
                                    Sta_station_period:Sta_station_period,
                                    id:int
                                    ):
                  sql = (db.query(Sta_station_schedule,Sta_station_period)
                        .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                        .filter(Sta_station_schedule.id == id)
                        .order_by(asc(Sta_station_period.period_time_start))
                        .all()
                        )
                  return sql
              
              @staticmethod
              def get_data_schedule_x(db:Session,
                                    id:int,
                                    Sta_staion_schedule:Sta_station_schedule):
                  sql = (db.query(Sta_station_schedule).filter(Sta_station_schedule.id == id)).all()
                  return sql


              @staticmethod
              def get_data_station(db:Session,
                                    id:int,
                                    Sta_station:Sta_station):
                  sql = (db.query(Sta_station).filter(Sta_station.id == id)).all()
                  return sql
              
              @staticmethod
              def get_data_period(db:Session,
                                    id:int,
                                    Sta_station_period:Sta_station_period):
                  sql = (db.query(Sta_station_period).filter(Sta_station_period.station_schedule_id == id)).all()
                  return sql
              
              @staticmethod
              def get_data_playlist(db:Session,
                                    id:int,
                                    Sta_station_playlist:Sta_station_playlist):
                  sql = (db.query(Sta_station_playlist).filter(Sta_station_playlist.station_period_id == id)).all()
                  
                  return sql
              
              @staticmethod
              def delete_schedule_broadcast(db:Session,
                                    id:int,
                                    user_id:int,
                                    update_time:datetime,
                                    Sta_station_schedule:Sta_station_schedule):
                  sql = (db.query(Sta_station_schedule).filter(Sta_station_schedule.id == id)).first()
                  sql.is_deleted = True
                  sql.broadcast_status_id = 8
                  sql.modified_by = user_id,
                  sql.modified = update_time

                  return sql
              
              @staticmethod
              def delete_schedule_period(db:Session,
                                    id:int,
                                    user_id:int,
                                    update_time:datetime,
                                    Sta_station_period:Sta_station_period):
                  sql = (db.query(Sta_station_schedule).filter(Sta_station_period.station_schedule_id == id)).first()
                  sql.is_deleted = True
                  sql.broadcast_status_id = 8
                  sql.modified_by = user_id,
                  sql.modified = update_time

                  return sql
              
              
              @staticmethod
              def check_station(db:Session,
                                Sta_station_schedule:Sta_station_schedule,
                                id:int,
                                broadcast_status_id:int,
                                user_id:int,
                                time_update:datetime):
                 sql = db.query(Sta_station_schedule).filter(Sta_station_schedule.id == id).first()
                 sql.broadcast_status_id = broadcast_status_id,
                 sql.broadcast_status_date = time_update,
                 sql.modified_by = user_id,
                 sql.modified = time_update,

                 return sql


              
              @staticmethod
              def check_period(db:Session,
                                Sta_station_period:Sta_station_period,
                                id:int,
                                broadcast_status_id:int,
                                user_id:int,
                                time_update:datetime):
                 sql = db.query(Sta_station_period).filter(Sta_station_period.id == id).first()
                 sql.broadcast_status_id = broadcast_status_id,
                 sql.broadcast_status_date = time_update,
                 sql.modified_by = user_id,
                 sql.modified = time_update,

                 return sql
              
              @staticmethod
              def get_all_data_check_period(db:Session,
                                Sta_station_period:Sta_station_period,
                                id:int):
              
                sql = db.query(Sta_station_period).filter(Sta_station_period.station_schedule_id == id).all()
                return sql
              

              @staticmethod
              def insert(db: Session, model: Generic[T]):
                db.add(model)
                db.commit()
                db.refresh(model)
                return True


              @staticmethod
              def update(db: Session, model: Generic[T]):
                db.commit()
                db.refresh(model)
                return True

              @staticmethod
              def delete(db: Session, model: Generic[T]):
                db.delete(model)
                db.commit()
                return True
    
                 
              
              