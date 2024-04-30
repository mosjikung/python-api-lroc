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
                   Sta_station_period,
                   Stat_customer,
                   Stat_customer_action_detail,
                   Member,
                   Sta_station_channel,
                   Sta_channel,
                   
                   )

import pdb



T = TypeVar("T")


class BaseRepo:
              @staticmethod
              def get_station_popular(db: Session,
                            Sta_station:Sta_station,
                            offset:int,
                            limit:int,
                            keyword:str,                           
                            ):
                            if keyword is None:
                                sql = (
                                                db.query(
                                                Sta_station,
                                                (Sta_station.count_like + Sta_station.count_share + Sta_station.count_listen + Sta_station.count_comment).label("TOTAL")
                                        )
                                        .filter(Sta_station.approve_status_id == 1)
                                        .filter(Sta_station.is_deleted == 'f')
                                        .filter(Sta_station.station_status_id == 1)
                                        .order_by(desc("TOTAL"))
                                        .offset(offset)
                                        .limit(limit)
                                        .all()
                                        )
                                return sql
                            else:
                                search = "%{}%".format(keyword)

                                sql = (
                                                db.query(
                                                Sta_station,
                                                (Sta_station.count_like + Sta_station.count_share + Sta_station.count_listen + Sta_station.count_comment).label("TOTAL")
                                        )
                                        .filter(Sta_station.approve_status_id == 1)
                                        .filter(Sta_station.is_deleted == 'f')
                                        .filter(Sta_station.station_status_id == 1)
                                        .filter(Sta_station.name.ilike(search))
                                        .order_by(desc("TOTAL"))
                                        .offset(offset)
                                        .limit(limit)
                                        .all()
                                        )
                                return sql

                                    
              
              @staticmethod
              def get_period_popular(db: Session,
                            Sta_station:Sta_station,
                            Sta_station_schedule:Sta_station_schedule,
                            Sta_station_period:Sta_station_period,
                            offset:int,
                            limit:int,
                            keyword:str
                            ):
                            if keyword is None:

                                sql =  (db.query(Sta_station,Sta_station_schedule,Sta_station_period,
                                        (Sta_station_period.count_like + Sta_station_period.count_listen + Sta_station_period.count_share).label("TOTAL"))
                                        .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                                        .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                                        .filter(Sta_station.approve_status_id == 1)
                                        .filter(Sta_station_period.is_deleted == 'f')
                                        .filter(Sta_station.station_status_id == 1)
                                        .order_by(desc("TOTAL"))
                                        .offset(offset)
                                        .limit(limit)
                                        .all()
                                        )
                                
                                return sql
                            else:
                                search = "%{}%".format(keyword)        
                                sql =  (db.query(Sta_station,Sta_station_schedule,Sta_station_period,
                                        (Sta_station_period.count_like + Sta_station_period.count_listen + Sta_station_period.count_share).label("TOTAL"))
                                        .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                                        .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                                        .filter(Sta_station.approve_status_id == 1)
                                        .filter(Sta_station_period.is_deleted == 'f')
                                        .filter(Sta_station.station_status_id == 1)
                                        .filter(Sta_station_period.name.ilike(search))
                                        .order_by(desc("TOTAL"))
                                        .offset(offset)
                                        .limit(limit)
                                        .all()
                                        )
                                
                                return sql
            
              

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
              
              @staticmethod
              def get_lastime_listen(db:Session,
                                     Stat_customer_action_detail:Stat_customer_action_detail,
                                     Sta_station:Sta_station,
                                     user_id:int,
                                     offset:int,
                                     limit:int
                                     ):
                        
                        sql = (db.query(
                                        Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.icon_path,
                                        Sta_station.approve_status_id,
                                        func.max(Stat_customer_action_detail.action_date).label('action_date')
                                        )
                               .join(Sta_station,Stat_customer_action_detail.station_id == Sta_station.id)
                               .filter(Stat_customer_action_detail.action_type_id == 2)
                               .filter(Stat_customer_action_detail.customer_id == user_id)
                               .group_by(
                                        Sta_station.id,
                                        Sta_station.name,
                                        Sta_station.icon_path,
                                        Sta_station.approve_status_id
                                        )
                               .order_by(desc('action_date'))
                               .offset(offset)
                               .limit(limit)
                               .all()
                               )
                        return sql
              
              @staticmethod
              def get_produce(db: Session, 
                              Sta_station_channel:Sta_station_channel,
                              Sta_channel: Sta_channel,
                              Member:Member,
                              id:int):
                            sql = (db.query(Sta_station_channel,Sta_channel,Member)
                                   .join(Sta_channel, Sta_station_channel.channel_id == Sta_channel.id)
                                   .join(Member, Sta_station_channel.created_by == Member.id)
                                   .filter(Sta_station_channel.id == id)
                                   .all()
                                   )
                            return sql
                            
              @staticmethod
              def get_produce_none(db: Session,
                                   model:Generic[T],
                                   id:int):
                            sql = (db.query(model)
                                   .filter(model.id == id)
                                   .first()
                                   )
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

              @staticmethod
              def rollback(db: Session, model: Generic[T]):
                            db.rollback(model)
                            db.refresh(model)
                            return False