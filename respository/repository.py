from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session, joinedload ,aliased
from sqlalchemy import desc, null, or_ ,func , cast ,Date ,asc , select ,case ,Time

from sqlalchemy.sql.expression import nulls_last

from datetime import datetime, timedelta ,date
from jose import JWTError, jwt

from config import SECRET_KEY,ALGORITHM

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from model import (Users , 
                   Sta_categories , 
                   Sta_station , 
                   Sta_station_schedule ,
                   Sta_period_types,
                   Sta_station_statuses,
                   Sta_approve_statuses,
                   Member,
                   Sta_station_period,
                   Sta_station_member,
                   Countries,
                    Sta_process_statuses,
                    Sta_broadcast_statuses,
                    Sta_period_status,
                    Sta_broadcast,
                    Sta_station_playlist
                   )

import pdb


T = TypeVar("T")


class Ex_Decode:

    def decode_token(token: str):
         try:
          decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
         
          date_time= datetime.fromtimestamp( decode_token["exp"] )

          return decode_token if date_time >= datetime.now() else None 
         except Exception as ex:
          print(ex)
          return {}


class BaseRepo:
    """
    CRUD
    C = Create
    R = Read
    U = update
    D = Delete
    """

    @staticmethod
    def retrieve_all(db: Session, model: Generic[T]):
        sql =  (db.query(model)
               .filter(model.count_like.isnot(None))
               .order_by(desc(model.count_like))
               .all()
               )
        return sql
    
    @staticmethod
    def test(db: Session, model: Generic[T],keyword:str):
        
        sql =  (db.query(model)
               .filter(model.schedule_number.like(search))
               .all()
               )
        return sql

    # orderby / offset / limit


    @staticmethod
    def get_data_station_user(db: Session,
                              model: Generic[T],
                              offset:int,
                              limit:set,
                              order_direction:str,
                              keyword:str,
                              file_type_media_id:int):
        if keyword is not None:
               search = "%{}%".format(keyword)
        if keyword == '':
               keyword = None
        if order_direction is None:
               order_direction = 'asc'
        
        
        
        if file_type_media_id is None and order_direction == 'asc' and keyword is None:
               sql =  (db.query(model)
               .filter(model.is_deleted == 'f')
               .filter(model.station_id.is_(None))
               .filter(model.channel_id.is_(None))
               .order_by(asc(model.created))
               .offset(offset)
               .limit(limit)
               .all()
               )
     
        elif file_type_media_id is None and order_direction == 'asc' and keyword is not None:
               sql =  (db.query(model)
               .filter(model.is_deleted == 'f')
               .filter(model.station_id.is_(None))
               .filter(model.channel_id.is_(None))
               .filter(model.name.like(search))
               .order_by(asc(model.created))
               .offset(offset)
               .limit(limit)
               .all()
               )

        elif file_type_media_id is None and order_direction == 'desc' and keyword is None:
               sql =  (db.query(model)
               .filter(model.is_deleted == 'f')
               .filter(model.station_id.is_(None))
               .filter(model.channel_id.is_(None))
               .order_by(desc(model.created))
               .offset(offset)
               .limit(limit)
               .all()
               )

        elif file_type_media_id is None and order_direction == 'desc' and keyword is not None:
               sql =  (db.query(model)
               .filter(model.is_deleted == 'f')
               .filter(model.station_id.is_(None))
               .filter(model.channel_id.is_(None))
               .filter(model.name.like(search))
               .order_by(desc(model.created))
               .offset(offset)
               .limit(limit)
               .all()
               )

        elif file_type_media_id is not None and order_direction == 'asc' and keyword is None:
               sql =  (db.query(model)
               .filter(model.is_deleted == 'f')
               .filter(model.station_id.is_(None))
               .filter(model.channel_id.is_(None))
               .filter(model.file_type_media_id == file_type_media_id)
               .order_by(asc(model.created))
               .offset(offset)
               .limit(limit)
               .all()
               )
     
        elif file_type_media_id is not None and order_direction == 'asc' and keyword is not None:
               sql =  (db.query(model)
               .filter(model.is_deleted == 'f')
               .filter(model.station_id.is_(None))
               .filter(model.channel_id.is_(None))
               .filter(model.file_type_media_id == file_type_media_id)
               .filter(model.name.like(search))
               .order_by(asc(model.created))
               .offset(offset)
               .limit(limit)
               .all()
               )

        elif file_type_media_id is not None and order_direction == 'desc' and keyword is None:
               sql =  (db.query(model)
               .filter(model.is_deleted == 'f')
               .filter(model.station_id.is_(None))
               .filter(model.channel_id.is_(None))
               .filter(model.file_type_media_id == file_type_media_id)
               .order_by(desc(model.created))
               .offset(offset)
               .limit(limit)
               .all()
               )

        elif file_type_media_id is not None and order_direction == 'desc' and keyword is not None:
               sql =  (db.query(model)
               .filter(model.is_deleted == 'f')
               .filter(model.station_id.is_(None))
               .filter(model.channel_id.is_(None))
               .filter(model.file_type_media_id == file_type_media_id)
               .filter(model.name.like(search))
               .order_by(desc(model.created))
               .offset(offset)
               .limit(limit)
               .all()
               )

        
        return sql
    

    @staticmethod
    def get_data_kind_media(db: Session,
                            model: Generic[T],
                            id:int):
         sql = db.query(model).filter(model.id == id).first()

         return sql
    

    @staticmethod
    def count_data_station_user(db: Session,
                              model: Generic[T],
                              keyword:str,
                              file_type_media_id:int):
         
         if keyword is not None:
               search = "%{}%".format(keyword)
         if keyword == '':
               keyword = None

         
         if file_type_media_id is None and keyword is None:
               sql =  (db.query(model)
               .filter(model.is_deleted == 'f')
               .filter(model.station_id.is_(None))
               .filter(model.channel_id.is_(None))
               .count()
               )
     
         elif file_type_media_id is None and keyword is not None:
               sql =  (db.query(model)
               .filter(model.is_deleted == 'f')
               .filter(model.station_id.is_(None))
               .filter(model.channel_id.is_(None))
               .filter(model.name.like(search))
               
               .count()
               )
         elif file_type_media_id is not None and keyword is None:
               sql =  (db.query(model)
               .filter(model.is_deleted == 'f')
               .filter(model.station_id.is_(None))
               .filter(model.channel_id.is_(None))
               .filter(model.file_type_media_id == file_type_media_id)
               .count()
               )
     
         elif file_type_media_id is not None and keyword is not None:
               sql =  (db.query(model)
               .filter(model.is_deleted == 'f')
               .filter(model.station_id.is_(None))
               .filter(model.channel_id.is_(None))
               .filter(model.file_type_media_id == file_type_media_id)
               .filter(model.name.like(search))
               .count()
               )
    
         return sql
         


    @staticmethod
    def search_value(db: Session, model: Generic[T], offset:int, limit:int, keyword: Optional[str] = None):
        check_str = keyword.isnumeric()
        if check_str == True:
            return db.query(model).filter(or_(model.code == keyword, model.category_id == keyword)).offset(offset).limit(limit).all()
        else:
            return db.query(model).filter(model.name.like(keyword)).offset(offset).limit(limit).all()
    # orderby / offset / limit

    @staticmethod
    def find_all_member(db: Session, Member: Member):
        results = db.query(func.count(Member.id)).filter(Member.is_deleted == 'f').scalar()
        return results
    
    @staticmethod
    def find_all_station(db: Session, Sta_station: Sta_station):
        results = db.query(func.count(Sta_station.id)).filter(Sta_station.is_deleted == 'f').scalar()
        return results
    
    @staticmethod
    def find_all_station_schedule(db: Session, Sta_station_schedule: Sta_station_schedule):
        results = db.query(func.count(Sta_station_schedule.id)).filter(Sta_station_schedule.broadcast_status_id == 4).filter(Sta_station_schedule.is_deleted == 'f').scalar()
        return results
    

    @staticmethod
    def find_all_max_station(db: Session, Sta_station: Sta_station):
        results = db.query(func.count(Sta_station.id)).filter(Sta_station_schedule.is_deleted == 'f').scalar()
        return results
    
    @staticmethod
    def find_all_active_station(db: Session, Sta_station: Sta_station):
        results = db.query(func.count(Sta_station.id)).filter(Sta_station.station.station_status_id == '1').filter(Sta_station_schedule.is_deleted == 'f').scalar()
        return results
    
    @staticmethod
    def find_all_max_schedule(db: Session, Sta_station: Sta_station):
        results = db.query(func.count(Sta_station.id)).filter(Sta_station.station.station_status_id == '1').filter(Sta_station_schedule.is_deleted == 'f').scalar()
        return results
    
    @staticmethod
    def find_all_max_schedule_count_all(db: Session, Sta_station_schedule: Sta_station_schedule):
        results = db.query(func.count(Sta_station_schedule.id)).filter(Sta_station_schedule.is_deleted == 'f').scalar()
        return results
    
    @staticmethod
    def find_all_max_schedule_count(db: Session,
                                 Sta_station_schedule:Sta_station_schedule,
                                 Member:Member,
                                 Sta_station:Sta_station,
                                 date:date,
                                 offset:int,
                                 limit:int,
                                 type:str,
                                 order_by:str,
                                 order_direction:str,
                                 keyword:str,
                                 ):
        
        if keyword is not None:
            search = "%{}%".format(keyword)
        if keyword == '':
           keyword = None
        if order_direction is None:
           order_direction = 'asc'
        if date is None and type is None and order_direction == None and keyword is None:
            print("count1")
            results = (db.query(Sta_station_schedule, Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.is_deleted == "f")
             .count()
             )
        elif date is None and type is None and order_direction == None and keyword is not None:
            print("count2")
            results = (db.query(Sta_station_schedule, Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.name.like(keyword),Sta_station_schedule.schedule_number.like(keyword)))
             .count()
             )
        elif date is None and type is None and order_direction == 'desc' and keyword is None:
             results = (db.query(Sta_station_schedule, Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.is_deleted == "f")
             .count()
             )

        elif date is None and type is None and order_direction == 'desc' and keyword is not None:
             print("count3")
             results = (db.query(Sta_station_schedule, Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.name.like(search),Sta_station_schedule.schedule_number.like(search)))
             .count()
             )

        elif date is None and type is None and order_direction == 'asc' and keyword is None:
            print("count4")
            results = (db.query(Sta_station_schedule, Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.is_deleted == "f")
             .count()
             )
            
        elif date is None and type is None and order_direction == 'asc' and keyword is not None:
            print("count5")
            results = (db.query(Sta_station_schedule, Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.name.like(search),Sta_station_schedule.schedule_number.like(search)))
             .count()
             )
        
        elif type == 'lasted-schedule' and  order_direction == 'desc' and keyword is None:
             print("count6")
             results = (db.query(Sta_station_schedule, Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(cast(Sta_station_schedule.created, Date) == date)
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(Sta_station_schedule.process_status_id == 3)
             .count()
             )

        elif type == 'lasted-schedule' and  order_direction == 'desc' and keyword is not None:
             results = (db.query(Sta_station_schedule, Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(cast(Sta_station_schedule.created, Date) == date)
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(Sta_station_schedule.process_status_id == 3)
             .filter(or_(Sta_station_schedule.name.like(search),Sta_station_schedule.schedule_number.like(search)))
             .count()
             )


        elif type == 'lasted-schedule' and order_direction == 'asc' and keyword is None:
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(cast(Sta_station_schedule.created, Date) == date)
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(Sta_station_schedule.process_status_id == 3)
             .count()
             )


        elif type == 'lasted-schedule' and order_direction == 'asc' and keyword is not None:
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(cast(Sta_station_schedule.created, Date) == date)
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(Sta_station_schedule.process_status_id == 3)
             .filter(or_(Sta_station_schedule.name.like(search),Sta_station_schedule.schedule_number.like(search)))
             .count()
             )
        
         
        elif type == 'on-air' and order_direction == 'desc':
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.broadcast_status_id == '5')
             .filter(Sta_station_schedule.is_deleted == "f")
             .count()
             )

        elif type == 'on-air' and order_direction == 'asc':
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.broadcast_status_id == '5')
             .filter(Sta_station_schedule.is_deleted == "f")
             .count()
             )

        elif type == 'status-edit' and order_direction == 'desc' and keyword is None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '4')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )


        elif type == 'status-edit' and order_direction == 'asc' and keyword is None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '4')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )


        elif type == 'status-edit' and order_direction == 'desc' and keyword is not None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '4')
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.schedule_number.like(search) , Member.first_name.like(search) , Sta_station_schedule.process_status_id.like(search)))
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )


        elif type == 'status-edit' and order_direction == 'asc' and keyword is not None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '4')
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.schedule_number.like(search) , Member.first_name.like(search) , Sta_station_schedule.process_status_id.like(search)))
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )

        elif type == 'status-consider' and order_direction == 'desc' and keyword is None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '3')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )

        elif type == 'status-consider' and order_direction == 'asc' and keyword is None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '3')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(asc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )

        elif type == 'status-consider' and order_direction == 'desc' and keyword is not None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '3')
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.schedule_number.like(search) , Member.first_name.like(search) , Sta_station_schedule.process_status_id.like(search)))
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )

        elif type == 'status-consider' and order_direction == 'asc' and keyword is not None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '3')
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.schedule_number.like(search) , Member.first_name.like(search) , Sta_station_schedule.process_status_id.like(search)))
             .order_by(asc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )

        elif type == 'status-approve' and order_direction == 'desc' and keyword is None:
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '7')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )

        elif type == 'status-approve' and order_direction == 'asc' and keyword is None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '7')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(asc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )

        elif type == 'status-approve' and order_direction == 'desc' and keyword is not None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '7')
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.schedule_number.like(search) , Member.first_name.like(search) , Sta_station_schedule.process_status_id.like(search)))
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )

        elif type == 'status-approve' and order_direction == 'asc' and keyword is not None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '7')
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.schedule_number.like(search) , Member.first_name.like(search) , Sta_station_schedule.process_status_id.like(search)))
             .order_by(asc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )

        elif type == 'status-disapproved' and order_direction == 'desc' and keyword is  None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '8')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )

        elif type == 'status-disapproved' and order_direction == 'asc' and keyword is  None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '8')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(asc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )
            
        elif type == 'status-disapproved' and order_direction == 'desc' and keyword is not None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '10')
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.schedule_number.like(search) , Member.first_name.like(search) , Sta_station_schedule.process_status_id.like(search)))
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )

        elif type == 'status-prepare' and order_direction == 'desc' and keyword is None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '10')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )

        elif type == 'status-prepare' and order_direction == 'asc' and keyword is None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '10')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )

        elif type == 'status-prepare' and order_direction == 'desc' and keyword is not None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '10')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )

        elif type == 'status-prepare' and order_direction == 'asc' and keyword is not None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '10')
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.schedule_number.like(search) , Member.first_name.like(search) , Sta_station_schedule.process_status_id.like(search)))
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )

        elif type == 'status-broadcast' and order_direction == 'desc' and keyword is None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '11')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )

        elif type == 'status-broadcast' and order_direction == 'asc' and keyword is None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '11')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )

        elif type == 'status-broadcast' and order_direction == 'desc' and keyword is not None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '11')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )

        elif type == 'status-broadcast' and order_direction == 'asc' and keyword is not None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '11')
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.schedule_number.like(search) , Member.first_name.like(search) , Sta_station_schedule.process_status_id.like(search)))
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .count()
             )

        
             
        else:
            results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.is_deleted == "f")
             .count()
             )
        
        return results
    
    
    
    
   
   
    @staticmethod
    def get_all_station_schedule(db: Session,
                                 Sta_station_schedule:Sta_station_schedule,
                                 Member:Member,
                                 Sta_station:Sta_station,
                                 date:date,
                                 offset:int,
                                 limit:int,
                                 type:str,
                                 order_by:str,
                                 order_direction:str,
                                 keyword:str,
                                 ):
        
        if keyword is not None:
            search = "%{}%".format(keyword)
        if keyword == '':
           keyword = None
        if order_direction is None:
           order_direction = 'asc'
        if date is None and type is None and order_direction is None and  keyword is None:
            print("1")
            results = (db.query(Sta_station_schedule, Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.is_deleted == "f")
             .offset(offset)
             .limit(limit)
             .all()
             )
            
        elif date is None and type is None and order_direction is None and keyword is not None:
            print("2")
            results = (db.query(Sta_station_schedule, Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.name.like(search),Sta_station_schedule.schedule_number.like(search)))
             .filter(Sta_station_schedule.name == keyword)
             .offset(offset)
             .limit(limit)
             .all()
             )
        
        elif date is None and type is None and order_direction == 'desc' and keyword is None:
             print("3")
             results = (db.query(Sta_station_schedule, Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif date is None and type is None and order_direction == 'desc' and keyword is not None:
             print("4")
             results = (db.query(Sta_station_schedule, Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.name.like(search),Sta_station_schedule.schedule_number.like(search)))
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )
            
        
        elif date is None and type is None and order_direction == 'asc' and keyword is None:
            print("5")
            results = (db.query(Sta_station_schedule, Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(asc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )
            
        elif date is None and type is None and order_direction == 'asc' and keyword is not None:
            print("6")
            results = (db.query(Sta_station_schedule, Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.name.like(search),Sta_station_schedule.schedule_number.like(search)))
             .order_by(asc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )
        
        elif type == 'lasted-schedule' and  order_direction == 'desc' and keyword is None:
             print("7")
             results = (db.query(Sta_station_schedule, Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(cast(Sta_station_schedule.created, Date) == date)
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(Sta_station_schedule.process_status_id == 3)
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'lasted-schedule' and  order_direction == 'desc' and keyword is not None:
             print("8")
             results = (db.query(Sta_station_schedule, Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(cast(Sta_station_schedule.created, Date) == date)
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(Sta_station_schedule.process_status_id == 3)
             .filter(or_(Sta_station_schedule.name.like(search),Sta_station_schedule.schedule_number.like(search)))
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )


        elif type == 'lasted-schedule' and order_direction == 'asc' and keyword is None:
             print("9")
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(cast(Sta_station_schedule.created, Date) == date)
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(Sta_station_schedule.process_status_id == 3)
             .order_by(asc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )


        elif type == 'lasted-schedule' and order_direction == 'asc' and keyword is not None:
             print("10")
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(cast(Sta_station_schedule.created, Date) == date)
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(Sta_station_schedule.process_status_id == 3)
             .filter(or_(Sta_station_schedule.name.like(search),Sta_station_schedule.schedule_number.like(search)))
             .order_by(asc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )
        
         
        elif type == 'on-air' and order_direction == 'desc':
             print("11")
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.broadcast_status_id == '5')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(asc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'on-air' and order_direction == 'asc':
             print("12")
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.broadcast_status_id == '5')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(asc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'status-edit' and order_direction == 'desc' and keyword is None:
             print("13") 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '4')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )


        elif type == 'status-edit' and order_direction == 'asc' and keyword is None: 
             print("14")
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '4')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )


        elif type == 'status-edit' and order_direction == 'desc' and keyword is not None: 
             print("15")
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '4')
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.schedule_number.like(search) , Member.first_name.like(search) , Sta_station_schedule.process_status_id.like(search)))
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )


        elif type == 'status-edit' and order_direction == 'asc' and keyword is not None: 
             print("16")
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '4')
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.schedule_number.like(search) , Member.first_name.like(search) , Sta_station_schedule.process_status_id.like(search)))
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'status-consider' and order_direction == 'desc' and keyword is None: 
             print("17")
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '3')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'status-consider' and order_direction == 'asc' and keyword is None: 
             print("18")
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '3')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(asc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'status-consider' and order_direction == 'desc' and keyword is not None: 
             print("19")
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '3')
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.schedule_number.like(search) , Member.first_name.like(search) , Sta_station_schedule.process_status_id.like(search)))
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'status-consider' and order_direction == 'asc' and keyword is not None: 
             print("20")
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '3')
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.schedule_number.like(search) , Member.first_name.like(search) , Sta_station_schedule.process_status_id.like(search)))
             .order_by(asc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'status-approve' and order_direction == 'desc' and keyword is None:
             print("21")
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '7')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'status-approve' and order_direction == 'asc' and keyword is None: 
             print("22")
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '7')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(asc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'status-approve' and order_direction == 'desc' and keyword is not None: 
             print("23")
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '7')
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.schedule_number.like(search) , Member.first_name.like(search) , Sta_station_schedule.process_status_id.like(search)))
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'status-approve' and order_direction == 'asc' and keyword is not None: 
             print("24")
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '7')
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.schedule_number.like(search) , Member.first_name.like(search) , Sta_station_schedule.process_status_id.like(search)))
             .order_by(asc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'status-disapproved' and order_direction == 'desc' and keyword is  None: 
             print("25")
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '8')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'status-disapproved' and order_direction == 'asc' and keyword is  None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '8')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(asc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )
            
        elif type == 'status-disapproved' and order_direction == 'desc' and keyword is not None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '10')
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.schedule_number.like(search) , Member.first_name.like(search) , Sta_station_schedule.process_status_id.like(search)))
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'status-prepare' and order_direction == 'desc' and keyword is None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '10')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'status-prepare' and order_direction == 'asc' and keyword is None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '10')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'status-prepare' and order_direction == 'desc' and keyword is not None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '10')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'status-prepare' and order_direction == 'asc' and keyword is not None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '10')
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.schedule_number.like(search) , Member.first_name.like(search) , Sta_station_schedule.process_status_id.like(search)))
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'status-broadcast' and order_direction == 'desc' and keyword is None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '11')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'status-broadcast' and order_direction == 'asc' and keyword is None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '11')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'status-broadcast' and order_direction == 'desc' and keyword is not None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '11')
             .filter(Sta_station_schedule.is_deleted == "f")
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        elif type == 'status-broadcast' and order_direction == 'asc' and keyword is not None: 
             results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .join (Sta_station,Sta_station.id == Sta_station_schedule.station_id)
             .filter(Sta_station_schedule.process_status_id == '11')
             .filter(Sta_station_schedule.is_deleted == "f")
             .filter(or_(Sta_station_schedule.schedule_number.like(search) , Member.first_name.like(search) , Sta_station_schedule.process_status_id.like(search)))
             .order_by(desc(Sta_station_schedule.created))
             .offset(offset)
             .limit(limit)
             .all()
             )

        
             
             
        else:
            print("Hi")
            results = (db.query(Sta_station_schedule , Member,Sta_station)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .filter(cast(Sta_station_schedule.created, Date) == date)
             .filter(Sta_station_schedule.is_deleted == "f")
             .offset(offset)
             .limit(limit)
             .all()
             )
            

       
    
        return results

    @staticmethod
    def get_all_station_test(db: Session,Sta_station: Sta_station ,type:str, offset:int , limit:int):
        if type == 'is_popular':
            results = (db.query(Sta_station_schedule , Member)
             .join (Member, Member.id == Sta_station_schedule.created_by)
             .order_by(desc(Sta_station.created))
             .offset(offset)
             .limit(limit)
             .all()
             )


        return results
    



    @staticmethod
    def get_all_station_popular(db: Session,
                                Sta_station: Sta_station,
                                Sta_station_statuses:Sta_station_statuses,
                                Member:Member,
                                offset:int,
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
        if type == '':
               type = None
        
        if type == 'is_popular':
            print("1")
            results = (db.query(Sta_station,Sta_station_statuses,Member)
            .join(Sta_station_statuses,Sta_station.station_status_id == Sta_station_statuses.id)
            .join(Member, Member.id == Sta_station.created_by)
            .filter(Sta_station.approve_status_id == 1)
            .filter(Sta_station.is_deleted == 'f')
            .order_by(asc(Sta_station_statuses.id),desc(Sta_station.id))
            .offset(offset)
            .limit(limit)
            .all()
            )
        elif type is None and order_direction == 'desc' and keyword is None:
            print("2")
            results = (db.query(Sta_station,Sta_station_statuses,Member)
            .join(Sta_station_statuses,Sta_station.station_status_id == Sta_station_statuses.id)
            .join(Member, Member.id == Sta_station.created_by)
            .filter(Sta_station.approve_status_id == 1)
            .filter(Sta_station.is_deleted == 'f')
            .order_by(asc(Sta_station_statuses.id),desc(Sta_station.id))
            .offset(offset)
            .limit(limit)
            .all()
            )

        elif type is None and order_direction == 'desc' and keyword is not None:
            print("3")
            results = (db.query(Sta_station,Sta_station_statuses,Member)
            .join(Sta_station_statuses,Sta_station.station_status_id == Sta_station_statuses.id)
            .join(Member, Member.id == Sta_station.created_by)
            .filter(Sta_station.approve_status_id == 1)
            .filter(Sta_station.is_deleted == 'f')
            .filter(Sta_station.name.like(search))
            .order_by(asc(Sta_station_statuses.id),desc(Sta_station.id))
            .offset(offset)
            .limit(limit)
            .all()
            )


        elif type is None and order_direction == 'asc' and keyword is None:
            print("4")
            results = (db.query(Sta_station,Sta_station_statuses,Member)
            .join(Sta_station_statuses,Sta_station.station_status_id == Sta_station_statuses.id)
            .join(Member, Member.id == Sta_station.created_by)
            .filter(Sta_station.is_deleted == 'f')
            .filter(Sta_station.approve_status_id == 1)
            .order_by(desc(Sta_station_statuses.id),asc(Sta_station.id))
            .offset(offset)
            .limit(limit)
            .all()
            )

        elif type is None and order_direction == 'asc' and keyword is not None:
            print("5")
            results = (db.query(Sta_station,Sta_station_statuses,Member)
            .join(Sta_station_statuses,Sta_station.station_status_id == Sta_station_statuses.id)
            .join(Member, Member.id == Sta_station.created_by)
            .filter(Sta_station.approve_status_id == 1)
            .filter(Sta_station.is_deleted == 'f')
            .filter(Sta_station.name.like(search))
            .order_by(desc(Sta_station_statuses.id),asc(Sta_station.id))
            .offset(offset)
            .limit(limit)
            .all()
            )

        return results


    @staticmethod
    def count_all_station_popular(db: Session,
                                Sta_station: Sta_station,
                                Sta_station_statuses:Sta_station_statuses,
                                Member:Member,
                                keyword:str):
        if keyword is not None:
                search = "%{}%".format(keyword)
        if keyword == '':
                keyword = None
       
            
        
        if keyword is None:
            results = (db.query(Sta_station,Sta_station_statuses,Member)
            .join(Sta_station_statuses,Sta_station.station_status_id == Sta_station_statuses.id)
            .join(Member, Member.id == Sta_station.created_by)
            .filter(Sta_station.approve_status_id == 1)
            .filter(Sta_station.is_deleted == 'f')
            .count()
            )

        elif keyword is not None:

            results = (db.query(Sta_station,Sta_station_statuses,Member)
            .join(Sta_station_statuses,Sta_station.station_status_id == Sta_station_statuses.id)
            .join(Member, Member.id == Sta_station.created_by)
            .filter(Sta_station.approve_status_id == 1)
            .filter(Sta_station.is_deleted == 'f')
            .filter(Sta_station.name.like(search))
            .count()
            )

        return results
    
    @staticmethod
    def find_data_member(db: Session,
                         model: Generic[T],
                         member_id:int):
         sql = db.query(model).filter(model.id == member_id).first()
         
         return sql

    
    @staticmethod
    def get_all_initial(db: Session, model: Generic[T]):
        sql = db.query(model).order_by(asc(model.id)).all()
        return sql
    
    @staticmethod
    def get_all_initial_broadcast(db: Session, model: Generic[T]):
        sql = db.query(model).order_by(asc(model.id)).all()
        return sql




    @staticmethod
    def retrieve_by_id(db: Session, model: Generic[T], id: int):
        return db.query(model).filter(model.id == id).all()
    
    
    #Sta_categories , Sta_station , Sta_station_schedule ,Sta_Period_Types
    @staticmethod
    def get_all_query_master(db: Session, Sta_categories:Sta_categories):
        
        sql = db.query(Sta_categories).all()

        return sql
    @staticmethod
    def get_all_query_master_period_types(db: Session, Sta_period_types:Sta_period_types):
        
        sql2 = db.query(Sta_period_types).all()

        return sql2
    
    @staticmethod
    def update_status_station(db: Session, Sta_station_schedule:Sta_station_schedule , station_schedule_id:int, process_status:int , type:str):
        if type == 'status':
            sql = db.query(Sta_station_schedule).filter(Sta_station_schedule.id == station_schedule_id).first()
            sql.process_status = process_status
        elif type == 'update':
            sql = db.query(Sta_station_schedule).filter(Sta_station_schedule.id == station_schedule_id).first()
          
            sql.is_deleted = True
        return sql
    
    
    @staticmethod
    def get_data_url_all(db: Session,
                      Sta_station_schedule:Sta_station_schedule,
                      Sta_station_period:Sta_station_period,
                      date:date,
                      id:int):
         
         sql = (db.query(Sta_station_schedule,Sta_station_period)
                .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                .filter(Sta_station_schedule.station_id == id)
                .filter(Sta_station_period.is_deleted == 'f')
                .filter(Sta_station_schedule.is_deleted == 'f')
                .filter(cast(Sta_station_schedule.schedule_date, Date) == date)
                .order_by(desc(Sta_station_schedule.id),asc(Sta_station_period.id))
                .all()
                )
         
         return sql

    @staticmethod
    def update_status_suspend(db: Session,
                      model: Generic[T],
                      user_id:int,
                      id:int,
                      station_status_id:int,
                      start:datetime,
                      end:datetime,
                      comment:str,
                      disable_comment:str,
                      update_time:datetime):
         sql = db.query(model).filter(model.id == id).first()
         sql.is_enabled = False
         sql.is_deleted = False
         sql.station_status_id = 2
         sql.modified_by = user_id
         sql.modified = update_time
         sql.suspend_date_start= start
         sql.suspend_date_end = end
         sql.suspend_comment = comment
         sql.disable_comment = disable_comment

         return sql
    


    @staticmethod
    def update_status_suspend_schedule(db: Session,
                      Sta_station_schedule: Sta_station_schedule,
                      user_id:int,
                      id:int,
                      update_time:datetime):
          
          sql = db.query(Sta_station_schedule).filter(Sta_station_schedule.id == id).first()
          sql.broadcast_status_id = 4
          sql.broadcast_status_date = update_time
          sql.modified = update_time
          sql.modified_by = user_id
          return sql
    

    @staticmethod
    def update_status_suspend_period(db: Session,
                      Sta_station_period: Sta_station_period,
                      user_id:int,
                      id:int,
                      update_time:datetime):
         sql = db.query(Sta_station_period).filter(Sta_station_period.id == id).first()
         sql.broadcast_status_id = 4
         sql.broadcast_status_date = update_time
         sql.modified = update_time
         sql.modified_by = user_id
         return sql

         
    


    @staticmethod
    def get_broadcast_main(db: Session,
                      Sta_station_schedule:Sta_station_schedule,
                      current_date:date,
                      id:int):
          sql = (db.query(Sta_station_schedule)
                 .filter(Sta_station_schedule.station_id == id)
                 .filter(cast(Sta_station_schedule.schedule_date, Date) == current_date)
                 .order_by(asc(Sta_station_schedule.broadcast_url))
                 .first()
                 )
          return sql
    

    @staticmethod
    def update_status_use(db: Session,
                      model: Generic[T],
                      id:int,
                      user_id:int,
                      station_status_id:int,
                      update_time:datetime):
         sql = db.query(model).filter(model.id == id).first()
         sql.is_enabled = True
         sql.is_deleted = False
         sql.station_status_id = 1
         sql.modified_by = user_id
         sql.modified = update_time
         return sql
    
    @staticmethod
    def check_status_station(db: Session,
                      model: Generic[T],
                      id:int):
         sql = db.query(model).filter(model.id == id).first()
         return sql
    

    @staticmethod
    def update_status_delete(db: Session,
                      model: Generic[T],
                      id:int,
                      user_id:int,
                      station_status_id:int,
                      update_time:datetime):
         sql = db.query(model).filter(model.id == id).first()
         sql.is_enabled = False
         sql.is_deleted = False
         sql.station_status_id = 3,
         sql.modified_by = user_id,
         sql.deleted_date = update_time,
         sql.modified = update_time
         return sql
    
    @staticmethod
    def update_status_close(db: Session,
                      model: Generic[T],
                      user_id:int,
                      id:int,
                      station_status_id:int,
                      disable_comment:str,
                      update_time:datetime):
         sql = db.query(model).filter(model.id == id).first()
         sql.is_enabled = False
         sql.is_deleted = False
         sql.station_status_id = 4,
         sql.modified_by = user_id,
         sql.disable_comment = disable_comment,
         sql.modified = update_time
         return sql
    
    @staticmethod
    def update_resume_shchedule(db: Session,
                                Sta_station_schedule:Sta_station_schedule,
                                id:int,
                                user_id:int,
                                time:datetime,
                                broadcast_status_id:int):
         sql = db.query(Sta_station_schedule).filter(Sta_station_schedule.id == id).first()
         sql.broadcast_status_id = broadcast_status_id
         sql.broadcast_status_date = time
         sql.modified_by = user_id
         sql.modified = time
         return sql
         
    
    @staticmethod
    def update_resume_shchedule_special(db: Session,
                                Sta_station_schedule:Sta_station_schedule,
                                id:int,
                                user_id:int,
                                time:datetime,
                                broadcast_status_id:int):
         sql = db.query(Sta_station_schedule).filter(Sta_station_schedule.id == id).first()
         sql.broadcast_status_id = broadcast_status_id
         sql.broadcast_status_date = time
         sql.modified_by = user_id
         sql.modified = time
         sql.service_stop_date = None
         return sql
    

    @staticmethod
    def update_resume_period(db: Session,
                                Sta_station_period:Sta_station_period,
                                id:int,
                                user_id:int,
                                time:datetime,
                                broadcast_status_id:int):
         sql = db.query(Sta_station_period).filter(Sta_station_period.id == id).first()
         sql.broadcast_status_id = broadcast_status_id
         sql.broadcast_status_date = time
         sql.modified_by = user_id
         sql.modified = time
         return sql

    
    @staticmethod
    def delete_by_id(db: Session, model: Generic[T], id: int , user_id:int , time_update:datetime):
        sql =  db.query(model).filter(model.id == id).first()
        sql.is_deleted = True
        sql.modified_by = user_id,
        sql.modified = time_update
        return sql
    
    @staticmethod
    def update_station_member(
        db: Session,
        model: Generic[T],
        time_update:datetime,
        id:int,
        member_id : int,
        station_id : int ,
        is_owner : str
    ):
        sql = db.query(model).filter(model.id == id).first()
        sql.modified_by = member_id,
        sql.station_id = station_id,
        sql.member_id = member_id,
        sql.is_owner =  is_owner,

        return sql
    
    """
    Media
    """
    @staticmethod
    def get_all_file_media(db: Session, model: Generic[T]):
        sql =  (db.query(model)
               .filter(model.is_deleted == 'f')
               .all()
               )
        return sql
    
    
    @staticmethod
    def get_all_data_list_file_type_media(db: Session, 
                                          model: Generic[T],
                                          offset:int,
                                          limit:int,
                                          order_direction:str,
                                          keyword):
        if keyword is not None:
               search = "%{}%".format(keyword)
        if keyword == '':
               keyword = None
        if order_direction is None:
               order_direction = 'asc'

        if order_direction == 'asc' and keyword is None:
               sql = (db.query(model)
               .filter(model.is_deleted == 'f')
               .order_by(asc(model.created))
               .offset(offset)
               .limit(limit)
               .all()
               )
     
        elif order_direction == 'asc' and keyword is not None:
               sql =  (db.query(model)
               .filter(model.is_deleted == 'f')
               .filter(model.name.like(search))
               .order_by(asc(model.created))
               .offset(offset)
               .limit(limit)
               .all()
               )

        elif order_direction == 'desc' and keyword is None:
               sql =  (db.query(model)
               .filter(model.is_deleted == 'f')
               .order_by(desc(model.created))
               .offset(offset)
               .limit(limit)
               .all()
               )

        elif order_direction == 'desc' and keyword is not None:
               sql =  (db.query(model)
               .filter(model.is_deleted == 'f')
               .filter(model.name.like(search))
               .order_by(desc(model.created))
               .offset(offset)
               .limit(limit)
               .all()
               )

        
        return sql
    

    @staticmethod
    def update_file_media(
        db: Session,
        model: Generic[T],
        id:int,
        member_id : int,
        time_update:datetime,
        name : str ,
        file_status_id : int
   
    ):
        sql = db.query(model).filter(model.id == id).first()
        sql.modified = time_update
        sql.modified_by = member_id
        sql.name = name
        sql.file_status_id = file_status_id
        return sql
    
    @staticmethod
    def update_file_media_with_key(
        db: Session,
        model: Generic[T],
        id:int,
        member_id : int,
        time_update:datetime,
        name : str ,
        file_status_id : int,
        object_key:str,
        url:str,
        file_size:int,
        mime_type:str,
        file_name:str
   
    ):
        sql = db.query(model).filter(model.id == id).first()
        sql.modified = time_update
        sql.modified_by = member_id
        sql.name = name
        sql.file_status_id = file_status_id
        sql.object_key = object_key
        sql.file_path = url
        sql.file_size = file_size
        sql.file_type = mime_type
        sql.file_name = file_name
        return sql
    
    @staticmethod
    def update_file_type_media(db:Session,
                               model: Generic[T],
                               id:int,
                               time_update:datetime,
                               modified_by:int,
                               name:str,
                               description:str):
        sql = db.query(model).filter(model.id == id).first()
        sql.modified = time_update,
        sql.modified_by = modified_by,
        sql.name = name,
        sql.description = description

        return sql
    
    @staticmethod
    def update_file_status_media(db:Session,
                               model: Generic[T],
                               user_id:int,
                               file_status_id:int,
                               id,
                               time_update:datetime):
        sql = db.query(model).filter(model.id == id).first()
        sql.modified = time_update,
        sql.modified_by = user_id,
        sql.file_status_id = file_status_id

        return sql
    
 
    @staticmethod
    def get_total_data(db: Session, 
                    Sta_station:Sta_station,
                    Member:Member,
                    Sta_station_member:Sta_station_member,
                    Sta_station_statuses:Sta_station_statuses,
                    Sta_approve_statuses:Sta_approve_statuses,
                    Countries:Countries):
    
        sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.is_deleted == 'f')
                    .count()
                    )
               
        return sql
    
   
    


    @staticmethod
    def get_new_data(db: Session, 
                    Sta_station:Sta_station,
                    Member:Member,
                    Sta_station_member:Sta_station_member,
                    Sta_station_statuses:Sta_station_statuses,
                    Sta_approve_statuses:Sta_approve_statuses,
                    Countries:Countries):
       

          

        sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_approve_statuses.id.is_(None))
                    .filter(Sta_station.is_deleted == 'f')
                    .count()
                    )
               
        return sql
    


    @staticmethod
    def get_approve_data(db: Session, 
                    Sta_station:Sta_station,
                    Member:Member,
                    Sta_station_member:Sta_station_member,
                    Sta_station_statuses:Sta_station_statuses,
                    Sta_approve_statuses:Sta_approve_statuses,
                    Countries:Countries):
   
        sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_approve_statuses.id == 1)
                    .filter(Sta_station.is_deleted == 'f')
                    .count()
                    )
       
        return sql


    @staticmethod
    def get_disapprove_data(db: Session, 
                    Sta_station:Sta_station,
                    Member:Member,
                    Sta_station_member:Sta_station_member,
                    Sta_station_statuses:Sta_station_statuses,
                    Sta_approve_statuses:Sta_approve_statuses,
                    Countries:Countries):
 
        sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_approve_statuses.id == 2)
                    .filter(Sta_station.is_deleted == 'f')
                    .count()
                    ) 

        return sql
    

    


         
    @staticmethod  
    def get_all_list_regis(db: Session, 
                           Sta_station:Sta_station,
                           Member:Member,
                           Sta_station_member:Sta_station_member,
                           Sta_station_statuses:Sta_station_statuses,
                           Sta_approve_statuses:Sta_approve_statuses,
                           Countries:Countries,
                           offset:int,
                           limit:int,
                           order_direction:str,
                           keyword:str,
                           type:str):
         
        first_name = None
        last_name = None
        if keyword is not None:
             if ' ' in keyword:
                    names = keyword.split()
                    first_name = names[0]
                    last_name = names[1]
                    first_name = "%{}%".format(first_name)
                    last_name = "%{}%".format(last_name)
                    search = "%{}%".format(keyword)
             else:
                    search = "%{}%".format(keyword)
        if keyword == '':
               keyword = None
        if order_direction is None:
               order_direction = 'asc'
        if type is None:
             type = 'total'
       
        
        
        if type == 'total' and order_direction == 'asc' and keyword is None:     

                sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.is_deleted == 'f')
                    .order_by(asc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
        elif type == 'total' and order_direction == 'asc' and keyword is not None and first_name is not None and last_name is not None:
               
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Member.first_name.like(first_name))
                    .filter(Member.last_name.like(last_name))
                    .filter(Sta_station.is_deleted == 'f')
                    .order_by(asc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               if sql == []:
                    sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.name.like(search))
                    .filter(Sta_station.is_deleted == 'f')
                    .order_by(asc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )

               


        elif type == 'total' and order_direction == 'asc' and keyword is not None:
               
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(or_(Member.first_name.like(search),Member.last_name.like(search),Member.email_verify.like(search),Sta_station.name.like(search),Member.username.like(search)))
                    .filter(Sta_station.is_deleted == 'f')
                    .order_by(asc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               
               
               
        elif type == 'total' and order_direction == 'desc' and keyword is None:
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.is_deleted == 'f')
                    .order_by(desc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               

        elif type == 'total' and order_direction == 'desc' and keyword is not None and first_name is not None and last_name is not None:
               
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Member.first_name.like(first_name))
                    .filter(Member.last_name.like(last_name))
                    .order_by(desc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               if sql == []:
                    sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.name.like(search))
                    .filter(Sta_station.is_deleted == 'f')
                    .order_by(desc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               
               
        elif type == 'total' and order_direction == 'desc' and keyword is not None:

               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(or_(Member.first_name.like(search),Member.last_name.like(search),Member.email_verify.like(search),Sta_station.name.like(search),Member.username.like(search)))
                    .order_by(desc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               
        elif type == 'new' and order_direction == 'asc' and keyword is None:     
                
                sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_approve_statuses.id.is_(None))
                    .filter(Sta_station.is_deleted == 'f')
                    .order_by(asc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
                

        elif type == 'new' and order_direction == 'asc' and keyword is not None and first_name is not None and last_name is not None:
               
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_approve_statuses.id.is_(None))
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Member.first_name.like(first_name))
                    .filter(Member.last_name.like(last_name))
                    .order_by(asc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               if sql == []:
                    sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_approve_statuses.id.is_(None))
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .order_by(asc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )

               
        elif type == 'new' and order_direction == 'asc' and keyword is not None:
              
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_approve_statuses.id.is_(None))
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(or_(Member.first_name.like(search),Member.last_name.like(search),Member.email_verify.like(search),Sta_station.name.like(search),Member.username.like(search)))
                    .order_by(asc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               
        elif type == 'new' and order_direction == 'desc' and keyword is None:
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Sta_approve_statuses.id.is_(None))
                    .order_by(desc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               

        elif type == 'new' and order_direction == 'desc' and keyword is not None and first_name is not None and last_name is not None:
               
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_approve_statuses.id.is_(None))
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Member.first_name.like(first_name))
                    .filter(Member.last_name.like(last_name))
                    .order_by(desc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               if sql == []:
                    sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_approve_statuses.id.is_(None))
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .order_by(desc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               
        elif type == 'new' and order_direction == 'desc' and keyword is not None:
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_approve_statuses.id.is_(None))
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(or_(Member.first_name.like(search),Member.last_name.like(search),Member.email_verify.like(search),Sta_station.name.like(search),Member.username.like(search)))
                    .order_by(desc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               
               

        elif type == 'approve' and order_direction == 'asc' and keyword is None:     

                sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 1)
                    .filter(Sta_station.is_deleted == 'f')
                    .order_by(asc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
                
        elif type == 'approve' and order_direction == 'asc' and keyword is not None and first_name is not None and last_name is not None:
               
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 1)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Member.first_name.like(first_name))
                    .filter(Member.last_name.like(last_name))
                    .order_by(asc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               if sql == []:
                    sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 1)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .order_by(asc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )

               
        elif type == 'approve' and order_direction == 'asc' and keyword is not None:

               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 1)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(or_(Member.first_name.like(search),Member.last_name.like(search),Member.email_verify.like(search),Sta_station.name.like(search),Member.username.like(search)))
                    .order_by(asc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               
        elif type == 'approve' and order_direction == 'desc' and keyword is None:
              sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 1)
                    .filter(Sta_station.is_deleted == 'f')
                    .order_by(desc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
              
        elif type == 'approve' and order_direction == 'desc' and keyword is not None and first_name is not None and last_name is not None:
               
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 1)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Member.first_name.like(first_name))
                    .filter(Member.last_name.like(last_name))
                    .order_by(desc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               

               if sql == []:
                    sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 1)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .order_by(desc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               
        elif type == 'approve' and order_direction == 'desc' and keyword is not None:
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 1)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(or_(Member.first_name.like(search),Member.last_name.like(search),Member.email_verify.like(search),Sta_station.name.like(search),Member.username.like(search)))
                    .order_by(desc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               

        elif type == 'disapproved' and order_direction == 'asc' and keyword is None:     

                sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 2)
                    .filter(Sta_station.is_deleted == 'f')
                    .order_by(asc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
                
        elif type == 'disapproved' and order_direction == 'asc' and keyword is not None and first_name is not None and last_name is not None:
               
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 2)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Member.first_name.like(first_name))
                    .filter(Member.last_name.like(last_name))
                    .order_by(asc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               if sql == []:
                    sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 2)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .order_by(asc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )

               
        elif type == 'disapproved' and order_direction == 'asc' and keyword is not None:
              
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 2)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(or_(Member.first_name.like(search),Member.last_name.like(search),Member.email_verify.like(search),Sta_station.name.like(search),Member.username.like(search)))
                    .order_by(asc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               
        elif type == 'disapproved' and order_direction == 'desc' and keyword is None:
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 2)
                    .filter(Sta_station.is_deleted == 'f')
                    .order_by(desc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               
        elif type == 'disapproved' and order_direction == 'desc' and keyword is not None and first_name is not None and last_name is not None:
               
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 2)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Member.first_name.like(first_name))
                    .filter(Member.last_name.like(last_name))
                    .order_by(desc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               if sql == []:
                    sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 2)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .order_by(desc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               
        elif type == 'disapproved' and order_direction == 'desc' and keyword is not None:
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 2)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(or_(Member.first_name.like(search),Member.last_name.like(search),Member.email_verify.like(search),Sta_station.name.like(search),Member.username.like(search)))
                    .order_by(desc(Sta_station.id))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
        return sql
        



    @staticmethod  
    def count_all_list_regis(db: Session, 
                           Sta_station:Sta_station,
                           Member:Member,
                           Sta_station_member:Sta_station_member,
                           Sta_station_statuses:Sta_station_statuses,
                           Sta_approve_statuses:Sta_approve_statuses,
                           Countries:Countries,
                           keyword:str,
                           type:str):
         
        first_name = None
        last_name = None
        if keyword is not None:
             if ' ' in keyword:
                    names = keyword.split()
                    first_name = names[0]
                    last_name = names[1]
                    first_name = "%{}%".format(first_name)
                    last_name = "%{}%".format(last_name)
                    search = "%{}%".format(keyword)
             else:
                    search = "%{}%".format(keyword)
        if keyword == '':
               keyword = None
        if type is None:
             type = 'total'

       
        
        if type == 'total'  and keyword is None:     
                print("Use->>>>>>this")
                sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.is_deleted == 'f')
                    .count()
                    )
                
        elif type == 'total' and keyword is not None and first_name is not None and last_name is not None:
               
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Member.first_name.like(first_name))
                    .filter(Member.last_name.like(last_name))
                    .count()
                    )
               if sql == 0:
                    sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Member.first_name.like(search))
                    .count()
                    )


        elif type == 'total' and keyword is not None:
               
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(or_(Member.first_name.like(search),Member.last_name.like(search),Member.email_verify.like(search),Sta_station.name.like(search),Member.username.like(search)))
                    .count()
                    )

        elif type == 'new' and keyword is None:     

                sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Sta_approve_statuses.id.is_(None))
                    .count()
                    )
        elif type == 'new' and keyword is not None and first_name is not None and last_name is not None:
               
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_approve_statuses.id.is_(None))
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Member.first_name.like(first_name))
                    .filter(Member.last_name.like(last_name))
                    .count()
                    )
               
               if sql == 0:
                    sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_approve_statuses.id.is_(None))
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .count()
                    )

               
               
        elif type == 'new' and keyword is not None:
               
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_approve_statuses.id.is_(None))
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(or_(Member.first_name.like(search),Member.last_name.like(search),Member.email_verify.like(search),Sta_station.name.like(search),Member.username.like(search)))
                    .count()
                    )

        elif type == 'approve' and keyword is None:     

                sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 1)
                    .filter(Sta_station.is_deleted == 'f')
                    .count()
                    )
        elif type == 'approve' and keyword is not None and first_name is not None and last_name is not None:
               
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 1)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Member.first_name.like(first_name))
                    .filter(Member.last_name.like(last_name))
                    .count()
                    )
               
               if sql == 0:
                    sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 1)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .count()
                    )

               
        elif type == 'approve' and keyword is not None:
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 1)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(or_(Member.first_name.like(search),Member.last_name.like(search),Member.email_verify.like(search),Sta_station.name.like(search),Member.username.like(search)))
                    .count()
                    )

        elif type == 'disapproved' and keyword is None:     

               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 2)
                    .filter(Sta_station.is_deleted == 'f')
                    .count()
                    )
               
        elif type == 'disapproved' and keyword is not None and first_name is not None and last_name is not None:
               
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 2)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Member.first_name.like(first_name))
                    .filter(Member.last_name.like(last_name))
                    .count()
                    )
               if sql == 0:
                    sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 2)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .count()
                    )
               

        elif type == 'disapproved' and keyword is not None:
               sql = (db.query(Sta_station,Member,Sta_station_member,Sta_station_statuses,Sta_approve_statuses,Countries)
                    .outerjoin(Sta_station_member,Sta_station.id == Sta_station_member.station_id)
                    .join (Member, Member.id == Sta_station_member.member_id)
                    .outerjoin(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
                    .outerjoin(Sta_approve_statuses, Sta_station.approve_status_id == Sta_approve_statuses.id)
                    .outerjoin(Countries,Sta_station.country_id == Countries.id)
                    .filter(Sta_station.approve_status_id == 2)
                    .filter(Sta_station.is_deleted == 'f')
                    .filter(or_(Member.first_name.like(search),Member.last_name.like(search),Member.email_verify.like(search),Sta_station.name.like(search),Member.username.like(search)))
                    .count()
                    )
      
        return sql

    @staticmethod  
    def update_station_regis(db: Session, 
                           model:Generic[T],
                           id:int,
                           approve_description:str,
                           approve_status_id:int,
                           user_id:int,
                           update_time:datetime):
         
         if approve_status_id == 2:
               sql = db.query(model).filter(model.id == id).first()
               sql.is_enabled =  False
               sql.is_deleted = False
               sql.station_status_id = None,
               sql.modified_by = user_id,
               sql.approve_description = approve_description,
               sql.approve_status_id = approve_status_id,
               sql.modified = update_time,
               sql.approve_date = update_time
     
         elif approve_status_id == 1:

               sql = db.query(model).filter(model.id == id).first()
               sql.is_enabled =  True
               sql.is_deleted = False
               sql.station_status_id = 1,
               sql.modified_by = user_id,
               sql.approve_description = approve_description,
               sql.approve_status_id = approve_status_id,
               sql.modified = update_time,
               sql.approve_date = update_time

         elif approve_status_id == 5:
               sql = db.query(model).filter(model.id == id).first()
               sql.is_enabled =  False
               sql.station_status_id = 5,
               sql.modified_by = user_id,
               sql.modified = update_time
         
         elif approve_status_id == 6:
               sql = db.query(model).filter(model.id == id).first()
               sql.is_enabled =  True
               sql.station_status_id = 1,
               sql.modified_by = user_id,
               sql.modified = update_time
         
         return sql
    
    
    
    @staticmethod
    def get_all_activity(db: Session, 
                         model:Generic[T],
                         id:int):
         sql = db.query(model).filter(model.id == id).first()

         return sql

    @staticmethod
    def count_data_list_media(db: Session, 
                           model:Generic[T],
                           id:int):
         sql = (db.query(model)
               .filter(model.file_type_media_id == id)
               .filter(model.is_deleted == 'f')
               .filter(model.station_id.is_(None))
               .filter(model.channel_id.is_(None))
               .filter(model.file_status_id == 1)
               .count())
         return sql
    
    @staticmethod
    def get_station_detail(db: Session, 
                           Sta_station:Sta_station,
                           Sta_station_statuses:Sta_station_statuses,
                           Countries:Countries,
                           id:int):
         sql = (db.query(Sta_station,Sta_station_statuses,Countries)
               .join(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
               .join(Countries , Sta_station.country_id == Countries.id)
               .filter(Sta_station.id == id)
               .filter(Sta_station.is_deleted == 'f')
               
                )
         return sql
    
    @staticmethod
    def get_data_station_playlist(db: Session, 
                         model:Generic[T],
                         id:int):
         sql = db.query(model).filter(model.id == id).order_by(desc(model.created)).all()
         return sql
    
    
    @staticmethod
    def get_data_all(db: Session,
                    Sta_station:Sta_station,
                    Sta_station_statuses:Sta_station_statuses,
                    Sta_station_schedule:Sta_station_schedule,
                    Sta_station_period:Sta_station_period,
                    Sta_process_statuses:Sta_process_statuses,
                    Sta_broadcast_statuses:Sta_broadcast_statuses,
                    Sta_period_status:Sta_period_status,
                    Sta_categories:Sta_categories,
                    Sta_broadcast:Sta_broadcast,
                    id:int
                                            ):
         broadcast_a = aliased(Sta_broadcast_statuses)
         sql = (db.query(Sta_station,Sta_station_statuses,Sta_station_schedule,Sta_station_period,Sta_process_statuses,Sta_broadcast_statuses,Sta_period_status,Sta_categories,Sta_broadcast,broadcast_a)
               .join(Sta_station_statuses, Sta_station.station_status_id == Sta_station_statuses.id)
               .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
               .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
               .join(Sta_process_statuses, Sta_station_schedule.process_status_id == Sta_process_statuses.id)
               .outerjoin(Sta_broadcast_statuses, Sta_station_schedule.broadcast_status_id == Sta_broadcast_statuses.id)
               .join(Sta_period_status, Sta_station_period.period_status_id  == Sta_period_status.id)
               .join(Sta_categories,Sta_station_period.period_category_id == Sta_categories.id)
               .outerjoin(Sta_broadcast, Sta_station_period.id == Sta_broadcast.station_period_id)
               .outerjoin(broadcast_a, Sta_broadcast.broadcast_status_id == broadcast_a.id)
               .filter(Sta_station.id == id)
               .filter(Sta_station.approve_status_id == 1)
               .filter(Sta_station_period.is_deleted == 'f')
               .filter(Sta_station_schedule.is_deleted == 'f')
               .order_by(asc(Sta_station_schedule.id),asc(Sta_station_period.id))
               .all()
               )
         return sql
    

    @staticmethod
    def get_data_member_all(db: Session,
                         Sta_station:Sta_station,
                         Sta_station_member:Sta_station_member,
                         Member:Member,
                         id:int):
         sql = (db.query(Sta_station,Sta_station_member,Member)
                .outerjoin(Sta_station_member, Sta_station.id == Sta_station_member.station_id)
                .join(Member, Sta_station_member.member_id == Member.id)
                .filter(Sta_station.id == id)
                .filter(Sta_station.is_deleted == 'f')
                .filter(Member.is_deleted == 'f')
                .filter(Sta_station_member.is_owner == 't')
                .all()
                )
         
         return sql
    
    @staticmethod
    def get_data_station_period(db: Session, 
                         Sta_station_schdule:Sta_station_schedule,
                         Sta_station_period:Sta_station_period,
                         Sta_station_playlist:Sta_station_playlist,
                         id:int):
         sql = (db.query(Sta_station_schdule,Sta_station_period,Sta_station_playlist)
                .join(Sta_station_period , Sta_station_schdule.id == Sta_station_period.station_schedule_id)
                .join(Sta_station_playlist, Sta_station_period.id == Sta_station_playlist.station_period_id)
                .filter(Sta_station_period.is_deleted == 'f')
                .filter(Sta_station_schdule.station_id == id)
                .filter(Sta_station_period.broadcast_status_id.in_([5, 7]))
                .order_by(desc(Sta_station_schdule.schedule_date),desc(Sta_station_period.id))
                .all()
                )
         
         return sql
    
    @staticmethod
    def station_schedule_id(db: Session, 
                         model:Generic[T],
                         id:int):
         sql = db.query(model).filter(model.station_period_id == id).all()
         return sql
    
    @staticmethod
    def check_station_member(db: Session, 
                         model:Generic[T],
                         member_id:int,
                         station_id:int):
         sql = db.query(model).filter(model.member_id == member_id).filter(model.station_id == station_id).all()
         return  sql
    
    @staticmethod
    def check_chanel_member(db: Session, 
                         model:Generic[T],
                         member_id:int,
                         station_id:int):
         sql = db.query(model).filter(model.member_id == member_id).filter(model.channel_id == station_id).all()
         return  sql
    
    @staticmethod
    def get_data_period(db:Session,
                                    id:int,
                                    Sta_station_period:Sta_station_period):
                  sql = (db.query(Sta_station_period).filter(Sta_station_period.station_schedule_id == id)).all()
                  return sql
    

    @staticmethod
    def get_country(db: Session, 
                    model:Generic[T],
                    id:int):
         sql = db.query(model).filter(model.id == id).all()
         return  sql
    
    @staticmethod
    def get_data_station_schedule(db: Session, 
                    model:Generic[T],
                    id:int,
                    date:date):
         sql = (db.query(model)
                .filter(model.station_id == id)
                .filter(cast(model.schedule_date, Date) == date)
                .filter(model.broadcast_status_id == 5)
                .first())
         return  sql
    

    @staticmethod
    def count_customer(db: Session,
                       model:Generic[T]):
         sql = (db.query(model)
                .filter(model.is_deleted == 'f')
                .count()
                )
         return sql
    
    @staticmethod
    def count_station(db: Session,
                       model:Generic[T]):
         sql = (db.query(model)
                .filter(model.approve_status_id == 1)
                .filter(model.is_deleted == 'f')
                .count()
                )
         return sql
    
    @staticmethod
    def count_period(db: Session,
                     model:Generic[T]):
         sql = (db.query(model)
               .filter(model.broadcast_status_id == 3)
               .filter(model.period_status_id.in_([3,4]))
               .filter(model.is_deleted == 'f')
               .count()
          )
         return sql
    
    @staticmethod
    def sum_station_online(db: Session,
                     model:Generic[T]):
         sql = (db.query(model)
                .filter(model.is_deleted == 'f')
                .all()
                )
         return sql
    
    

    @staticmethod
    def summary_station_onair(db: Session,
                         Sta_station:Sta_station,
                         Sta_station_schedule:Sta_station_schedule):
         subquery = (db.query(Sta_station.id) 
               .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id) 
               .filter(Sta_station.is_deleted == 'f') 
               .filter(Sta_station_schedule.broadcast_status_id == 3) 
               .filter(Sta_station_schedule.is_deleted == 'f') 
               .group_by(Sta_station.id)
               .subquery()
               )
        
         sql = db.query(subquery.c.id).count()
         return sql
    

    @staticmethod
    def active_6_1(db: Session,
                         Sta_station:Sta_station,
                         Sta_station_schedule:Sta_station_schedule):
         subquery = (db.query(Sta_station.id) 
               .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id) 
               .filter(Sta_station.is_deleted == 'f') 
               .filter(Sta_station_schedule.broadcast_status_id == 5) 
               .filter(Sta_station_schedule.process_status_id == 3)
               .filter(Sta_station_schedule.is_deleted == 'f') 
               .group_by(Sta_station.id)
               .subquery()
               )
        
         sql = db.query(subquery.c.id).count()
         return sql
    

    @staticmethod
    def active_6_2(db: Session,
                         Sta_station:Sta_station,
                         Sta_station_schedule:Sta_station_schedule):
         subquery = (db.query(Sta_station.id) 
               .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id) 
               .filter(Sta_station.is_deleted == 'f')
               .filter(Sta_station_schedule.process_status_id == 3)
               .filter(Sta_station_schedule.is_deleted == 'f') 
               .group_by(Sta_station.id)
               .subquery()
               )
        
         sql = db.query(subquery.c.id).count()
         return sql
    

    @staticmethod
    def active_7_1(db: Session,
                         Sta_station:Sta_station,
                         Sta_station_schedule:Sta_station_schedule):
         subquery = (db.query(Sta_station_schedule.id) 
               .join(Sta_station, Sta_station_schedule.station_id == Sta_station.id) 
               .filter(Sta_station.is_deleted == 'f')
               .filter(Sta_station_schedule.broadcast_status_id == 5)
               .filter(Sta_station_schedule.process_status_id == 3)
               .filter(Sta_station_schedule.is_deleted == 'f') 
               .group_by(Sta_station_schedule.id)
               .subquery()
               )
     
         sql = db.query(subquery.c.id).count()
         return sql
    

    @staticmethod
    def active_7_2(db: Session,
                         Sta_station:Sta_station,
                         Sta_station_schedule:Sta_station_schedule):
         subquery = (db.query(Sta_station_schedule.id) 
               .join(Sta_station, Sta_station_schedule.station_id == Sta_station.id) 
               .filter(Sta_station.is_deleted == 'f')
               .filter(Sta_station_schedule.process_status_id == 3)
               .filter(Sta_station_schedule.is_deleted == 'f') 
               .group_by(Sta_station_schedule.id)
               .subquery()
               )
        
         sql = db.query(subquery.c.id).count()
         return sql
    

    @staticmethod
    def get_data_period_status_id(db:Session,
                                  Sta_station_period:Sta_station_period):
         
         
         sql= (
                    db.query(
                         Sta_station_period.period_status_id,
                         case(
                              
                                   (Sta_station_period.period_status_id == 2, 'รอออกอากาศ'),
                                   (Sta_station_period.period_status_id == 3, 'ขอให้ปรับแก้'),
                                   (Sta_station_period.period_status_id == 4, 'ส่งผลการแก้ไข'),
                                   (Sta_station_period.period_status_id == 5, 'ปิดงานแก้ไข')
                              ,
                              else_=''
                         ).label('period_status_name'),
                         func.count(Sta_station_period.id)
                    )
                    .filter(Sta_station_period.broadcast_status_id == 3)
                    .filter(Sta_station_period.period_status_id.in_([2, 3, 4, 5]))
                    .filter(Sta_station_period.is_deleted == 'f')
                    .group_by(Sta_station_period.period_status_id, 'period_status_name')
                    .order_by(Sta_station_period.period_status_id.asc())
                    .all()
               )
         return sql
    

    @staticmethod
    def get_data_station_popular(db:Session,
                                 Sta_station:Sta_station):
        sql = (db.query(
            Sta_station.id,
            Sta_station.name,
            Sta_station.object_key,
            Sta_station.approve_status_id,
            (Sta_station.count_like + Sta_station.count_share + Sta_station.count_listen + Sta_station.count_comment).label("TOTAL")
               )
               .filter(Sta_station.approve_status_id == 1)
               .filter(Sta_station.is_deleted == False)
               .order_by(desc("TOTAL").nulls_last())
               
             )
        
        return sql
    
    @staticmethod
    def get_lasted(db:Session,
                   Sta_station:Sta_station,
                   Sta_station_schedule:Sta_station_schedule,
                   Sta_station_period:Sta_station_period,
                   Member:Member):
          broadcast_status_name_case = case(
          
                    (Sta_station_schedule.process_status_id == 3, 'ส่งออกอากาศ')
                    ).label('broadcast_status_name')
          
          sql = (db.query(Sta_station,Sta_station_schedule,Sta_station_period,Member,broadcast_status_name_case)
                 .join(Sta_station_schedule, Sta_station.id == Sta_station_schedule.station_id)
                 .join(Sta_station_period, Sta_station_schedule.id == Sta_station_period.station_schedule_id)
                 .join(Member, Sta_station.created_by == Member.id)
                 .filter(Sta_station_period.broadcast_status_id == 3)
                 .filter(Sta_station_schedule.process_status_id == 3)
                 .order_by(desc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.schedule_date))
                 .all()
                 )
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
    def check_station_schedule(db:Session,
                                Sta_station_schedule:Sta_station_schedule,
                                id:int,
                                user_id:int,
                                time_update:datetime):
     
                 sql = db.query(Sta_station_schedule).filter(Sta_station_schedule.id == id).first()
                 sql.broadcast_status_id = 4
                 sql.broadcast_status_date = time_update
                 sql.modified_by = user_id
                 sql.modified = time_update

                 return sql

    @staticmethod
    def check_station_schedule_ban(db:Session,
                                Sta_station_schedule:Sta_station_schedule,
                                id:int,
                                user_id:int,
                                time_update:datetime):
     
                 sql = db.query(Sta_station_schedule).filter(Sta_station_schedule.id == id).first()
                 sql.broadcast_status_id = 6
                 sql.broadcast_status_date = time_update
                 sql.modified_by = user_id
                 sql.modified = time_update

                 return sql

              
    @staticmethod
    def  check_period(db:Session,
                                Sta_station_period:Sta_station_period,
                                id:int,
                                user_id:int,
                                time_update:datetime):
                 sql = db.query(Sta_station_period).filter(Sta_station_period.id == id).first()
                 sql.broadcast_status_id = 6
                 sql.broadcast_status_date = time_update
                 sql.modified_by = user_id
                 sql.modified = time_update

                 return sql
    
    @staticmethod
    def  check_period_4(db:Session,
                                Sta_station_period:Sta_station_period,
                                id:int,
                                user_id:int,
                                time_update:datetime):
                 sql = db.query(Sta_station_period).filter(Sta_station_period.id == id).first()
                 sql.broadcast_status_id = 4
                 sql.broadcast_status_date = time_update
                 sql.modified_by = user_id
                 sql.modified = time_update

                 return sql
    

    @staticmethod
    def find_schedule(db:Session,
                      model:Generic[T],
                      id:int):
         sql = db.query(model).filter(model.station_id == id).all()
         return sql
    

    @staticmethod
    def find_period(db:Session,
                      model:Generic[T],
                      id:int):
         sql = db.query(model).filter(model.station_schedule_id == id).all()
         return sql
    

    @staticmethod
    def check_time_on_air(db:Session,
                      model:Generic[T],
                      id:int,
                      time:Time,
                      date:Date):
          sql = (db.query(model)
                 .filter(model.station_id == id)
                 .filter(model.schedule_time_start <= time , model.schedule_time_end >= time)
                 .filter(cast(model.schedule_date, Date) == date)
                 .all()
                 )
          if sql:
               return True
          else:
               return False
          



    


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


class UsersRepo(BaseRepo):
    @staticmethod
    def find_by_username(db: Session, model: Generic[T], username: str):
        return db.query(model).filter(model.username == username).first()


class JWTRepo:
    def generate_token(data: dict, expires_delta: Optional[timedelta] = None):
        """
        to_encode = {
            "id": user_id,
            "sub": user_name,
            "exp": expire
        }
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days = 365*2)

        to_encode.update({"exp": expire})

        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encode_jwt

    def decode_token(token: str):
        try:
            decode_token = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
            return decode_token if decode_token["expires"] >= datetime.time() else None
        except:
            return {}


class JWTBearer(HTTPBearer):
    
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        
        if credentials: #ถ้ามี token
            
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=401, detail="Invalid authentication sheme."
                )
            
            if credentials.credentials is not None : #check ว่าถ้ามี token
                
                check_payload = self.verfity_jwt(credentials.credentials)
                if check_payload is False:
                   
                    raise HTTPException(
                        status_code=401, detail="Invalid token or Token is Expire"
                    )
                else:
                    return credentials.credentials
            
            else:
                HTTPException(
                        status_code=401, detail="Not Found Token"
                    )


                  
                
        else: #ถ้าไม่มีค่า
            raise HTTPException(status=401, detail="Invalid authorization code.")
    
        
    def verfity_jwt(Self, jwttoken: str): #check jwt ว่ามีข้อมูลหรือไม่
        isTokenValid: bool = False
        
        try:
            payload = jwt.decode(jwttoken, SECRET_KEY, algorithms=[ALGORITHM])
        except:
            payload = None
        
        
        if payload:
            isTokenValid = True
        
        return isTokenValid
    
    def refresh_jwt(jwttoken: str):
        try:
            payload = jwt.decode(jwttoken, SECRET_KEY, algorithms=[ALGORITHM])
            
            time_add = datetime.utcnow() + timedelta(days = 365*2)
            expire = int(time_add.timestamp())
            payload.update({"exp": expire})
            
            
            access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
            
            
        except:
            payload = None

        return access_token , jwttoken
    