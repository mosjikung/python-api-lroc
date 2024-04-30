from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, null,or_ ,func , cast ,Date ,asc ,case , and_


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
                   Sta_station_schedule_activitie,
                   Sta_broadcast,
                   Sta_broadcast_history_status,
                   Sta_station_activities,
                   Sta_station_period
                   )

import pdb




T = TypeVar("T")



class BaseRepo:
 
 @staticmethod
 def count_type_1(db: Session,
                         Sta_station:Sta_station,
                         Sta_station_schedule:Sta_station_schedule,
                         Member:Member):
     
    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(or_(Sta_station_schedule.broadcast_status_id == 3,Sta_station_schedule.broadcast_status_id == 4, Sta_station_schedule.broadcast_status_id == 5 ,Sta_station_schedule.broadcast_status_id == 6 ,  Sta_station_schedule.broadcast_status_id == 7))
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .count()
               )
    return results
 
 @staticmethod
 def count_type_2(db: Session,
                        Sta_station:Sta_station,
                         Sta_station_schedule:Sta_station_schedule,
                         Member:Member):
     
    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 5)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .count()
               )
    return results
 

 @staticmethod
 def count_type_3(db: Session,
                        Sta_station:Sta_station,
                         Sta_station_schedule:Sta_station_schedule,
                         Member:Member):
     
    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 3)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .count()
               )
    return results
 
 @staticmethod
 def count_type_4(db: Session,
                        Sta_station:Sta_station,
                         Sta_station_schedule:Sta_station_schedule,
                         Member:Member):
     
    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 7)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .count()
               )
    return results



 def find_all_station_schedule(db: Session,
                         Sta_station:Sta_station,
                         Sta_station_schedule:Sta_station_schedule,
                         Member:Member,
                         offset:int,
                         limit:int,
                         type:str,
                         order_direction:str,
                         keyword:str):
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
                
               
               if  type == 'total' and order_direction == 'asc'  and keyword is None:
                 
                    
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(or_(Sta_station_schedule.broadcast_status_id == 3, Sta_station_schedule.broadcast_status_id == 5 , Sta_station_schedule.broadcast_status_id == 7))
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                    
               elif type == "total"  and order_direction == 'asc' and  keyword is not None and first_name is not None and last_name is not None:
                   
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(or_(Sta_station_schedule.broadcast_status_id == 3, Sta_station_schedule.broadcast_status_id == 5 , Sta_station_schedule.broadcast_status_id == 7))
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(and_(Member.first_name.like(first_name),Member.last_name.like(last_name)))
                   .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                   
                   if results == []:
                      results = (db.query(Sta_station,Sta_station_schedule,Member)
                    .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                    .join(Member , Sta_station.created_by == Member.id)
                    .filter(or_(Sta_station_schedule.broadcast_status_id == 3, Sta_station_schedule.broadcast_status_id == 5 , Sta_station_schedule.broadcast_status_id == 7))
                    .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                    .filter(Sta_station_schedule.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
                       
               elif  type == 'total' and order_direction == 'asc'  and keyword is not None:
                    
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(or_(Sta_station_schedule.broadcast_status_id == 3, Sta_station_schedule.broadcast_status_id == 5 , Sta_station_schedule.broadcast_status_id == 7))
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search),Member.username.like(search),Member.first_name.like(search),Member.last_name.like(search),Sta_station.name.like(search)))
                   .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                    
               elif  type == 'total' and order_direction == 'desc'  and keyword is None:
                  
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(or_(Sta_station_schedule.broadcast_status_id == 3, Sta_station_schedule.broadcast_status_id == 5 , Sta_station_schedule.broadcast_status_id == 7))
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .order_by(desc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                    
               elif type == "total"  and order_direction == 'desc' and  keyword is not None and first_name is not None and last_name is not None:
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(or_(Sta_station_schedule.broadcast_status_id == 3, Sta_station_schedule.broadcast_status_id == 5 , Sta_station_schedule.broadcast_status_id == 7))
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(and_(Member.first_name.like(first_name),Member.last_name.like(last_name)))
                   .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                   
                   if results == []:
                      results = (db.query(Sta_station,Sta_station_schedule,Member)
                    .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                    .join(Member , Sta_station.created_by == Member.id)
                    .filter(or_(Sta_station_schedule.broadcast_status_id == 3, Sta_station_schedule.broadcast_status_id == 5 , Sta_station_schedule.broadcast_status_id == 7))
                    .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                    .filter(Sta_station_schedule.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
                    
               elif  type == 'total' and order_direction == 'desc'  and keyword is not None:
                   
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(or_(Sta_station_schedule.broadcast_status_id == 3, Sta_station_schedule.broadcast_status_id == 5 , Sta_station_schedule.broadcast_status_id == 7))
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search),Member.username.like(search),Member.first_name.like(search),Member.last_name.like(search),Sta_station.name.like(search)))
                   .order_by(desc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                  
               

               elif type == 'onair' and order_direction == 'asc'  and keyword is None:
                    print("5")
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 5)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                    
               elif type == "onair"  and order_direction == 'asc' and  keyword is not None and first_name is not None and last_name is not None:
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 5)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(and_(Member.first_name.like(first_name),Member.last_name.like(last_name)))
                   .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                   
                   if results == []:
                      results = (db.query(Sta_station,Sta_station_schedule,Member)
                    .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                    .join(Member , Sta_station.created_by == Member.id)
                    .filter(Sta_station_schedule.broadcast_status_id == 5)
                    .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                    .filter(Sta_station_schedule.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
                      
               elif type == 'onair' and order_direction == 'asc'  and keyword is not None:
                   print("6")
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 5)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search),Member.username.like(search),Member.first_name.like(search),Member.last_name.like(search),Sta_station.name.like(search)))
                   .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )

               elif type == 'onair' and order_direction == 'desc'  and keyword is None:
                    print("7")
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 5)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .order_by(desc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                    

               elif type == "onair"  and order_direction == 'desc' and  keyword is not None and first_name is not None and last_name is not None:
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 5)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(and_(Member.first_name.like(first_name),Member.last_name.like(last_name)))
                   .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                   
                   if results == []:
                      results = (db.query(Sta_station,Sta_station_schedule,Member)
                    .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                    .join(Member , Sta_station.created_by == Member.id)
                    .filter(Sta_station_schedule.broadcast_status_id == 5)
                    .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                    .filter(Sta_station_schedule.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
                      
               elif  type == 'onair' and order_direction == 'desc'  and keyword is not None:
                   print("8")
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 5)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search),Member.username.like(search),Member.first_name.like(search),Member.last_name.like(search),Sta_station.name.like(search)))
                   .order_by(desc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .limit(limit)
                   .all()
                   )

               elif type == 'waiting' and order_direction == 'asc'  and keyword is None:
                    print("9")
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 3)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .order_by(desc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                    
               elif type == "waiting"  and order_direction == 'asc' and  keyword is not None and first_name is not None and last_name is not None:
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 3)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(and_(Member.first_name.like(first_name),Member.last_name.like(last_name)))
                   .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                   
                   if results == []:
                      results = (db.query(Sta_station,Sta_station_schedule,Member)
                    .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                    .join(Member , Sta_station.created_by == Member.id)
                    .filter(Sta_station_schedule.broadcast_status_id == 3)
                    .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                    .filter(Sta_station_schedule.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
                      
               elif type == 'waiting' and order_direction == 'asc'  and keyword is not None:
                   print("10")
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 3)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search),Member.username.like(search),Member.first_name.like(search),Member.last_name.like(search),Sta_station.name.like(search)))
                   .order_by(desc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )

               elif type == 'waiting' and order_direction == 'desc'  and keyword is None:
                    print("11")
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 3)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .order_by(desc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                    
               elif type == "waiting"  and order_direction == 'desc' and  keyword is not None and first_name is not None and last_name is not None:
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 3)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(and_(Member.first_name.like(first_name),Member.last_name.like(last_name)))
                   .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                   
                   if results == []:
                      results = (db.query(Sta_station,Sta_station_schedule,Member)
                    .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                    .join(Member , Sta_station.created_by == Member.id)
                    .filter(Sta_station_schedule.broadcast_status_id == 3)
                    .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                    .filter(Sta_station_schedule.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
                      
               elif  type == 'waiting' and order_direction == 'desc'  and keyword is not None:
                   print("12")
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 3)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search),Member.username.like(search),Member.first_name.like(search),Member.last_name.like(search),Sta_station.name.like(search)))
                   .order_by(desc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )

               elif type == 'history' and order_direction == 'asc'  and keyword is None:
                    print("13")
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 7)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .order_by(desc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                    
               elif type == "history"  and order_direction == 'asc' and  keyword is not None and first_name is not None and last_name is not None:
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 7)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(and_(Member.first_name.like(first_name),Member.last_name.like(last_name)))
                   .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                   
                   if results == []:
                      results = (db.query(Sta_station,Sta_station_schedule,Member)
                    .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                    .join(Member , Sta_station.created_by == Member.id)
                    .filter(Sta_station_schedule.broadcast_status_id == 7)
                    .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                    .filter(Sta_station_schedule.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
               elif type == 'history' and order_direction == 'asc'  and keyword is not None:
                   print("14")
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 7)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search),Member.username.like(search),Member.first_name.like(search),Member.last_name.like(search),Sta_station.name.like(search)))
                   .order_by(desc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )

               elif type == 'history' and order_direction == 'desc'  and keyword is None:
                    print("15")
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 7)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .order_by(desc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
               elif type == "history"  and order_direction == 'desc' and  keyword is not None and first_name is not None and last_name is not None:
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 7)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(and_(Member.first_name.like(first_name),Member.last_name.like(last_name)))
                   .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                   
                   if results == []:
                      results = (db.query(Sta_station,Sta_station_schedule,Member)
                    .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                    .join(Member , Sta_station.created_by == Member.id)
                    .filter(Sta_station_schedule.broadcast_status_id == 7)
                    .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                    .filter(Sta_station_schedule.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .order_by(asc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                    .offset(offset)
                    .limit(limit)
                    .all()
                    )
                      
               elif  type == 'history' and order_direction == 'desc'  and keyword is not None:
                   print("16")
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 7)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search),Member.username.like(search),Member.first_name.like(search),Member.last_name.like(search),Sta_station.name.like(search)))
                   .order_by(desc(Sta_station_schedule.schedule_date),asc(Sta_station_schedule.broadcast_status_id),desc(Sta_station_schedule.schedule_number))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                

               return results


 def count_all_station_schedule(db: Session,
                         Sta_station:Sta_station,
                         Sta_station_schedule:Sta_station_schedule,
                         Member:Member,
                         offset:int,
                         limit:int,
                         type:str,
                         order_direction:str,
                         keyword:str):
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
                
             
               if  type == 'total' and order_direction == 'asc'  and keyword is None:
                 
                    
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(or_(Sta_station_schedule.broadcast_status_id == 3,Sta_station_schedule.broadcast_status_id == 4, Sta_station_schedule.broadcast_status_id == 5 ,Sta_station_schedule.broadcast_status_id == 6 ,  Sta_station_schedule.broadcast_status_id == 7))
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .count()
                   )
                    
               elif type == "total"  and order_direction == 'asc' and  keyword is not None and first_name is not None and last_name is not None:
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(or_(Sta_station_schedule.broadcast_status_id == 3, Sta_station_schedule.broadcast_status_id == 5 , Sta_station_schedule.broadcast_status_id == 7))
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(and_(Member.first_name.like(first_name),Member.last_name.like(last_name)))
                   .count()
                   )
                   
                   if results == 0:
                      results = (db.query(Sta_station,Sta_station_schedule,Member)
                    .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                    .join(Member , Sta_station.created_by == Member.id)
                    .filter(or_(Sta_station_schedule.broadcast_status_id == 3, Sta_station_schedule.broadcast_status_id == 5 , Sta_station_schedule.broadcast_status_id == 7))
                    .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                    .filter(Sta_station_schedule.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .count()
                    )
                      
               elif  type == 'total' and order_direction == 'asc'  and keyword is not None:
                   
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(or_(Sta_station_schedule.broadcast_status_id == 3,Sta_station_schedule.broadcast_status_id == 4, Sta_station_schedule.broadcast_status_id == 5 ,Sta_station_schedule.broadcast_status_id == 6 ,  Sta_station_schedule.broadcast_status_id == 7))
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search),Member.username.like(search),Member.first_name.like(search),Member.last_name.like(search),Sta_station.name.like(search)))
                   .count()
                   )
            
               elif  type == 'total' and order_direction == 'desc'  and keyword is None:
                  
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(or_(Sta_station_schedule.broadcast_status_id == 3,Sta_station_schedule.broadcast_status_id == 4, Sta_station_schedule.broadcast_status_id == 5 ,Sta_station_schedule.broadcast_status_id == 6 ,  Sta_station_schedule.broadcast_status_id == 7))
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .count()
                   )
                    
               elif type == "total"  and order_direction == 'desc' and  keyword is not None and first_name is not None and last_name is not None:
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(or_(Sta_station_schedule.broadcast_status_id == 3, Sta_station_schedule.broadcast_status_id == 5 , Sta_station_schedule.broadcast_status_id == 7))
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(and_(Member.first_name.like(first_name),Member.last_name.like(last_name)))
                   .count()
                   )
                   
                   if results == 0:
                      results = (db.query(Sta_station,Sta_station_schedule,Member)
                    .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                    .join(Member , Sta_station.created_by == Member.id)
                    .filter(or_(Sta_station_schedule.broadcast_status_id == 3, Sta_station_schedule.broadcast_status_id == 5 , Sta_station_schedule.broadcast_status_id == 7))
                    .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                    .filter(Sta_station_schedule.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .count()
                    )
                    
               elif  type == 'total' and order_direction == 'desc'  and keyword is not None:
                   
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(or_(Sta_station_schedule.broadcast_status_id == 3,Sta_station_schedule.broadcast_status_id == 4, Sta_station_schedule.broadcast_status_id == 5 ,Sta_station_schedule.broadcast_status_id == 6 ,  Sta_station_schedule.broadcast_status_id == 7))
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search),Member.username.like(search),Member.first_name.like(search),Member.last_name.like(search),Sta_station.name.like(search)))
                   .count()
                   )
                  
               

               elif type == 'onair' and order_direction == 'asc'  and keyword is None:
                    print("5")
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 5)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .count()
                   )
                    
               elif type == "onair"  and order_direction == 'asc' and  keyword is not None and first_name is not None and last_name is not None:
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 5)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(and_(Member.first_name.like(first_name),Member.last_name.like(last_name)))
                   .count()
                   )
                   
                   if results == 0:
                      results = (db.query(Sta_station,Sta_station_schedule,Member)
                    .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                    .join(Member , Sta_station.created_by == Member.id)
                    .filter(Sta_station_schedule.broadcast_status_id == 5)
                    .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                    .filter(Sta_station_schedule.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .count()
                    )
                      
               elif type == 'onair' and order_direction == 'asc'  and keyword is not None:
                   print("6")
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 5)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search),Member.username.like(search),Member.first_name.like(search),Member.last_name.like(search),Sta_station.name.like(search)))
                   .count()
                   )

               elif type == 'onair' and order_direction == 'desc'  and keyword is None:
                    print("7")
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 5)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .count()
                   )
                    
               elif type == "onair"  and order_direction == 'desc' and  keyword is not None and first_name is not None and last_name is not None:
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 5)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(and_(Member.first_name.like(first_name),Member.last_name.like(last_name)))
                   .count()
                   )
                   
                   if results == 0:
                      results = (db.query(Sta_station,Sta_station_schedule,Member)
                    .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                    .join(Member , Sta_station.created_by == Member.id)
                    .filter(Sta_station_schedule.broadcast_status_id == 5)
                    .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                    .filter(Sta_station_schedule.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .count()
                    )
                      
               elif  type == 'onair' and order_direction == 'desc'  and keyword is not None:
                   print("8")
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 5)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search),Member.username.like(search),Member.first_name.like(search),Member.last_name.like(search),Sta_station.name.like(search)))
                   .count()
                   )

               elif type == 'waiting' and order_direction == 'asc'  and keyword is None:
                    print("9")
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 3)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .count()
                   )
                    
               elif type == "waiting"  and order_direction == 'asc' and  keyword is not None and first_name is not None and last_name is not None:
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 3)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(and_(Member.first_name.like(first_name),Member.last_name.like(last_name)))
                   .count()
                   )
                   
                   if results == 0:
                      results = (db.query(Sta_station,Sta_station_schedule,Member)
                    .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                    .join(Member , Sta_station.created_by == Member.id)
                    .filter(Sta_station_schedule.broadcast_status_id == 3)
                    .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                    .filter(Sta_station_schedule.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .count()
                    )
                      
               elif type == 'waiting' and order_direction == 'asc'  and keyword is not None:
                   print("10")
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 3)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search),Member.username.like(search),Member.first_name.like(search),Member.last_name.like(search),Sta_station.name.like(search)))
                   .count()
                   )

               elif type == 'waiting' and order_direction == 'desc'  and keyword is None:
                    print("11")
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 3)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .count()
                   )
                    
               elif type == "waiting"  and order_direction == 'desc' and  keyword is not None and first_name is not None and last_name is not None:
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 3)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(and_(Member.first_name.like(first_name),Member.last_name.like(last_name)))
                   .count()
                   )
                   
                   if results == 0:
                      results = (db.query(Sta_station,Sta_station_schedule,Member)
                    .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                    .join(Member , Sta_station.created_by == Member.id)
                    .filter(Sta_station_schedule.broadcast_status_id == 3)
                    .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                    .filter(Sta_station_schedule.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .count()
                    )
                      
               elif  type == 'waiting' and order_direction == 'desc'  and keyword is not None:
                   print("12")
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 3)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search),Member.username.like(search),Member.first_name.like(search),Member.last_name.like(search),Sta_station.name.like(search)))
                   .count()
                   )

               elif type == 'history' and order_direction == 'asc'  and keyword is None:
                    print("13")
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 7)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .count()
                   )
                    
               elif type == "history"  and order_direction == 'asc' and  keyword is not None and first_name is not None and last_name is not None:
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 7)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(and_(Member.first_name.like(first_name),Member.last_name.like(last_name)))
                   .count()
                   )
                   
                   if results == 0:
                      results = (db.query(Sta_station,Sta_station_schedule,Member)
                    .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                    .join(Member , Sta_station.created_by == Member.id)
                    .filter(Sta_station_schedule.broadcast_status_id == 7)
                    .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                    .filter(Sta_station_schedule.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .count()
                    )
                      
               elif type == 'history' and order_direction == 'asc'  and keyword is not None:
                   print("14")
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 7)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search),Member.username.like(search),Member.first_name.like(search),Member.last_name.like(search),Sta_station.name.like(search)))
                   .count()
                   )

               elif type == 'history' and order_direction == 'desc'  and keyword is None:
                    print("15")
                    results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 7)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .count()
                   )
               
               elif type == "history"  and order_direction == 'desc' and  keyword is not None and first_name is not None and last_name is not None:
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 7)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(and_(Member.first_name.like(first_name),Member.last_name.like(last_name)))
                   .count()
                   )
                   
                   if results == 0:
                      results = (db.query(Sta_station,Sta_station_schedule,Member)
                    .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                    .join(Member , Sta_station.created_by == Member.id)
                    .filter(Sta_station_schedule.broadcast_status_id == 7)
                    .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                    .filter(Sta_station_schedule.is_deleted == 'f')
                    .filter(Sta_station.name.like(search))
                    .count()
                    )
                      
               elif  type == 'history' and order_direction == 'desc'  and keyword is not None:
                   print("16")
                   results = (db.query(Sta_station,Sta_station_schedule,Member)
                   .join(Sta_station_schedule , Sta_station.id == Sta_station_schedule.station_id)
                   .join(Member , Sta_station.created_by == Member.id)
                   .filter(Sta_station_schedule.broadcast_status_id == 7)
                   .filter(Sta_station_schedule.broadcast_status_id.isnot(None))
                   .filter(Sta_station_schedule.is_deleted == 'f')
                   .filter(or_(Sta_station_schedule.schedule_number.like(search),Sta_station_schedule.name.like(search),Member.username.like(search),Member.first_name.like(search),Member.last_name.like(search),Sta_station.name.like(search)))
                   .count()
                   )
               return results
 


 def get_schedule_activity(db:Session,
                           Sta_station_schedule_activitie:Sta_station_schedule_activitie,
                           Member:Member,
                           Users:Users,
                           id:int,
                           object:str,
                           ):
      
    first_name_case =   case(
                            (Sta_station_schedule_activitie.type_user == 'members', Member.first_name),
                            (Sta_station_schedule_activitie.type_user == 'users', Users.first_name)
                                
                            ).label('firstName')
    last_name_case =    case(
                        
                            (Sta_station_schedule_activitie.type_user == 'members', Member.last_name),
                            (Sta_station_schedule_activitie.type_user == 'users', Users.last_name)
                        
                             ).label('lastName')
    sql = (db.query(Sta_station_schedule_activitie.id,
                   Sta_station_schedule_activitie.created,
                   first_name_case,
                   last_name_case,
                   Sta_station_schedule_activitie.name,
                   Sta_station_schedule_activitie.description,
                   Sta_station_schedule_activitie.created_by,
                   Sta_station_schedule_activitie.type_user,
                   Sta_station_schedule_activitie.status_id,
                   Member.object_key,
                   Users.object_key,
                   Sta_station_schedule_activitie.type_user
                   )
                   .outerjoin(Member, and_(Sta_station_schedule_activitie.created_by == Member.id, Sta_station_schedule_activitie.type_user == 'members'))
                   .outerjoin(Users, and_(Sta_station_schedule_activitie.created_by == Users.id, Sta_station_schedule_activitie.type_user == 'users'))
                   .filter(Sta_station_schedule_activitie.type_user.isnot(None))
                   .filter(Sta_station_schedule_activitie.type_user != '')
                   .filter(Sta_station_schedule_activitie.object == object)
                   .filter(Sta_station_schedule_activitie.reference_id == id)
                   .filter(Sta_station_schedule_activitie.name.in_(['รอออกอากาศ','ส่งออกอากาศ', 'ขอให้ปรับแก้', 'ส่งผลการแก้ไข', 'ปิดงานแก้ไข','ตรวจสอบ']))
                   .order_by(asc(Sta_station_schedule_activitie.id))
                   .all()
    )
    return sql
 
 def get_schedule_activity_onair(db:Session,
                           Sta_station_schedule_activitie:Sta_station_schedule_activitie,
                           Member:Member,
                           Users:Users,
                           id:int
                           ):
      
    first_name_case =   case(
                            (Sta_station_schedule_activitie.type_user == 'members', Member.first_name),
                            (Sta_station_schedule_activitie.type_user == 'users', Users.first_name)
                                
                            ).label('firstName')
    last_name_case =    case(
                        
                            (Sta_station_schedule_activitie.type_user == 'members', Member.last_name),
                            (Sta_station_schedule_activitie.type_user == 'users', Users.last_name)
                        
                             ).label('lastName')
    sql = (db.query(Sta_station_schedule_activitie.id,
                   Sta_station_schedule_activitie.created,
                   first_name_case,
                   last_name_case,
                   Sta_station_schedule_activitie.name,
                   Sta_station_schedule_activitie.description,
                   Sta_station_schedule_activitie.created_by,
                   Sta_station_schedule_activitie.type_user,
                   Sta_station_schedule_activitie.status_id,
                   Member.object_key,
                   Users.object_key,
                   Sta_station_schedule_activitie.type_user
                   )
                   .outerjoin(Member, and_(Sta_station_schedule_activitie.created_by == Member.id, Sta_station_schedule_activitie.type_user == 'members'))
                   .outerjoin(Users, and_(Sta_station_schedule_activitie.created_by == Users.id, Sta_station_schedule_activitie.type_user == 'users'))
                   .filter(Sta_station_schedule_activitie.station_schedule_id == id)
                   .filter(Sta_station_schedule_activitie.name.in_(['ใช้งานสถานี','ปิดการใช้งานสถานี', 'ปิดการใช้งานผังรายการ', 'ปิดการใช้งานผังย่อยรายการ', 'ลบสถานี', 'แบนสถานี' , 'แบนผังรายการ','แบนผังย่อยรายการ','ยกเลิกแบนผังรายการ','ยกเลิกแบนผังย่อยรายการ','รอออกอากาศ','กำลังออกอากาศ','ออกอากาศแล้ว']))
                   .order_by(asc(Sta_station_schedule_activitie.id))

                   
                   .all()
    )
    return sql
 
 @staticmethod
 def update_period_user(db: Session,
                         Sta_station_period:Sta_station_period,
                         user_id:int,
                         id:int,
                         time_update:datetime):
    sql = db.query(Sta_station_period).filter(Sta_station_period.id == id).first()
    sql.user_id = user_id,
    sql.modified = time_update,
    sql.modified_by = user_id
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



