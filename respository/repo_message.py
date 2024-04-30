from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session, joinedload , aliased  
from sqlalchemy import desc, null,or_ ,func , cast ,Date ,asc , text 
from sqlalchemy.sql import literal , union , union_all ,  select 


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
                   Sta_message,
                   Sta_message_groups,
                   Sta_message_type,
                   Sta_message_files,
                   Sta_message_statuses,
                   Customer
                   )

import pdb





T = TypeVar("T")

class BaseRepo:

 @staticmethod
 def get_all_message(db: Session,
                         Sta_message:Sta_message,
                         Member:Member,
                         offset:int,
                         limit:int,
                         type:str,
                         order_direction:str,
                         keyword:str,
                         #user_id:int
                         ):
              if type is None:
                      type = "inbox"
              if order_direction is None:
                      order_direction = "desc"
              if keyword is '':
                    keyword =  None
              
              user_id = 600
                    

              if type == "inbox" and order_direction == 'desc' and keyword is None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_status_id == '2')
                   .filter(Sta_message.receive_member_id == user_id)
                   .order_by(desc(Sta_message.created))
                   .all()
                )
               
              elif type == "inbox" and order_direction == 'desc' and keyword is not None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_status_id == '2')
                   .filter(Sta_message.receive_member_id == user_id)
                   .filter(or_(Member.first_name.like(keyword),Sta_message.name.like(keyword)))
                   .order_by(desc(Sta_message.created))
                   .all()
                )
               
              elif type == "inbox" and order_direction == 'asc' and keyword is None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_status_id == '2')
                   .filter(Sta_message.receive_member_id == user_id)
                   .order_by(asc(Sta_message.created))
                   .all()
                )
               
              elif type == "inbox" and order_direction == 'asc' and keyword is not None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_status_id == '2')
                   .filter(Sta_message.receive_member_id == user_id)
                   .filter(or_(Member.first_name.like(keyword),Sta_message.name.like(keyword)))
                   .order_by(asc(Sta_message.created))
                   .all()
                )
              
 
              elif type == "draft" and order_direction == 'desc' and keyword is None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_status_id == '1')
                   .filter(Sta_message.receive_member_id == user_id)
                   .order_by(desc(Sta_message.created))
                   .all()
                )
               
              elif type == "draft" and order_direction == 'desc' and keyword is not None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_status_id == '1')
                   .filter(Sta_message.receive_member_id == user_id)
                   .filter(or_(Member.first_name.like(keyword),Sta_message.name.like(keyword)))
                   .order_by(desc(Sta_message.created))
                   .all()
                )
               
              elif type == "draft" and order_direction == 'asc' and keyword is None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_status_id == '1')
                   .filter(Sta_message.receive_member_id == user_id)
                   .order_by(asc(Sta_message.created))
                   .all()
                )
               
              elif type == "draft" and order_direction == 'asc' and keyword is not None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_status_id == '1')
                   .filter(Sta_message.receive_member_id == user_id)
                   .filter(or_(Member.first_name.like(keyword),Sta_message.name.like(keyword)))
                   .order_by(asc(Sta_message.created))
                   .all()
                )
               

              elif type == "trash" and order_direction == 'desc' and keyword is None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_status_id == '3')
                   .filter(Sta_message.receive_member_id == user_id)
                   .order_by(desc(Sta_message.created))
                   .all()
                )
               

              elif type == "trash" and order_direction == 'desc' and keyword is not None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_status_id == '3')
                   .filter(Sta_message.receive_member_id == user_id)
                   .filter(or_(Member.first_name.like(keyword),Sta_message.name.like(keyword)))
                   .order_by(desc(Sta_message.created))
                   .all()
                )
               

              elif type == "trash" and order_direction == 'asc' and keyword is None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_status_id == '3')
                   .filter(Sta_message.receive_member_id == user_id)
                   .all()
                )
               

              elif type == "trash" and order_direction == 'asc' and keyword is not None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_status_id == '3')
                   .filter(Sta_message.receive_member_id == user_id)
                   .filter(or_(Member.first_name.like(keyword),Sta_message.name.like(keyword)))
                   .order_by(asc(Sta_message.created))
                   .all()
                )

              return results
 


 @staticmethod
 def get_message_type(db: Session,
                         Sta_message:Sta_message,
                         Member:Member,
                         offset:int,
                         limit:int,
                         type:str,
                         order_direction:str,
                         keyword:str,
                         #user_id:int
                         ):
    
              if type is None:
                      type = "problem"
              if order_direction is None:
                      order_direction = "desc"
              if keyword is '':
                    keyword =  None
              
              user_id = 600
                    

              if type == "problem" and order_direction == 'desc' and keyword is None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_type_id == '1')
                   .filter(Sta_message.receive_member_id == user_id)
                   .order_by(desc(Sta_message.created))
                   .all()
                )
               
              elif type == "problem" and order_direction == 'desc' and keyword is not None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_type_id == '1')
                   .filter(Sta_message.receive_member_id == user_id)
                   .filter(or_(Member.first_name.like(keyword),Sta_message.name.like(keyword)))
                   .order_by(desc(Sta_message.created))
                   .all()
                )
               
              elif type == "problem" and order_direction == 'asc' and keyword is None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_type_id == '1')
                   .filter(Sta_message.receive_member_id == user_id)
                   .order_by(asc(Sta_message.created))
                   .all()
                )
               
              elif type == "problem" and order_direction == 'asc' and keyword is not None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_type_id == '1')
                   .filter(Sta_message.receive_member_id == user_id)
                   .filter(or_(Member.first_name.like(keyword),Sta_message.name.like(keyword)))
                   .order_by(asc(Sta_message.created))
                   .all()
                )
               

              elif type == "contact" and order_direction == 'desc' and keyword is None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_type_id == '2')
                   .filter(Sta_message.receive_member_id == user_id)
                   .order_by(desc(Sta_message.created))
                   .all()
                )
               
              elif type == "contact" and order_direction == 'desc' and keyword is not None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_type_id == '2')
                   .filter(Sta_message.receive_member_id == user_id)
                   .filter(or_(Member.first_name.like(keyword),Sta_message.name.like(keyword)))
                   .order_by(desc(Sta_message.created))
                   .all()
                )
               
              elif type == "contact" and order_direction == 'asc' and keyword is None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_type_id == '2')
                   .filter(Sta_message.receive_member_id == user_id)
                   .order_by(asc(Sta_message.created))
                   .all()
                )
               
              elif type == "contact" and order_direction == 'asc' and keyword is not None:  
               results = (db.query(Sta_message,Member)
                   .join(Member,Member.id == Sta_message.form_member_id)
                   .filter(Sta_message.is_deleted == "f")
                   .filter(Sta_message.message_type_id == '2')
                   .filter(Sta_message.receive_member_id == user_id)
                   .filter(or_(Member.first_name.like(keyword),Sta_message.name.like(keyword)))
                   .order_by(asc(Sta_message.created))
                   .all()
                )
               
              return results
 
 @staticmethod
 def get_delete_message(db: Session,
                         Sta_message_groups:Sta_message_groups,
                         Member:Member,
                         Sta_message_type:Sta_message_type,
                         keyword:str,
                         id:int
                         ):
      if keyword is not None:
         search = "%{}%".format(keyword)
         sql = (db.query(Sta_message_groups,Member,Sta_message_type)
               .join(Member , Sta_message_groups.form_member_id == Member.id)
               .join(Sta_message_type, Sta_message_groups.message_type_id == Sta_message_type.id)
               .filter(Sta_message_groups.message_type_id == 1)
               .filter(Sta_message_groups.message_status_id == 3)
               .filter(Sta_message_groups.message_mode.in_(['s-g', 'c-g']))
               .filter(Sta_message_groups.is_deleted == 'f')
               .filter(Sta_message_groups.id == id)
               .filter(or_(Member.username.ilike(search),Sta_message_groups.name.ilike(search)))
               .all()
               )
         
      else:
          sql = (db.query(Sta_message_groups,Member,Sta_message_type)
               .join(Member , Sta_message_groups.form_member_id == Member.id)
               .join(Sta_message_type, Sta_message_groups.message_type_id == Sta_message_type.id)
               .filter(Sta_message_groups.message_type_id == 1)
               .filter(Sta_message_groups.message_status_id == 3)
               .filter(Sta_message_groups.id == id)
               .filter(Sta_message_groups.message_mode.in_(['s-g', 'c-g']))
               .filter(Sta_message_groups.is_deleted == 'f')
               .order_by(desc(Sta_message_groups.id))
               .all()
               )
      return sql
 

 @staticmethod
 def get_delete_message_web(db: Session,
                         Sta_message_groups:Sta_message_groups,
                         Customer:Customer,
                         Sta_message_type:Sta_message_type,
                         keyword:str,
                         id:int
                         ):
      
      if keyword is not None:
         search = "%{}%".format(keyword)

         sql = (db.query(Sta_message_groups,Customer,Sta_message_type)
               .join(Customer , Sta_message_groups.form_customer_id == Customer.id)
               .join(Sta_message_type, Sta_message_groups.message_type_id == Sta_message_type.id)
               .filter(Sta_message_groups.message_type_id == 1)
               .filter(Sta_message_groups.message_status_id == 3)
               .filter(Sta_message_groups.message_mode == 'w-g')
               .filter(Sta_message_groups.is_deleted == 'f')
               .filter(Sta_message_groups.id == id)
               .filter(or_(Member.username.ilike(search),Sta_message_groups.name.ilike(search)))
               .order_by(desc(Sta_message_groups.id))
               .all()
               )
         
      else:
          sql = (db.query(Sta_message_groups,Customer,Sta_message_type)
               .join(Customer , Sta_message_groups.form_customer_id == Customer.id)
               .join(Sta_message_type, Sta_message_groups.message_type_id == Sta_message_type.id)
               .filter(Sta_message_groups.message_type_id == 1)
               .filter(Sta_message_groups.message_status_id == 3)
               .filter(Sta_message_groups.id == id)
               .filter(Sta_message_groups.message_mode == 'w-g')
               .filter(Sta_message_groups.is_deleted == 'f')
               .order_by(desc(Sta_message_groups.id))
               .all()
               )
      return sql
         
 

 @staticmethod
 def get_delete_message_all(db: Session,
                         Sta_message_groups:Sta_message_groups,
                         offset:int,
                         limit:int
                         ):
      
      sql = (db.query(Sta_message_groups)
             .filter(Sta_message_groups.is_deleted == 'f')
             .filter(Sta_message_groups.message_status_id == 3)
             .filter(Sta_message_groups.message_mode.in_(['s-g', 'c-g' , 'w-g']))
             .order_by(desc(Sta_message_groups.created))
             .offset(offset)
             .limit(limit)
             .all()
             )
      return sql
 
 @staticmethod
 def get_message_by_status(db: Session,
                         Sta_message_groups:Sta_message_groups,
                         offset:int,
                         limit:int
                         ):
      
      sql = (db.query(Sta_message_groups)
             .filter(Sta_message_groups.is_deleted == 'f')
             .filter(Sta_message_groups.message_type_id == 1)
             .filter(Sta_message_groups.message_mode.in_(['s-g', 'c-g' , 'w-g']))
             .order_by(desc(Sta_message_groups.created))
             .offset(offset)
             .limit(limit)
             .all()
             )
      return sql
 
 @staticmethod
 def get_message_group_by_status(db: Session,
                         Sta_message_groups:Sta_message_groups,
                         Member:Member,
                         Sta_message_type:Sta_message_type,
                         keyword:str,
                         id:int
                         ):
      if keyword is not None:
         search = "%{}%".format(keyword)
         sql = (db.query(Sta_message_groups,Member,Sta_message_type)
               .join(Member , Sta_message_groups.form_member_id == Member.id)
               .join(Sta_message_type, Sta_message_groups.message_type_id == Sta_message_type.id)
               .filter(Sta_message_groups.message_type_id == 1)
               .filter(Sta_message_groups.message_mode.in_(['s-g', 'c-g']))
               .filter(Sta_message_groups.is_deleted == 'f')
               .filter(Sta_message_groups.id == id)
               .filter(or_(Member.username.ilike(search),Sta_message_groups.name.ilike(search)))
               .all()
               )
      
      else:
          sql = (db.query(Sta_message_groups,Member,Sta_message_type)
               .join(Member , Sta_message_groups.form_member_id == Member.id)
               .join(Sta_message_type, Sta_message_groups.message_type_id == Sta_message_type.id)
               .filter(Sta_message_groups.message_type_id == 1)
               .filter(Sta_message_groups.message_mode.in_(['s-g', 'c-g']))
               .filter(Sta_message_groups.is_deleted == 'f')
               .filter(Sta_message_groups.id == id)
               .all()
               )
          
      return sql
 

 @staticmethod
 def get_message_group_by_status_web(db: Session,
                         Sta_message_groups:Sta_message_groups,
                         Customer:Customer,
                         Sta_message_type:Sta_message_type,
                         keyword:str,
                         id:int
                         ):
      if keyword is not None:
         search = "%{}%".format(keyword)
         sql = (db.query(Sta_message_groups,Customer,Sta_message_type)
               .join(Customer , Sta_message_groups.form_customer_id == Customer.id)
               .join(Sta_message_type, Sta_message_groups.message_type_id == Sta_message_type.id)
               .filter(Sta_message_groups.message_type_id == 1)
               .filter(Sta_message_groups.message_mode== 'w-g')
               .filter(Sta_message_groups.is_deleted == 'f')
               .filter(Sta_message_groups.id == id)
               .filter(or_(Member.username.ilike(search),Sta_message_groups.name.ilike(search)))
               .all()
               )
      else:
          sql = (db.query(Sta_message_groups,Customer,Sta_message_type)
               .join(Customer , Sta_message_groups.form_customer_id == Customer.id)
               .join(Sta_message_type, Sta_message_groups.message_type_id == Sta_message_type.id)
               .filter(Sta_message_groups.message_type_id == 1)
               .filter(Sta_message_groups.message_mode== 'w-g')
               .filter(Sta_message_groups.id == id)
               .filter(Sta_message_groups.is_deleted == 'f')
               .all()
               )
          
      return sql
 


 
 @staticmethod
 def find_message_id(db: Session,
                     model: Generic[T],
                     user_id:int,
                     message_group_id:int):
   sql = (db.query(model)
          .filter(model.created_by == user_id)
          .filter(model.message_group_id == message_group_id)
          .order_by(desc(model.id))
          .first()
          )
   return sql
 
 @staticmethod
 def check_att_file(db: Session,
                    model: Generic[T],
                    message_group_id:int,
                    user_id:int,
                    update_time:datetime):
   sql = db.query(model).filter(model.id == message_group_id).first()
   sql.is_attach_file = True
   sql.modified_by = user_id
   sql.modified = update_time
   
   return sql
 
 @staticmethod
 def update_message_trash(db: Session,
                     model: Generic[T],
                     id:int,
                     update_time:datetime,
                     user_id:int):
    sql = db.query(model).filter(model.id == id).first()
    sql.message_status_id = 3
    sql.modified = update_time
    sql.modified_by = user_id

    return sql
 
 @staticmethod
 def update_message_group(db: Session,
                     model: Generic[T],
                     id:int,
                     update_time:datetime,
                     user_id:int):
    sql = db.query(model).filter(model.id == id).first()
    sql.is_deleted = True
    sql.modified = update_time
    sql.modified_by = user_id

    return sql
 
 @staticmethod
 def find_customer_id_from_sta_message_groups(db:Session,
                                              message_group:Sta_message_groups,
                                              customer:Customer,
                                              message:Sta_message,
                                              message_file:Sta_message_files,
                                              group_id: int):
      sql = (db.query(message_group , customer , message , message_file)
             .join(message, message.message_group_id == message_group.id)
             .join(customer , message_group.form_customer_id == customer.id)
             .outerjoin(message_file,message_file.message_id == message.id)
             .filter(message_group.id ==  group_id)
             .order_by(asc(message.created))
             .first()
             )
      return sql

 @staticmethod
 def search_name(db: Session,model: Generic[T],id:int):
    sql = db.query(model).filter(model.id == id).first()
    return sql
 
 @staticmethod
 def search_data_message(db: Session,Sta_message:Sta_message,Member:Member,id:int):
    sql = (db.query(Sta_message)
    .join(Member,Member_id == Sta_message.form_member_id)
    .filter(Sta_message.id == id).first()
    )
    return sql
 
 @staticmethod
 def delete_message(db: Session,Sta_message:Sta_message,id:int):
    sql = (db.query(Sta_message)
           .filter(Sta_message.id == id)
           .first()
           )
    sql.is_deleted = 'f'
   
    return sql
 

 @staticmethod
 def message_by_id(db: Session,
                   Sta_message_groups:Sta_message_groups,
                   Sta_message:Sta_message,
                   Sta_message_file:Sta_message_files,
                   id:int
                   ):
    sql = (db.query(Sta_message_groups,Sta_message)
          .join(Sta_message,Sta_message_groups.id == Sta_message.message_group_id)
          .outerjoin(Sta_message_files, Sta_message.id == Sta_message_file.message_id)
          .filter(Sta_message_groups.message_type_id == 1)
          .filter(Sta_message_groups.message_mode.in_(['s-g', 'c-g' , 'w-g']))
          .filter(Sta_message_groups.id == id)
          .filter(Sta_message_groups.is_deleted == 'f')
          .order_by(asc(Sta_message_groups.id),asc(Sta_message.id))
          .all()
           )
    return sql
 
 @staticmethod
 def get_data_message_group(db:Session,
                         message_groups:Sta_message_groups,
                         id:int,
                         user_id:int,
                         update_time:datetime):
         sql = db.query(message_groups).filter(message_groups.id == id).first()
         sql.is_deleted = True
         sql.modified_by = user_id
         sql.modified = update_time

         return sql
 
 @staticmethod
 def search_users(db: Session,
                 model: Generic[T],
                 id:int):
   sql = (db.query(model)
          .filter(model.id == id)
          .first()
          )
   return sql
 
 @staticmethod
 def find_message_file(db: Session,
                 model: Generic[T],
                 id:int):
    sql = (db.query(model)
           .filter(model.message_id == id)
           .all()
           )
    return sql
 
 @staticmethod
 def update_message_group_status(db:Session,
                                 message_group:Sta_message_groups,
                                 id:int):
         sql = (db.query(message_group).filter(message_group.id == id).first())
         sql.is_read = True

         return sql
 

 @staticmethod
 def count_message_group(db:Session,
                         model:Generic[T],
                         type:str):
      if type is None:
         type = "inbox"
      if type == "inbox":
         sql = (db.query(model)
                .filter(model.is_read == 'f')
                .filter(model.is_deleted == 'f')
                .filter(model.message_type_id == 1)
                .filter(Sta_message_groups.message_mode.in_(['s-g', 'c-g' , 'w-g']))
                .count()
                )
         
      elif type == "bin":
         sql = (db.query(model)
               .filter(model.is_deleted == 'f')
               .filter(model.message_status_id == 3)
               .filter(Sta_message_groups.message_mode.in_(['s-g', 'c-g' , 'w-g']))
               .filter(model.is_read == 'f')
               .count()
               )

      return sql
   
                     
     
      
      
 
      

 
 @staticmethod
 def update(db: Session, model: Generic[T]):
        db.commit()
        db.refresh(model)
        return True
 
 @staticmethod
 def insert(db: Session, model: Generic[T]):
        db.add(model)
        db.commit()
        db.refresh(model)
        return True
