from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, null,or_ ,func , cast ,Date ,asc ,case, and_


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
                   Sta_station_schedule,
                   Users,
                   Sta_station_period,
                   Sta_station_playlist_activities,
                   Sta_station_playlist_comments,
                   Sta_period_status,
                   Sta_station_playlist,
                   Sta_station_playlist_history,
                   Sta_station_schedule_activitie
                   )

import pdb




T = TypeVar("T")



class BaseRepo:
    @staticmethod
    def get_data_station_user(db: Session, model: Generic[T]):
        sql =  (db.query(model)
               .filter(model.is_deleted == 'f')
               .all()
               )
        return sql
    
    def update_status_activity(db: Session,
                         id:int,
                         user_id:int,
                         update_time:datetime,
                         Sta_station_playlist_activities:Sta_station_playlist_activities):
        is_deleted = True
        sql = db.query(Sta_station_playlist_activities).filter(Sta_station_playlist_activities.id == id).first()
        sql.is_deleted = is_deleted
        sql.modified_by = user_id,
        sql.modified = update_time,
        return sql
        

    def update_status_comment(db: Session,
                         id:int,
                         user_id:int,
                         update_time:datetime,
                         Sta_station_playlist_comments:Sta_station_playlist_comments):
        is_deleted = True
        sql = db.query(Sta_station_playlist_comments).filter(Sta_station_playlist_comments.id == id).first()
        sql.is_deleted = is_deleted
        sql.modified_by = user_id,
        sql.modified = update_time,
        return sql

  

    def update_station_schedule_status(db: Session,
                         id:int,
                         period_status_id:int,
                         user_id:int,
                         user_id_self:int,
                         update_time:datetime,
                         Sta_station_period:Sta_station_period):
        sql = db.query(Sta_station_period).filter(Sta_station_period.id == id).first()
        sql.period_status_id = period_status_id,
        sql.modified_by = user_id_self,
        sql.modified = update_time,
        sql.user_id = user_id
        return sql


    def get_detail_on_air(db: Session,
                       id:int,
                       Sta_station_period:Sta_station_period,
                       Sta_station_schedule:Sta_station_schedule,
                       Sta_station:Sta_station
                        ):
     
      sql = (db.query(Sta_station_period,Sta_station_schedule,Sta_station)
                   .join(Sta_station_schedule,Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                   .join(Sta_station,Sta_station.id == Sta_station_schedule.station_id)
                   .filter(Sta_station_period.id == id)
                   .all()
      )
      return sql
    


    def get_all_period_activity(db:Session,
                                id:int,
                                Sta_station_playlist:Sta_station_playlist,
                                Sta_station_period:Sta_station_period,
                                Sta_station_playlist_activities:Sta_station_playlist_activities):
        sql = (db.query(Sta_station_playlist,Sta_station_period,Sta_station_playlist_activities)
               .join(Sta_station_playlist,Sta_station_playlist.station_period_id == Sta_station_period.id)
               .join(Sta_station_playlist_activities,Sta_station_playlist_activities.station_playlist_id == Sta_station_playlist.id)
               .filter(Sta_station_period == id)
               ).all()
        

    def get_all_period_comments(db:Session,
                                id:int,
                                Sta_station_playlist:Sta_station_playlist,
                                Sta_station_period:Sta_station_period,
                                Sta_station_playlist_comments:Sta_station_playlist_comments):
        sql = (db.query(Sta_station_playlist,Sta_station_period,Sta_station_playlist_comments)
               .join(Sta_station_playlist,Sta_station_playlist.station_period_id == Sta_station_period.id)
               .join(Sta_station_playlist_comments,Sta_station_playlist_comments.station_playlist_id == Sta_station_playlist.id)
               .filter(Sta_station_period == id)
               ).all()
        
    def find_period(db:Session,
                     id:int,
                     model:Generic[T]):
        sql = db.query(model).filter(model.station_schedule_id == id).filter(model.is_deleted == 'f').all()
        return sql
    
    
    def find_schedule(db:Session,
                     id:int,
                     model:Generic[T]):
        sql = db.query(model).filter(model.id == id).filter(model.is_deleted == 'f').all()
        
        return sql
        
    
    def find_station(db:Session,
                     id:int,
                     model:Generic[T]):
        sql = db.query(model).filter(model.id == id).filter(model.is_deleted == 'f').all()
        return sql
    
    def find_activity(db:Session,
                     id:int,
                     model:Generic[T]):
        sql = db.query(model).filter(model.station_schedule_id == id).filter(model.is_deleted == 'f').all()
        return sql
    
    def find_playlist(db:Session,
                     id:int,
                     model:Generic[T]):
        sql = db.query(model).filter(model.station_period_id == id).filter(model.is_deleted == 'f').all()
       
        return sql
    
    def find_playlist_activity(db:Session,
                     id:int,
                     model:Generic[T]):
        sql = db.query(model).filter(model.station_playlist_id == id).filter(model.is_deleted == 'f').all()
        
        return sql
    
    def find_playlist_comments(db:Session,
                     id:int,
                     model:Generic[T]):
        sql = db.query(model).filter(model.station_playlist_id == id).filter(model.reply_id == None).filter(model.is_deleted == 'f').all()
        return sql
    
    def find_playlist_history(db:Session,
                     id:int,
                     model:Generic[T]):
        sql = db.query(model).filter(model.station_playlist_id == id).filter(model.is_deleted == 'f').all()
        return sql
    
    def check_type(db:Session,
                     id:int,
                     name:str,
                     model:Generic[T],
                     ):
        sql = db.query(model).filter(model.id == id).filter(model.username == name).filter(model.is_deleted == 'f').first()
        return sql
    
    def check_type(db:Session,
                     id:int,
                     name:str,
                     model:Generic[T],
                     ):
        sql = db.query(model).filter(model.id == id).filter(model.username == name).filter(model.is_deleted == 'f').first()
        return sql
    

    def find_user_activity(db:Session,
                     id:int,
                     model:Generic[T]
                     ):
        sql = db.query(model).filter(model.id == id).filter(model.is_deleted == 'f').all()
        return sql
    
    def find_activity_real(db:Session,
                     id:int,
                     model:Generic[T]):
        sql = db.query(model).filter(model.reference_id == id).filter(model.is_deleted == 'f').all()
        
        return sql
    
    def find_reply(db:Session,
                     id:int,
                     model:Generic[T]):
        sql = db.query(model).filter(model.reply_id == id).filter(model.is_deleted == 'f').all()
       
        return sql
    
    @staticmethod
    def get_data_schedule_period(db:Session,
                     Sta_station:Sta_station,
                     Sta_station_schedule:Sta_station_schedule,
                     Sta_station_period:Sta_station_period,
                     id:int
                     ):
        results = (db.query(Sta_station.id,Sta_station_schedule,Sta_station_period)
                    .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                    .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                    )
                 
        return results
        
    @staticmethod
    def get_all_period_data(db:Session,
                     Sta_station:Sta_station,
                     Sta_station_schedule:Sta_station_schedule,
                     Sta_station_period:Sta_station_period,
                     id:int
                     ):
                    
            broadcast_status_name = case(
                
                    (Sta_station_schedule.broadcast_status_id == 3, 'รอออกอากาศ')
                
            ).label('broadcast_status_name')

            period_status_name = case(
                
                    (Sta_station_period.period_status_id == 2, 'ปิดงาน'),
                    (Sta_station_period.period_status_id == 3, 'ขอให้ปรับแก้'),
                    (Sta_station_period.period_status_id == 4, 'ส่งผลการแก้ไข'),
                    (Sta_station_period.period_status_id == 5, 'ปิดงานแก้ไข')
                
            ).label('period_status_name')


            sql = (db.query(Sta_station,Sta_station_schedule,Sta_station_period,broadcast_status_name,period_status_name)
                        .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                        .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                        .filter(Sta_station_period.id == id)
                        .all()
               
                    )
            return sql
    
    @staticmethod
    def get_all_schedule_data(db:Session,
                     Sta_station:Sta_station,
                     Sta_station_schedule:Sta_station_schedule,
                     Sta_station_period:Sta_station_period,
                     id:int
                     ):
        
        sql = (db.query(Sta_station,Sta_station_schedule,Sta_station_period)
                        .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                        .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                        .filter(Sta_station_period.id == id)
                        .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_period.period_time_start),asc(Sta_station_schedule.schedule_number))
                        .all()
               
                    )
        return sql
    

    @staticmethod
    def get_all_station_data(db:Session,
                     Sta_station:Sta_station,
                     Sta_station_schedule:Sta_station_schedule,
                     Sta_station_period:Sta_station_period,
                     id:int
                     ):
        
        sql = (db.query(Sta_station,Sta_station_schedule,Sta_station_period)
                        .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                        .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                        .filter(Sta_station_period.id == id)
                        .all()
               
                    )
        return sql
    

    @staticmethod
    def get_all_playlist_data(db:Session,
                     Sta_station:Sta_station,
                     Sta_station_schedule:Sta_station_schedule,
                     Sta_station_period:Sta_station_period,
                     Sta_station_playlist:Sta_station_playlist,
                     id:int
                     ):
        
        sql = (db.query(Sta_station,Sta_station_schedule,Sta_station_period,Sta_station_playlist)
                        .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                        .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                        .join(Sta_station_playlist, Sta_station_period.id == Sta_station_playlist.station_period_id)
                        .filter(Sta_station_period.id == id)
                        .all()
               
                    )
        return sql
    

    @staticmethod
    def get_all_station_playlist_data(db:Session,
                     Sta_station_playlist_comments:Sta_station_playlist_comments,
                     Member:Member,
                     Users,
                     id:int
                     ):
        
        first_name_case = case(
            (Sta_station_playlist_comments.type_user == 'members', Member.first_name),
            (Sta_station_playlist_comments.type_user == 'users', Users.first_name)
            ).label('firstName')

        last_name_case = case(
            (Sta_station_playlist_comments.type_user == 'members', Member.last_name),
            (Sta_station_playlist_comments.type_user == 'users', Users.last_name)
            ).label('lastName')

        object_key_case = case(
            (Sta_station_playlist_comments.type_user == 'members', Member.object_key),
            (Sta_station_playlist_comments.type_user == 'users', Users.object_key)
            ).label('objectKey')

        username_case = case(
            (Sta_station_playlist_comments.type_user == 'members', Member.username),
            (Sta_station_playlist_comments.type_user == 'users', Users.username)
            ).label('username')
        sql = (db.query(Sta_station_playlist_comments,Member,Users,first_name_case,last_name_case,object_key_case,username_case)
               .outerjoin (Member,and_ (Sta_station_playlist_comments.created_by == Member.id ,Sta_station_playlist_comments.type_user == 'members'))
               .outerjoin (Users, and_(Sta_station_playlist_comments.created_by == Users.id ,Sta_station_playlist_comments.type_user == 'users'))
               .filter(Sta_station_playlist_comments.station_playlist_id == id)
               .filter(Sta_station_playlist_comments.is_deleted == 'f')
               .order_by(asc(Sta_station_playlist_comments.id))
               .all()
               )
        return sql
    
    @staticmethod
    def get_all_station_playlist_activity_data(db:Session,
                     Sta_station_playlist_activities:Sta_station_playlist_activities,
                     id:int
                     ):
        sql = (db.query(Sta_station_playlist_activities)
               .filter(Sta_station_playlist_activities.station_playlist_id == id)
               .filter(Sta_station_playlist_activities.is_deleted == 'f')
               .order_by(asc(Sta_station_playlist_activities.id))
               .all()
               )
        return sql
    
    @staticmethod
    def get_all_station_playlist_history_data(db:Session,
                     Sta_station_playlist_history:Sta_station_playlist_history,
                     id:int
                     ):
        sql = (db.query(Sta_station_playlist_history)
               .filter(Sta_station_playlist_history.station_playlist_id == id)
               .filter(Sta_station_playlist_history.is_deleted == 'f')
               .order_by(desc(Sta_station_playlist_history.id))
               .all()
               )
        return sql
    
    @staticmethod
    def select_update_data(db:Session,
                     Sta_station_period:Sta_station_period,
                     id:int,
                     period_status_id:int,
                     user_id:int,
                     update_time:datetime
                     ):
        sql = db.query(Sta_station_period).filter(Sta_station_period.id == id).first()
        sql.period_status_id = period_status_id,
        sql.modified = update_time,
        sql.modified_by = user_id
        return sql
    
    @staticmethod
    def select_update_playlist(db:Session,
                     Sta_station_playlist:Sta_station_playlist,
                     id:int
                     ):
        sql = db.query(Sta_station_playlist).filter(Sta_station_playlist.station_period_id == id).filter(Sta_station_playlist.is_edit == 't').all()
        return sql
    
    @staticmethod
    def select_update_playlist_2(db:Session,
                     Sta_station_playlist:Sta_station_playlist,
                     id:int
                     ):
        sql = (db.query(Sta_station_playlist)
               .filter(Sta_station_playlist.station_period_id == id)
               .filter(Sta_station_playlist.is_edit == 'f')
               .filter(Sta_station_playlist.station_playlist_status_id == 4)
               .all()
               )
        return sql
    

    @staticmethod
    def update_playlist(db:Session,
                     Sta_station_playlist:Sta_station_playlist,
                     id:int,
                     station_playlist_status_id:int):
        sql = db.query(Sta_station_playlist).filter(Sta_station_playlist.id == id).first()
        sql.station_playlist_status_id = station_playlist_status_id
        return sql
    
    
    @staticmethod
    def update_status_edit(db:Session,
                     Sta_station_playlist:Sta_station_playlist,
                     id:int
                     ):
        sql = db.query(Sta_station_playlist).filter(Sta_station_playlist.id == id).first()
        sql.is_edit = True
        return sql
    
    @staticmethod
    def check_count_playlist_activity(db:Session,
                     model:Generic[T],
                     id:int
                     ):
        sql = (db.query(model)
              .filter(model.station_playlist_id == id)
              .filter(model.is_deleted == 'f')
              .count()               
              )
        return sql
    
    @staticmethod
    def rollback_playlist_data(db:Session,
                     model:Generic[T],
                     id:int
                     ):
        sql = db.query(model).filter(model.id == id).first()
        sql.is_edit = False

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