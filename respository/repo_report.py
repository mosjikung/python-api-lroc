from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, null,or_ ,func , cast ,Date ,asc ,select ,extract


from datetime import datetime, timedelta ,date
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM


from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from model import (Users,
                   Stat_customer_detail,
                   Stat_customer_action_detail
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
    def get_all_data_report_1(db: Session, 
                              model: Generic[T] ,
                              id:int):
        
        current_date = datetime.now()
        previous_date = current_date - timedelta(days=1)
        subquery = (db.query(model.station_id,
                             model.schedule_id,
                             model.period_id,
                             model.customer_id,
                             model.action_type_id,
                             func.count(model.id).label('TOTAL'))
                             .filter(model.action_type_id.isnot(None))
                             .filter(model.station_id == id)
                             .filter(cast(model.action_date,Date) > previous_date,cast(model.action_date,Date) <= current_date)
                             .filter(model.is_active.is_(True))
                             .group_by(model.station_id , model.schedule_id , model.period_id , model.customer_id , model.action_type_id)
                             )
        main_query = db.query(func.sum(subquery.subquery().columns.TOTAL)).scalar()
        if main_query is not None:
            main_query = int(main_query)
        else:
            main_query = 0
        return main_query
    
    @staticmethod
    def get_all_data_report_2(db: Session, 
                              model: Generic[T] ,
                              id:int):
        current_date = datetime.now()
        previous_date = current_date - timedelta(days=7)
        subquery = (db.query(model.station_id,
                             model.schedule_id,
                             model.period_id,
                             model.customer_id,
                             model.action_type_id,
                             func.count(model.id).label('TOTAL'))
                             .filter(model.action_type_id.isnot(None))
                             .filter(model.station_id == id)
                             .filter(cast(model.action_date,Date) > previous_date,cast(model.action_date,Date) <= current_date)
                             .filter(model.is_active.is_(True))
                             .group_by(model.station_id , model.schedule_id , model.period_id , model.customer_id , model.action_type_id)
                             )
        main_query = db.query(func.sum(subquery.subquery().columns.TOTAL)).scalar()
        if main_query is not None:
            main_query = int(main_query)
        else:
            main_query = 0
        return main_query
    

    @staticmethod
    def get_all_data_report_3(db: Session, 
                              model: Generic[T] ,
                              id:int):
        current_date = datetime.now()
        previous_date = current_date - timedelta(days=30)
        subquery = (db.query(model.station_id,
                             model.schedule_id,
                             model.period_id,
                             model.customer_id,
                             model.action_type_id,
                             func.count(model.id).label('TOTAL'))
                             .filter(model.action_type_id.isnot(None))
                             .filter(model.station_id == id)
                             .filter(cast(model.action_date,Date) > previous_date,cast(model.action_date,Date) <= current_date)
                             .filter(model.is_active.is_(True))
                             .group_by(model.station_id , model.schedule_id , model.period_id , model.customer_id , model.action_type_id)
                             )
        main_query = db.query(func.sum(subquery.subquery().columns.TOTAL)).scalar()
        if main_query is not None:
            main_query = int(main_query)
        else:
            main_query = 0
        return main_query
    
    @staticmethod
    def get_all_data_report_4(db: Session, 
                              model: Generic[T] ,
                              id:int):
        current_date = datetime.now()
        subquery = (db.query(model.station_id,
                             model.schedule_id,
                             model.period_id,
                             model.customer_id,
                             model.action_type_id,
                             func.count(model.id).label('TOTAL'))
                             .filter(model.action_type_id.isnot(None))
                             .filter(model.station_id == id)
                             .filter(extract('month', cast(model.action_date, Date)) == current_date.month - 1)
                             .filter(model.is_active.is_(True))
                             .group_by(model.station_id , model.schedule_id , model.period_id , model.customer_id , model.action_type_id)
                             )
        main_query = db.query(func.sum(subquery.subquery().columns.TOTAL)).scalar()
        if main_query is not None:
            main_query = int(main_query)
        else:
            main_query = 0
        return main_query
    


    
    @staticmethod
    def get_all_data_report(db: Session, 
                            model: Generic[T] ,
                            date_start:str,
                            date_end:str,
                            type:str,
                            id:int):
        date_str_convert = datetime.strptime(date_start, "%Y-%m-%d")
        date_end_convert = datetime.strptime(date_end, "%Y-%m-%d")
        if type == 'day':
            
            subquery = (db.query(model.station_id,
                                model.schedule_id,
                                model.period_id,
                                model.customer_id,
                                model.action_type_id,
                                func.date(model.action_date).label('action_date'),
                                func.count(model.id).label('TOTAL'))
                                .filter(model.action_type_id.isnot(None))
                                .filter(model.station_id == id)
                                .filter(cast(model.action_date,Date) >= date_str_convert,cast(model.action_date,Date) <= date_end_convert)
                                .filter(model.is_active.is_(True))
                                .group_by(model.station_id , model.schedule_id , model.period_id , model.customer_id , model.action_type_id ,func.date(model.action_date))
                                ).subquery('report')
            main_query = db.query(subquery.c.action_date,func.sum(subquery.c.TOTAL)).group_by(subquery.c.action_date).order_by(subquery.c.action_date)
            
            return main_query
        
        elif type == 'month':
            subquery = (db.query(model.station_id,
                                model.schedule_id,
                                model.period_id,
                                model.customer_id,
                                model.action_type_id,
                                func.date(model.action_date).label('action_date'),
                                func.count(model.id).label('TOTAL'))
                                .filter(model.action_type_id.isnot(None))
                                .filter(model.station_id == id)
                                .filter(cast(model.action_date,Date) >= date_str_convert,cast(model.action_date,Date) <= date_end_convert)
                                .filter(model.is_active.is_(True))
                                .group_by(model.station_id , model.schedule_id , model.period_id , model.customer_id , model.action_type_id,model.action_date)
                                ).subquery('report')
            main_query = db.query(func.date_part('month', subquery.c.action_date).label('month'),func.date_part('year', subquery.c.action_date).label('year'),func.sum(subquery.c.TOTAL)).group_by(func.date_part('month', subquery.c.action_date),func.date_part('year', subquery.c.action_date)).order_by(func.date_part('year', subquery.c.action_date),func.date_part('month', subquery.c.action_date))
            return main_query
            




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

