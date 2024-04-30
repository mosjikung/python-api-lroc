from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, null,or_ ,func , cast ,Date ,asc ,case ,distinct
from datetime import datetime, timedelta ,date
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM
from sqlalchemy.sql.expression import nulls_last


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
              def get_all_guest(db: Session,
                            Sta_station:Sta_station,
                            Stat_customer_interest:Stat_customer_interest,
                            id:int
                            ):
                            
                            
                            sql =  (db.query(Sta_station.id , Sta_station.name , Sta_station.icon_path , Sta_station.approve_status_id)
                                    .join(Stat_customer_interest, Sta_station.id == Stat_customer_interest.station_id)
                                    .filter(Stat_customer_interest.is_active == True)
                                    .filter(Stat_customer_interest.customer_id == id)
                                    .filter(Sta_station.station_status_id == 1)
                                    .group_by(Sta_station.id , Sta_station.name , Sta_station.icon_path , Sta_station.approve_status_id)
                                    .all()
                                    )
                            return sql

              def get_all_schedule_period(db:Session,
                                      Sta_station_schedule:Sta_station_schedule,
                                      Sta_station_period:Sta_station_period,
                                      Sta_station:Sta_station,
                                      Sta_broadcast_type:Sta_broadcast_type,
                                      Sta_period_categories:Sta_period_categories,
                                      id:int,
                                      date:datetime):
                      
                            sql = (db.query(Sta_station_schedule,Sta_station_period,Sta_station,Sta_broadcast_type,Sta_period_categories)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .join(Sta_station, Sta_station_schedule.station_id == Sta_station.id)
                            .join(Sta_broadcast_type, Sta_station_period.broadcast_type_id == Sta_broadcast_type.id)
                            .join(Sta_period_categories, Sta_station_period.period_category_id == Sta_period_categories.id)
                            .filter(Sta_station.station_status_id == 1)
                            .filter(Sta_station.id == id)
                            .filter(cast(Sta_station_schedule.schedule_date, Date) == date)
                            .order_by(asc(Sta_station_period.period_time_start))
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
              def get_list_period_web(db:Session,
                                      Sta_station_schedule:Sta_station_schedule,
                                      Sta_station_period:Sta_station_period,
                                      Sta_station:Sta_station,
                                      Sta_period_categories:Sta_period_categories,
                                      id:int):
                      
                     sql = (db.query(Sta_station_schedule,Sta_station_period,Sta_station,Sta_period_categories)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .join(Sta_station, Sta_station_schedule.station_id == Sta_station.id)
                            .join(Sta_period_categories, Sta_station_period.period_category_id == Sta_period_categories.id)
                            .filter(Sta_station.station_status_id == 1)
                            .filter(Sta_station.id == id)
                            .filter(Sta_station_schedule.broadcast_status_id == 5)
                            .filter(Sta_station_period.broadcast_status_id == 5)
                            .order_by(desc(Sta_station_period.period_time_start))
                            .all()
                            )
                            
                     return sql
              

              @staticmethod
              def get_period_live_web(db:Session,
                                      Sta_station_schedule:Sta_station_schedule,
                                      Sta_station_period:Sta_station_period,
                                      Sta_station:Sta_station,
                                      Sta_period_categories:Sta_period_categories,
                                      id:int,
                                      live_id:int):
                      
                     sql = (db.query(Sta_station_schedule,Sta_station_period,Sta_station,Sta_period_categories)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .join(Sta_station, Sta_station_schedule.station_id == Sta_station.id)
                            .join(Sta_period_categories, Sta_station_period.period_category_id == Sta_period_categories.id)
                            .filter(Sta_station.station_status_id == 1)
                            .filter(Sta_station.id == id)
                            .filter(Sta_station_schedule.broadcast_status_id == 5)
                            .filter(Sta_station_period.broadcast_status_id == 5)
                            .filter(Sta_station_period.id == live_id)
                            .order_by(desc(Sta_station_period.period_time_start))
                            .all()
                            )
                            
                     return sql
              

              @staticmethod
              def get_listen_top(db:Session,
                                      Sta_station_schedule:Sta_station_schedule,
                                      Sta_station_period:Sta_station_period,
                                      Sta_station:Sta_station,
                                      Sta_period_categories:Sta_period_categories,
                                      id:int):
                      
                     sql = (db.query(Sta_station_schedule,Sta_station_period,Sta_station,Sta_period_categories)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .join(Sta_station, Sta_station_schedule.station_id == Sta_station.id)
                            .join(Sta_period_categories, Sta_station_period.period_category_id == Sta_period_categories.id)
                            .filter(Sta_station.station_status_id == 1)
                            .filter(Sta_station_schedule.broadcast_status_id == 5)
                            .filter(Sta_station_period.broadcast_status_id == 5)
                            .filter(Sta_station.id == id)
                            .order_by(desc(Sta_station_period.count_listen))
                            .all()
                            )
                            
                     return sql
              
              @staticmethod
              def search_data_all(db:Session,
                                  station:Sta_station,
                                  keyword:str,
                                  offset:int,
                                  limit:int):
                     if keyword is not None:
                            search = "%{}%".format(keyword)
                            sql = (db.query(station)
                            .filter(station.name.ilike(search))
                            .filter(station.is_deleted == 'f')
                            .filter(station.approve_status_id == 1)
                            .offset(offset)
                            .limit(limit)
                            .all()
                            )
                     
                     else:
                            
                            sql = (db.query(station)
                            .filter(station.is_deleted == 'f')
                            .filter(station.approve_status_id == 1)
                            .offset(offset)
                            .limit(limit)
                            .all()
                            )

                     


                     return sql
                     
              
              
              @staticmethod
              def get_list_programe_schedule(db:Session,
                                      Sta_station_schedule:Sta_station_schedule,
                                      Sta_station_period:Sta_station_period,
                                      Sta_station:Sta_station,
                                      Sta_broadcast_type:Sta_broadcast_type,
                                      Sta_period_categories:Sta_period_categories,
                                      id:int,
                                      date:datetime):
                      
                     sql = (db.query(Sta_station_schedule,Sta_station_period,Sta_station,Sta_broadcast_type,Sta_period_categories)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .join(Sta_station, Sta_station_schedule.station_id == Sta_station.id)
                            .join(Sta_broadcast_type, Sta_station_period.broadcast_type_id == Sta_broadcast_type.id)
                            .join(Sta_period_categories, Sta_station_period.period_category_id == Sta_period_categories.id)
                            .filter(Sta_station.station_status_id == 1)
                            .filter(Sta_station.id == id)
                            .filter(cast(Sta_station_schedule.schedule_date, Date) == date)
                            .order_by(asc(Sta_station_period.period_time_start))
                            .all()
                            )
                            
                     return sql
              

              @staticmethod
              def period_broadcast_web(db:Session,
                                      Sta_station_schedule:Sta_station_schedule,
                                      Sta_station_period:Sta_station_period,
                                      id:int):
                      
                     sql = (db.query(Sta_station_schedule,Sta_station_period)
                            .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                            .filter(Sta_station_schedule.broadcast_status_id == 5)
                            .filter(Sta_station_period.broadcast_status_id == 5)
                            .order_by(desc(Sta_station_period.period_time_start))
                            .all()
                            )
                            
                     return sql
              

              @staticmethod
              def get_detail_web(db:Session,
                                 Sta_station:Sta_station,
                                 Countries:Countries,
                                 id:int):
                     
                     sql = (db.query(Sta_station,Countries)
                            .join(Countries, Sta_station.country_id == Countries.id)
                            .filter(Sta_station.station_status_id == 1)
                            .filter(Sta_station.id == id)
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
              def select_station_data(db:Session,
                                      model:Generic[T],
                                      id:int):
                     sql = (db.query(model)
                            .filter(model.id == id)
                            .first()
                            )
                     return sql
              
              @staticmethod
              def get_data_like_station(db:Session,
                                model:Generic[T],
                                id:int):
                      sql = (db.query(distinct(model.station_id))
                             .filter(model.action_type_id == 1)
                             .filter(model.customer_id == id)
                             .all()
                             )
                      return sql
              
              @staticmethod
              def get_data_like_schedule(db:Session,
                                model:Generic[T],
                                id:int):
                      sql = (db.query(distinct(model.schedule_id))
                             .filter(model.action_type_id == 1)
                             .filter(model.customer_id == id)
                             .all()
                             )
                      return sql
              
              @staticmethod
              def get_data_like_period(db:Session,
                                model:Generic[T],
                                id:int):
                      sql = (db.query(distinct(model.period_id))
                             .filter(model.action_type_id == 1)
                             .filter(model.customer_id == id)
                             .all()
                             )
                      return sql
              
              @staticmethod
              def update_unlike(db:Session,
                                model:Generic[T],
                                user_id:int,
                                station_id:int,
                                update_time:datetime):
                      action_type = 1
                      sql = (db.query(model).filter(model.station_id == station_id).filter(model.customer_id == user_id).filter(model.action_type_id == action_type).first())
                      sql.action_type_id = 5
                      sql.modified = update_time
                      sql.modified_by = user_id
                      return sql


              @staticmethod
              def update_unlike_period(db:Session,
                                model:Generic[T],
                                user_id:int,
                                station_id:int,
                                period_id:int,
                                update_time:datetime):
                      action_type = 1
                      sql = (db.query(model).filter(model.station_id == station_id)
                             .filter(model.customer_id == user_id)
                             .filter(model.period_id == period_id)
                             .filter(model.action_type_id == action_type)
                             .first()
                             )
                      sql.action_type_id = 5
                      sql.modified = update_time
                      sql.modified_by = user_id

                      return sql
                      
              
              @staticmethod
              def get_data_cate(db:Session,
                                model:Generic[T]):
                      sql = (db.query(model)
                             .filter(model.is_deleted == 'f')
                             .order_by(asc(model.sort))
                             )
                      return sql

              @staticmethod
              def get_period_category_rec(db:Session,
                                          station:Sta_station,
                                          schedule:Sta_station_schedule,
                                          period:Sta_station_period,
                                          category:Sta_period_categories,
                                          offset:int,
                                          limit:int,
                                          id:int):
                     
                     sql = (db.query(station,
                                     schedule,
                                     period,
                                     category,
                                     func.sum(period.count_like + period.count_share + period.count_listen).label('TOTAL'))
                            .join(schedule , station.id == schedule.station_id)
                            .join(period, schedule.id == period.station_schedule_id)
                            .join(category,period.period_category_id == category.id)
                            .filter(period.period_category_id == id)
                            .filter(period.is_deleted == 'f')
                            .filter(period.broadcast_status_id == 5)
                            .filter(station.station_status_id == 1)
                            .group_by(period.id,category.id,station.id,schedule.id)
                            .order_by(desc("TOTAL"),asc(period.id))
                            .offset(offset)
                            .limit(limit)
                            .all()
                            )
                     return sql
              

              @staticmethod
              def get_period_schedule_cate_rec(db:Session,
                                          period:Sta_station_period,
                                          schedule:Sta_station_schedule,
                                          category:Sta_period_categories,
                                          station:Sta_station,
                                          offset:int,
                                          limit:int,
                                          category_id:int):
             
                     sql = (db.query(period,schedule,category,station)
                            .join(schedule,period.station_schedule_id == schedule.id)
                            .join(category,period.period_category_id == category.id)
                            .join(station, station.id == schedule.station_id)
                            .filter(period.period_category_id == category_id)
                            .filter(period.is_deleted == 'f')
                            .filter(period.broadcast_status_id == 5)
                            .filter(station.station_status_id == 1)
                            .order_by(desc(schedule.schedule_date),asc(period.period_time_start))
                            .offset(offset)
                            .limit(limit)
                            .all()
                            )
                     return sql
              

              
              
              @staticmethod
              def get_station_like_web(db:Session,
                                       cus_act:Stat_customer_action_detail,
                                       station:Sta_station,
                                       offset:int,
                                       limit:int,
                                       id:int):
                     query = (db.query(
                            cus_act.action_date.cast(Date),
                            station.id,
                            station.name,
                            station.icon_path,
                            station.approve_status_id
                            )
                            .join(station,station.id == cus_act.station_id)
                            .filter(cus_act.action_type_id == 1)
                            .filter(cus_act.customer_id == id)
                            .filter(station.approve_status_id == 1)
                            .filter(station.station_status_id == 1)
                            .filter(cus_act.is_active == True)
                            .group_by(
                            cus_act.action_date.cast(Date),
                            station.id,
                            station.name,
                            station.icon_path,
                            station.approve_status_id
                            )
                            .order_by(
                            cus_act.action_date.cast(Date).desc()
                            )
                            .offset(offset)
                            .limit(limit)
                            )


                     results = query.all()
                     return results
              

              @staticmethod
              def check_data_action_detail_period(db:Session,
                                                  cus_act:Stat_customer_action_detail,
                                                  user_id:int,
                                                  action_type_id:int,
                                                  station_id:int,
                                                  period_id:int):
                      
                     sql = (db.query(cus_act)
                            .filter(cus_act.customer_id == user_id)
                            .filter(cus_act.action_type_id == action_type_id)
                            .filter(cus_act.station_id == station_id)
                            .filter(cus_act.period_id == period_id)
                            .first()
                            )
                     return sql
              

              @staticmethod
              def check_data_action_detail_period_none(db:Session,
                                                  cus_act:Stat_customer_action_detail,
                                                  user_id:int,
                                                  action_type_id:int,
                                                  station_id:int):
                      
                     sql = (db.query(cus_act)
                            .filter(cus_act.customer_id == user_id)
                            .filter(cus_act.action_type_id == action_type_id)
                            .filter(cus_act.station_id == station_id)
                            .filter(cus_act.period_id == None)
                            .first()
                            )
                     return sql
              

              @staticmethod
              def get_count_like_period(db:Session,
                                   cus_act:Stat_customer_action_detail,
                                   action_type_id:int,
                                   station_id:int,
                                   period_id:int):
                     sql = (db.query(cus_act)
                            .filter(cus_act.action_type_id == action_type_id)
                            .filter(cus_act.station_id == station_id)
                            .filter(cus_act.period_id == period_id)
                            .count()
                            )
                     
                     
                     return sql
              

              @staticmethod
              def get_all_count_like_station_period(db:Session,
                                                    cus_act:Stat_customer_action_detail,
                                                    action_type_id:int,
                                                    station_id:int):
                      sql = (db.query(cus_act)
                             .filter(cus_act.action_type_id == action_type_id)
                             .filter(cus_act.station_id == station_id)
                             .count()
                             )
                      
                      return sql
              

              @staticmethod
              def get_count_like_period_none(db:Session,
                                                  cus_act:Stat_customer_action_detail,
                                                  action_type_id:int,
                                                  station_id:int):
                     
                     sql = (db.query(cus_act)
                            .filter(cus_act.action_type_id == action_type_id)
                            .filter(cus_act.station_id == station_id)
                            .filter(cus_act.period_id == None)
                            .count()
                            )
                     return sql
              

              @staticmethod
              def update_count_station(db:Session,
                                       station:Sta_station,
                                       value:int,
                                       station_id:int,
                                       action_type:int):
                     sql = db.query(station).filter(station.id == station_id).first()
                     if sql is not None:
                            if action_type == 1:
                                   sql.count_like = value
                            elif action_type == 2:
                                   sql.count_listen = value
                            elif action_type == 3:
                                   sql.count_share = value
                            elif action_type == 4:
                                   sql.count_comment = value
                            return sql
                     else:
                            return None
              


              @staticmethod
              def update_count_period(db:Session,
                                       period:Sta_station_period,
                                       value:int,
                                       period_id:int,
                                       action_type:int):
                     
                     sql = db.query(period).filter(period.id == period_id).first()
                     
                     if sql is not None:
                            if action_type == 1:
                                   sql.count_like = value
                            elif action_type == 2:
                                   sql.count_listen = value
                            elif action_type == 3:
                                   sql.count_share = value
                            return sql
                     else:
                            return None
                     
              @staticmethod
              def update_count_channel(db:Session,
                                       channel:Sta_channel,
                                       value:int,
                                       channel_id:int,
                                       action_type:int):
                     
                     sql = db.query(channel).filter(channel.id == channel_id).first()
                     if sql is not None:
                            if action_type == 1:
                                   sql.count_like = value
                            elif action_type == 2:
                                   sql.count_listen = value
                            elif action_type == 3:
                                   sql.count_share = value
                            return sql
                     else:
                            return None
              
              @staticmethod
              def get_data_broadcast_by_id(db:Session,
                                           station:Sta_station,
                                           schedule:Sta_station_schedule,
                                           period:Sta_station_period,
                                           id:int):
                      
                     sql = (db.query(station,schedule,period)
                            .join(schedule , station.id == schedule.station_id )
                            .join(period , schedule.id == period.station_schedule_id)
                            .filter(schedule.broadcast_status_id == 5)
                            .filter(period.broadcast_status_id == 5)
                            .filter(station.id == id)
                            .order_by(asc(schedule.schedule_date),asc(period.period_time_start))
                            .all()
                            )
                     return sql
              
              @staticmethod
              def count_all_like_channel(db:Session,
                                         model:Generic[T],
                                         id:int):
                     sql = (db.query(model)
                            .filter(model.id == id )
                            .first()
                            )
                     return sql
              
   
              @staticmethod
              def get_data_like_channel(db:Session,
                                        channel:Sta_channel,
                                        channel_id:int,
                                        score:int):
                     
                     sql = (db.query(channel)
                            .filter(channel.id == channel_id)
                            .first()
                            )
                     
                     sql.count_like = score
                     return sql
              
              @staticmethod
              def check_data_period(db:Session,
                                    period:Sta_station_period,
                                    period_id:int):
                     sql = (db.query(period)
                            .filter(period.id == period_id)
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