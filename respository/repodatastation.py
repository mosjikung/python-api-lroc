from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, null,or_ ,func , cast ,Date ,asc


from datetime import datetime, timedelta ,date
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM


from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from model import (Users
                   )

import pdb


T = TypeVar("T")


class BaseRepo:
    """
    CRUD
    C = Create
    R = Read
    U = update
    D = Delete
    """

    @staticmethod
    def get_all_schedule_catagories(db: Session, 
                                    model: Generic[T] , 
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
        if order_direction == 'asc' and keyword is None:
              print("1")
              sql = (db.query(model)
              .filter(model.is_deleted == 'f')
              .order_by(asc(model.created))
              .offset(offset)
              .limit(limit)
              .all())
        elif order_direction == 'asc' and keyword is not None:
              print("2")
              sql = (db.query(model)
              .filter(model.is_deleted == 'f')
              .filter(or_(model.name.like(search),model.description.like(search)))
              .order_by(asc(model.created))
              .offset(offset)
              .limit(limit)
              .all())
        elif order_direction == 'desc' and keyword is None:
              print("3")
              sql = (db.query(model)
              .filter(model.is_deleted == 'f')
              .order_by(desc(model.created))
              .offset(offset)
              .limit(limit)
              .all())
        elif order_direction == 'desc' and keyword is not None:
              print("4")
              sql = (db.query(model)
              .filter(model.is_deleted == 'f')
              .filter(or_(model.name.like(search),model.description.like(search)))
              .order_by(desc(model.created))
              .offset(offset)
              .limit(limit)
              .all())
        return sql
    


    @staticmethod
    def get_all_schedule_catagories_count(db: Session, 
                                    model: Generic[T] , 
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

        if order_direction == 'asc' and keyword is None:
              print("1")
              sql = (db.query(model)
              .filter(model.is_deleted == 'f')
              .count())
        elif order_direction == 'asc' and keyword is not None:
              print("2")
              sql = (db.query(model)
              .filter(model.is_deleted == 'f')
              .filter(or_(model.name.like(search),model.description.like(search)))
              .count()
              )
        elif order_direction == 'desc' and keyword is None:
              print("3")
              sql = (db.query(model)
              .filter(model.is_deleted == 'f')
              .count())
        elif order_direction == 'desc' and keyword is not None:
              print("4")
              sql = (db.query(model)
              .filter(model.is_deleted == 'f')
              .filter(or_(model.name.like(search),model.description.like(search)))
              .count())
        return sql
    
    @staticmethod
    def get_all_station_period_count(db: Session, model: Generic[T], id:int):
         sql = (db.query(model)
                .filter(model.is_deleted == 'f')
                .filter(model.period_category_id == id)
                .count()
                )
         return sql
    

    @staticmethod
    def update_station_schedule_type(db: Session, model: Generic[T], id:int ,modified:int,modified_by:int, name:str,description:str):
        sql = db.query(model).filter(model.id == id).first()
        sql.modified = modified,
        sql.modified_by = modified_by,
        sql.name = name,
        sql.description = description
        
        return sql
    

    def delete_station_schedule_type(db: Session, 
                                     model:Generic[T] , 
                                     id:int,
                                     user_id:int,
                                     update_time:datetime):
         sql = db.query(model).filter(model.id == id).first()
         sql.is_deleted = True
         sql.modified = update_time,
         sql.modified_by = user_id,

         return sql
    

    
    

    

    


    

    @staticmethod
    def insert(db: Session, model: Generic[T]):
        db.add(model)
        db.commit()
        db.refresh(model)
     


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

