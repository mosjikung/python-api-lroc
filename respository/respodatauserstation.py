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

from model import (Sta_station , 
                   Member,
                   Sta_station_member,
                   Sta_station_schedule,
                   Sta_channel_member,
                   Sta_channel,
                   Sta_station_channel
                   )

import pdb

T = TypeVar("T")

class BaseDataUser:
              @staticmethod
              def find_all_member_type_1(db: Session, 
                         Member:Member,
                         Sta_station:Sta_station,
                         Sta_station_member:Sta_station_member,
                         type:str,
                         order_direction:str,
                         keyword:str):
               first_name = None
               last_name = None
               if keyword is not None:
                    search = "%{}%".format(keyword)
               if keyword == '':
                keyword = None
               if order_direction is None:
                 order_direction = 'asc'
               if type is None:
                  type = "data_member"
               
               if type == "data_member"  and order_direction == 'asc'  and keyword is None:
                    print("1")
                    results = (db.query(Member,Sta_station,Sta_station_member)
                   .outerjoin (Sta_station_member,Sta_station_member.member_id == Member.id)            
                   .outerjoin(Sta_station, Sta_station.id == Sta_station_member.station_id)
                   .filter(Member.is_deleted == "f")
                   .filter(Member.is_activated == 't')
                   .filter(Member.member_type_id == 1)
                   .filter(or_(Sta_station.is_deleted == 'f',Sta_station.is_deleted.is_(None)))
                   .count()
                   )
               elif type == "data_member"  and order_direction == 'asc' and  keyword is not None:
                   print("2")
                   results = (db.query(Member,Sta_station,Sta_station_member)
                   .outerjoin (Sta_station_member,Sta_station_member.member_id == Member.id)            
                   .outerjoin(Sta_station, Sta_station.id == Sta_station_member.station_id)
                   .filter(Member.is_deleted == "f")
                   .filter(Member.is_activated == 't')
                   .filter(Member.member_type_id == 1)
                   .filter(or_(Sta_station.is_deleted == 'f',Sta_station.is_deleted.is_(None)))
                   .filter(or_(Member.first_name.like(first_name),Member.last_name.like(last_name),Sta_station.name.like(search),Member.username.like(search),Member.email_verify.like(search)))
                   .count()
                   )

               
               elif type == "data_member"  and order_direction == 'desc'  and keyword is None:
                   print("4")
                   results = (db.query(Member,Sta_station,Sta_station_member)
                   .outerjoin (Sta_station_member,Sta_station_member.member_id == Member.id)            
                   .outerjoin(Sta_station, Sta_station.id == Sta_station_member.station_id)
                   .filter(Member.is_deleted == "f")
                   .filter(Member.is_activated == 't')
                   .filter(Member.member_type_id == 1)
                   .filter(or_(Sta_station.is_deleted == 'f',Sta_station.is_deleted.is_(None)))
                   .count()
                   )
                           
               elif type == "data_member"  and order_direction == 'desc' and  keyword is not None:
                   print("5")
                   results = (db.query(Member,Sta_station,Sta_station_member)
                   .outerjoin (Sta_station_member,Sta_station_member.member_id == Member.id)            
                   .outerjoin(Sta_station, Sta_station.id == Sta_station_member.station_id)
                   .filter(Member.is_deleted == "f")
                   .filter(Member.is_activated == 't')
                   .filter(Member.member_type_id == 1)
                   .filter(or_(Sta_station.is_deleted == 'f',Sta_station.is_deleted.is_(None)))
                   .filter(or_(func.concat(Member.first_name, " ", Member.last_name).ilike(search),
                               func.concat(Member.first_name, "  ", Member.last_name).ilike(search),
                               Sta_station.name.like(search),
                               Member.first_name.ilike(search),
                               Member.last_name.ilike(search),
                               Member.username.like(search),
                               Member.email_verify.like(search)))
                   .count()
                   )

               
               return results
              

              @staticmethod
              def  find_all_member_type_2(db: Session, 
                         Member:Member,
                         Sta_channel:Sta_channel,
                         Sta_channel_member:Sta_channel_member,
                         type:str,
                         order_direction:str,
                         keyword:str):
               first_name = None
               last_name = None
               if keyword is not None:
                search = "%{}%".format(keyword)
               if keyword == '':
                keyword = None
               if order_direction is None:
                 order_direction = 'asc'
               if type is None:
                  type = "data_member"
               
               if type == "data_member"  and order_direction == 'asc'  and keyword is None:
                    print("1")
                    results = (db.query(Member,Sta_channel,Sta_channel_member)
                   .outerjoin(Sta_channel_member,Sta_channel_member.member_id == Member.id)            
                   .outerjoin(Sta_channel, Sta_channel.id == Sta_channel_member.channel_id)
                   .filter(Member.is_deleted == "f")
                   .filter(Member.is_activated == 't')
                   .filter(Member.member_type_id == 2)
                   .filter(or_(Sta_channel.is_deleted == 'f',Sta_channel.is_deleted.is_(None)))
                   .count()
                   )
                    
               elif type == "data_member"  and order_direction == 'asc' and  keyword is not None:
                   print("2")
                   results = (db.query(Member,Sta_channel,Sta_channel_member)
                   .outerjoin(Sta_channel_member,Sta_channel_member.member_id == Member.id)            
                   .outerjoin(Sta_channel, Sta_channel.id == Sta_channel_member.channel_id)
                   .filter(Member.is_deleted == "f")
                   .filter(Member.is_activated == 't')
                   .filter(Member.member_type_id == 2)
                   .filter(or_(Sta_channel.is_deleted == 'f',Sta_channel.is_deleted.is_(None)))
                   .filter(or_(func.concat(Member.first_name, " ", Member.last_name).ilike(search),
                               func.concat(Member.first_name, "  ", Member.last_name).ilike(search),
                               Sta_channel.name.like(search),
                               Member.first_name.ilike(search),
                               Member.last_name.ilike(search),
                               Member.username.like(search),
                               Member.email_verify.like(search)))
                   .count()
                   )

               
               elif type == "data_member"  and order_direction == 'desc'  and keyword is None:
                   print("4")
                   results = (db.query(Member,Sta_channel,Sta_channel_member)
                   .outerjoin(Sta_channel_member,Sta_channel_member.member_id == Member.id)            
                   .outerjoin(Sta_channel, Sta_channel.id == Sta_channel_member.channel_id)
                   .filter(Member.is_deleted == "f")
                   .filter(Member.is_activated == 't')
                   .filter(Member.member_type_id == 2)
                   .filter(or_(Sta_channel.is_deleted == 'f',Sta_channel.is_deleted.is_(None)))
                   .count()
                   )
                           
               elif type == "data_member"  and order_direction == 'desc' and  keyword is not None:
                   print("5")
                   results = (db.query(Member,Sta_channel,Sta_channel_member)
                   .outerjoin(Sta_channel_member,Sta_channel_member.member_id == Member.id)            
                   .outerjoin(Sta_channel, Sta_channel.id == Sta_channel_member.channel_id)
                   .filter(Member.is_deleted == "f")
                   .filter(Member.is_activated == 't')
                   .filter(Member.member_type_id == 2)
                   .filter(or_(Sta_channel.is_deleted == 'f',Sta_channel.is_deleted.is_(None)))
                   .filter(or_(func.concat(Member.first_name, " ", Member.last_name).ilike(search),
                               func.concat(Member.first_name, "  ", Member.last_name).ilike(search),
                               Sta_channel.name.like(search),
                               Member.first_name.ilike(search),
                               Member.last_name.ilike(search),
                               Member.username.like(search),
                               Member.email_verify.like(search)))
                   .count()
                   )
           
               return results


              

              @staticmethod
              def find__data_member_type_1(db: Session, 
                         Member:Member,
                         Sta_station:Sta_station,
                         Sta_station_member:Sta_station_member,
                         offset:int,
                         limit:int,
                         type:str,
                         order_direction:str,
                         keyword:str):
               
               first_name = None
               last_name = None
               if keyword is not None:
                    search = "%{}%".format(keyword)      
               if keyword == '':
                keyword = None
               if order_direction is None:
                 order_direction = 'desc'
               if type is None:
                  type = "data_member"
              
               if type == "data_member"  and order_direction == 'asc'  and keyword is None:
                    print("1")
                    results = (db.query(Member,Sta_station,Sta_station_member)
                   .outerjoin (Sta_station_member,Sta_station_member.member_id == Member.id)            
                   .outerjoin(Sta_station, Sta_station.id == Sta_station_member.station_id)
                   .filter(Member.is_deleted == "f")
                   .filter(Member.is_activated == 't')
                   .filter(Member.member_type_id == 1)
                   .filter(or_(Sta_station.is_deleted == 'f',Sta_station.is_deleted.is_(None)))
                   .order_by(asc(Sta_station.id),asc(Sta_station_member.is_owner))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                    
                
               elif type == "data_member"  and order_direction == 'asc' and  keyword is not None:
                    results = (db.query(Member,Sta_station,Sta_station_member)
                   .outerjoin (Sta_station_member,Sta_station_member.member_id == Member.id)            
                   .outerjoin(Sta_station, Sta_station.id == Sta_station_member.station_id)
                   .filter(Member.is_deleted == "f")
                   .filter(Member.is_activated == 't')
                   .filter(Member.member_type_id == 1)
                   .filter(or_(Sta_station.is_deleted == 'f',Sta_station.is_deleted.is_(None)))
                   .filter(or_(func.concat(Member.first_name, " ", Member.last_name).ilike(search),
                               func.concat(Member.first_name, "  ", Member.last_name).ilike(search),
                               Sta_station.name.like(search),
                               Member.first_name.ilike(search),
                               Member.last_name.ilike(search),
                               Member.username.like(search),
                               Member.email_verify.like(search)))
                   .order_by(asc(Sta_station.id),asc(Sta_station_member.is_owner))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                    

               elif type == "data_member"  and order_direction == 'desc'  and keyword is None:
                   results = (db.query(Member,Sta_station,Sta_station_member)
                   .outerjoin (Sta_station_member,Sta_station_member.member_id == Member.id)            
                   .outerjoin(Sta_station, Sta_station.id == Sta_station_member.station_id)
                   .filter(Member.is_deleted == "f")
                   .filter(Member.is_activated == 't')
                   .filter(Member.member_type_id == 1)
                   .filter(or_(Sta_station.is_deleted == 'f',Sta_station.is_deleted.is_(None)))
                   .order_by(desc(Sta_station.id),desc(Sta_station_member.is_owner))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                   
                           
               elif type == "data_member"  and order_direction == 'desc' and  keyword is not None:
                    
                    results = (db.query(Member,Sta_station,Sta_station_member)
                   .outerjoin (Sta_station_member,Sta_station_member.member_id == Member.id)            
                   .outerjoin(Sta_station, Sta_station.id == Sta_station_member.station_id)
                   .filter(Member.is_deleted == "f")
                   .filter(Member.is_activated == 't')
                   .filter(Member.member_type_id == 1)
                   .filter(or_(Sta_station.is_deleted == 'f',Sta_station.is_deleted.is_(None)))
                   .filter(or_(func.concat(Member.first_name, " ", Member.last_name).ilike(search),
                               func.concat(Member.first_name, "  ", Member.last_name).ilike(search),
                               Sta_station.name.like(search),
                               Member.first_name.ilike(search),
                               Member.last_name.ilike(search),
                               Member.username.like(search),
                               Member.email_verify.like(search)))
                   .order_by(desc(Sta_station.id),desc(Sta_station_member.is_owner))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                    

               

                              
               return results
              


              @staticmethod
              def find__data_member_type_2(db: Session, 
                         Member:Member,
                         Sta_channel:Sta_channel,
                         Sta_channel_member:Sta_channel_member,
                         offset:int,
                         limit:int,
                         type:str,
                         order_direction:str,
                         keyword:str):
               
               first_name = None
               last_name = None
               if keyword is not None:
                    search = "%{}%".format(keyword)

               if keyword is not None:
                search = "%{}%".format(keyword)
               if keyword == '':
                keyword = None
               if order_direction is None:
                 order_direction = 'desc'
               if type is None:
                  type = "data_member"
               
              
               if type == "data_member"  and order_direction == 'asc'  and keyword is None:
                    print("1")
                    results = (db.query(Member,Sta_channel,Sta_channel_member)
                   .outerjoin(Sta_channel_member,Sta_channel_member.member_id == Member.id)            
                   .outerjoin(Sta_channel, Sta_channel.id == Sta_channel_member.channel_id)
                   .filter(Member.is_deleted == "f")
                   .filter(Member.is_activated == 't')
                   .filter(Member.member_type_id == 2)
                   .filter(or_(Sta_channel.is_deleted == 'f',Sta_channel.is_deleted.is_(None)))
                   .order_by(asc(Sta_channel.id),asc(Sta_channel_member.is_owner))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                
               elif type == "data_member"  and order_direction == 'asc' and  keyword is not None:
                   print("2")
                   results = (db.query(Member,Sta_channel,Sta_channel_member)
                   .outerjoin(Sta_channel_member,Sta_channel_member.member_id == Member.id)            
                   .outerjoin(Sta_channel, Sta_channel.id == Sta_channel_member.channel_id)
                   .filter(Member.is_deleted == "f")
                   .filter(Member.is_activated == 't')
                   .filter(Member.member_type_id == 2)
                   .filter(or_(Sta_channel.is_deleted == 'f',Sta_channel.is_deleted.is_(None)))
                   .filter(or_(func.concat(Member.first_name, " ", Member.last_name).ilike(search),
                               func.concat(Member.first_name, "  ", Member.last_name).ilike(search),
                               Sta_channel.name.like(search),
                               Member.first_name.ilike(search),
                               Member.last_name.ilike(search),
                               Member.username.like(search),
                               Member.email_verify.like(search)))
                   .order_by(asc(Sta_channel.id),asc(Sta_channel_member.is_owner))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )

               

               elif type == "data_member"  and order_direction == 'desc'  and keyword is None:
                   print("4")
                   results = (db.query(Member,Sta_channel,Sta_channel_member)
                   .outerjoin(Sta_channel_member,Sta_channel_member.member_id == Member.id)            
                   .outerjoin(Sta_channel, Sta_channel.id == Sta_channel_member.channel_id)
                   .filter(Member.is_deleted == "f")
                   .filter(Member.is_activated == 't')
                   .filter(Member.member_type_id == 2)
                   .filter(or_(Sta_channel.is_deleted == 'f',Sta_channel.is_deleted.is_(None)))
                   .order_by(desc(Sta_channel.id),desc(Sta_channel_member.is_owner))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )
                           
               elif type == "data_member"  and order_direction == 'desc' and  keyword is not None:
                   print("5")
                   results = (db.query(Member,Sta_channel,Sta_channel_member)
                   .outerjoin(Sta_channel_member,Sta_channel_member.member_id == Member.id)            
                   .outerjoin(Sta_channel, Sta_channel.id == Sta_channel_member.channel_id)
                   .filter(Member.is_deleted == "f")
                   .filter(Member.is_activated == 't')
                   .filter(Member.member_type_id == 2)
                   .filter(or_(Sta_channel.is_deleted == 'f',Sta_channel.is_deleted.is_(None)))
                   .filter(or_(func.concat(Member.first_name, " ", Member.last_name).ilike(search),
                               func.concat(Member.first_name, "  ", Member.last_name).ilike(search),
                               Sta_channel.name.like(search),
                               Member.first_name.ilike(search),
                               Member.last_name.ilike(search),
                               Member.username.like(search),
                               Member.email_verify.like(search)))
                   .order_by(desc(Sta_channel.id),desc(Sta_channel_member.is_owner))
                   .offset(offset)
                   .limit(limit)
                   .all()
                   )

               

                              
               return results
              

              @staticmethod
              def find_all_member_type_1_none(db: Session, 
                         Member:Member,
                         Sta_station:Sta_station,
                         Sta_station_member:Sta_station_member):
               
               
            
                results = (db.query(Member,Sta_station,Sta_station_member)
                .outerjoin (Sta_station_member,Sta_station_member.member_id == Member.id)            
                .outerjoin(Sta_station, Sta_station.id == Sta_station_member.station_id)
                .filter(Member.is_deleted == "f")
                .filter(Member.is_activated == 't')
                .filter(Member.member_type_id == 1)
                .filter(or_(Sta_station.is_deleted == 'f',Sta_station.is_deleted.is_(None)))
                .count()
                   )
                return results
              

              @staticmethod
              def find_all_member_type_2_none(db: Session, 
                         Member:Member,
                         Sta_channel:Sta_channel,
                         Sta_channel_member:Sta_channel_member):

                results = (db.query(Member,Sta_channel,Sta_channel_member)
                   .outerjoin(Sta_channel_member,Sta_channel_member.member_id == Member.id)            
                   .outerjoin(Sta_channel, Sta_channel.id == Sta_channel_member.channel_id)
                   .filter(Member.is_deleted == "f")
                   .filter(Member.is_activated == 't')
                   .filter(Member.member_type_id == 2)
                   .filter(or_(Sta_channel.is_deleted == 'f',Sta_channel.is_deleted.is_(None)))
                   .count()
                   )
                return results
              

              

              @staticmethod
              def check_email_station(db:Session , model:Generic[T], email:str):
               sql = db.query(model).filter(model.email_verify == email).first()
               return sql  
              
              @staticmethod
              def check_data_station(db:Session , model:Generic[T], station_id:int):
               sql = db.query(model).filter(model.id == station_id).first()
               return sql
              
              @staticmethod
              def find_user_name(db:Session , model:Generic[T], id:int , username:str):
                 sql = (db.query(model)
                        .filter(model.id == id)
                        .filter(model.username == username)
                        .first()
                        )
                 return sql
              
              @staticmethod
              def check_duplicate_email_station(db:Session, model:Generic[T], emails:str):
                 sql = db.query(model).filter(model.email == emails).first()
                 return sql
              

              
              @staticmethod
              def update_station_waitting_by_id(db:Session, 
                                                model:Generic[T], 
                                                id:int ,
                                                update_time:datetime ,
                                                uniqe_real_link:str,
                                                expire:datetime
                                                ):
                 sql = db.query(model).filter(model.id == id).first()
                 sql.modified = update_time
                 sql.unique_link = uniqe_real_link
                 sql.expire_time = expire
                 
                 return sql
              


              @staticmethod
              def update_channel_waitting_by_id(db:Session, 
                                                model:Generic[T], 
                                                id:int ,
                                                update_time:datetime ,
                                                uniqe_real_link:str,
                                                expire:datetime
                                                ):
                 sql = db.query(model).filter(model.id == id).first()
                 sql.modified = update_time
                 sql.unique_link = uniqe_real_link
                 sql.expire_time = expire
                 
                 return sql
              
              
              @staticmethod
              def check_duplicate_email_channel(db:Session, model:Generic[T], emails:str):
                 sql = db.query(model).filter(model.email == emails).first()
                 return sql
              
              @staticmethod
              def check_station_waiting(db:Session , model:Generic[T], token:str):
               sql = db.query(model).filter(model.uniqe_link == token).first()
               return sql
              
              @staticmethod
              def check_channel_data(db:Session ,
                                    Sta_station_channel:Sta_station_channel,
                                    Sta_channel:Sta_channel,
                                    ):
               sql = (db.query(Sta_station_channel,Sta_channel)
                     .join(Sta_channel , Sta_station_channel.channel_id == Sta_channel.id)
                     .filter(Sta_station_channel.station_channel_invite_status_id == 2)
                     .filter(Sta_station_channel.is_deleted == 'f')
                     .all())
               return sql 
              
              @staticmethod
              def get_channel(db:Session,
                              Sta_channel:Sta_channel):
                 sql = db.query(Sta_channel).filter(Sta_channel.is_deleted == 'f').all()
                       
                 return sql
              
              @staticmethod
              def delete_user_station(db:Session,
                              model:Generic[T],
                              id:int):
                 sql = db.query(model).filter(model.id == id).first()
                 sql.is_deleted = True
                       
                 return sql
    