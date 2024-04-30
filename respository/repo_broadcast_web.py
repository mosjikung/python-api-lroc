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
                   Sta_station_playlist,
                   Sta_station_channel,
                   Sta_channel,
                   )

import pdb



T = TypeVar("T")


class BaseRepo:
              @staticmethod
              def get_data_broadcast(db: Session,
                            Sta_station:Sta_station,
                            Sta_station_schedule:Sta_station_schedule,
                            Sta_station_period:Sta_station_period,
                            offset:int,
                            limit:int,
                            order_direction:str,
                            station_id:int):

                            if order_direction is None:
                                          order_direction = 'asc'
                            if station_id is None:
                                   results = (db.query(Sta_station,Sta_station_schedule,Sta_station_period)
                                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                                   .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                                   .filter(Sta_station_schedule.broadcast_status_id == 5)
                                   .filter(Sta_station_period.broadcast_status_id == 5)
                                   .filter(Sta_station.station_status_id == 1)
                                   .offset(offset)
                                   .limit(limit)
                                   .all()
                                   )
                            else:
                                    results = (db.query(Sta_station,Sta_station_schedule,Sta_station_period)
                                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                                   .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                                   .filter(Sta_station_schedule.broadcast_status_id == 5)
                                   .filter(Sta_station_period.broadcast_status_id == 5)
                                   .filter(Sta_station.id == station_id)
                                   .offset(offset)
                                   .limit(limit)
                                   .all()
                                   )
                                    
                            return results
                 
              
              @staticmethod
              def find_channel(db: Session,
                            Sta_station_channel:Sta_station_channel,
                            Sta_channel:Sta_channel,
                            Member:Member,
                            id:int):
                            sql = (db.query(Sta_station_channel,Sta_channel,Member)
                                   .join(Sta_channel,Sta_station_channel.channel_id == Sta_channel.id)
                                   .join(Member, Sta_channel.created_by == Member.id)
                                   .filter(Sta_station_channel.id == id)
                                   .all()
                                   )
                            return sql
              
              @staticmethod
              def find_channel_none(db: Session,
                                    Member:Member,
                                    id:int):
                            sql = db.query(Member).filter(Member.id == id).first()
                            return sql
              

              

              