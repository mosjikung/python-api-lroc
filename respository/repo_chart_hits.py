from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, null,or_ ,func , cast ,Date ,asc ,case ,distinct
from datetime import datetime, timedelta ,date
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM
from sqlalchemy.sql.expression import nulls_last
from sqlalchemy import text


from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from model import (Sta_station , 
                   Sta_station_schedule,
                   Sta_station_period,
                   Stat_customer,
                   Stat_customer_action_detail,
                   Stat_customer_interest,
                   Member,
                   Sta_channel,
                   Sta_station_channel,
                   Sta_period_categories,
                   Sta_broadcast_type,
                   Countries,
                   Sta_categories
                   
                   )

import pdb



T = TypeVar("T")


class BaseRepo:
              @staticmethod
              def data_month_hitz(db:Session,
                                  cus_act:Stat_customer_action_detail):
                     
                     current_year = datetime.now().year
                     
                     sql = (
                            db.query(
                                   func.date_part('month', cus_act.action_date).label("Top 100 Radio"),
                                   func.count(cus_act.id).label("TOTAL")
                            )
                            .filter(cus_act.action_type_id.isnot(None))
                            .filter(cus_act.is_active == True)  # Use '==' for comparison
                            .filter(func.date_part('year', cus_act.action_date) == current_year)
                            .group_by(func.date_part('month', cus_act.action_date))
                            .order_by(func.date_part('month', cus_act.action_date).asc())
                            .all()
                     )
                     return sql
              

              @staticmethod
              def get_count_action(db:Session,
                                   cus_act:Stat_customer_action_detail,
                                   station:Sta_station,
                                   month:int):
                                          
                            subquery = (
                                          db.query(cus_act.station_id)
                                          .filter(cus_act.action_type_id.isnot(None))
                                          .filter(cus_act.is_active == True) # Assuming 'is_active' is a boolean column
                                          .filter(func.date_part('month', cus_act.action_date) == month)
                                          .group_by(cus_act.station_id)
                                          .subquery()
                                          )
                            

                            query = (
                                          db.query(
                                          func.sum(station.count_listen).label('count_listen'),
                                          func.sum(station.count_like).label('count_like'),
                                          func.sum(station.count_share).label('count_share')
                                          )
                                          .join(subquery, station.id == subquery.c.station_id)
                                          )
              
                            sql = query.one()
                            
                            return sql
              
              @staticmethod
              def get_list_station_month(db:Session,
                                         station:Sta_station,
                                         cus_act:Stat_customer_action_detail,
                                         month:int):
                            
                            subquery = (db.query(cus_act.station_id)
                                   .filter(cus_act.action_type_id.isnot(None))
                                   .filter(cus_act.is_active == True)
                                   .filter(func.date_part('month', cus_act.action_date) == month)
                                   .group_by(cus_act.station_id).subquery()
                                   )

                                  
                            query = (db.query(
                                    station,
                                   (station.count_like + station.count_share + station.count_listen + station.count_comment).label("TOTAL")
                                   )
                                   .filter(station.id.in_(subquery))
                                   .filter(station.station_status_id == 1)
                                   .order_by(desc("TOTAL"))
                                   )
                            return query
              

              @staticmethod
              def get_check_status_offline(db:Session,
                                           station:Sta_station,
                                           schedule:Sta_station_schedule,
                                           period:Sta_station_period,
                                           cus_act:Stat_customer_action_detail,
                                           customer_id :int,
                                           month:int):
                     
                     subquery = (db.query(cus_act.station_id)
                                .filter(cus_act.action_type_id.isnot(None))
                                .filter(cus_act.is_active == True)
                                .filter(func.date_part('month', cus_act.action_date) == month)
                                .group_by(cus_act.station_id)
                                .subquery()
                            )

                     
                     query = (db.query(
                                   station.id,
                                   station.icon_path,
                                   station.name,
                                   case
                                   (
                                          (schedule.broadcast_status_id != 5, 'OFFLINE'),
                                          (schedule.broadcast_status_id == 5, 'ONLINE')

                                   ).label('Status'),
                                   func.min(schedule.schedule_date).label('min_schedule_date'),  # Label the result
                                   func.min(period.period_time_start).label('min_period_time_start'),  # Label the result
                                   func.max(period.period_time_end).label('max_period_time_end'),  # Label the result
                                   
                                   )
                                   .join(schedule, station.id == schedule.station_id)
                                   .join(period, schedule.id == period.station_schedule_id)
                                   .filter(station.id.in_(subquery))
                                   .filter(station.id == customer_id)
                                   .filter(cast(schedule.schedule_date,Date)>= func.CURRENT_DATE())
                                   .filter(period.broadcast_status_id.isnot(None))
                                   .group_by(station.id, station.icon_path, station.name,'Status')
                                   )
                     
                     sql = query.all()
                     return sql
                                   
              
              @staticmethod
              def check_station_like(db:Session,
                                     cus_act:Stat_customer_action_detail,
                                     station_id:int,
                                     user_id:int):
                            sql = (db.query(cus_act)
                                   .filter(cus_act.station_id == station_id)
                                   .filter(cus_act.customer_id == user_id)
                                   .filter(cus_act.action_type_id == 1)
                                   .first()
                                   )
                            
                            return sql
              
              @staticmethod
              def get_playlist_month_all(db:Session,
                                         station:Sta_station,
                                         schedule:Sta_station_schedule,
                                         period:Sta_station_period,
                                         cus_act:Stat_customer_action_detail,
                                         offset:int,
                                         limit:int,
                                         month:int):
                      
                            subquery = (db.query(cus_act.station_id)
                                          .filter(cus_act.action_type_id.isnot(None))
                                          .filter(cus_act.is_active == 't')
                                          .filter(func.date_part('month', cus_act.action_date) == month)
                                          .group_by(cus_act.station_id).subquery()
                                          )
                            
                            
                            query = (db.query(
                                          station,
                                          schedule,
                                          period
                                          )
                                          .join(schedule, station.id == schedule.station_id)
                                          .join(period, schedule.id == period.station_schedule_id)
                                          .filter(schedule.broadcast_status_id == 5)
                                          .filter(period.broadcast_status_id == 5)
                                          .filter(station.id.in_(subquery))
                                          .order_by(asc(schedule.schedule_date),asc(period.period_time_start))
                                          .offset(offset)
                                          .limit(limit)
                            )
                            
                            sql = query.all()
                            
                            return sql
              

              @staticmethod
              def get_playlist_month_only(db:Session,
                                         station:Sta_station,
                                         schedule:Sta_station_schedule,
                                         period:Sta_station_period,
                                         cus_act:Stat_customer_action_detail,
                                         station_id:int,
                                         month:int):
                            
                            subquery = (db.query(cus_act.station_id)
                                          .filter(cus_act.action_type_id.isnot(None))
                                          .filter(cus_act.is_active == 't')
                                          .filter(func.date_part('month', cus_act.action_date) == month)
                                          .group_by(cus_act.station_id).subquery()
                                          )
                            query = (db.query(
                                          station,
                                          schedule,
                                          period
                                          )
                                          .join(schedule, station.id == schedule.station_id)
                                          .join(period, schedule.id == period.station_schedule_id)
                                          .filter(schedule.broadcast_status_id == 5)
                                          .filter(period.broadcast_status_id == 5)
                                          .filter(station.id == station_id)
                                          .filter(station.id.in_(subquery))
                                          .order_by(asc(schedule.schedule_date),asc(period.period_time_start))
                                          
                            )
                            
                            sql = query.all()
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