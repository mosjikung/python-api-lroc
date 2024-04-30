from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, null,or_ ,func , cast ,Date ,asc ,case ,distinct,text
from datetime import datetime, timedelta ,date
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM
from sqlalchemy.sql.expression import nulls_last



from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from model import (Sta_station,
                   Sta_help_type,
                   Sta_report_type,
                   Sta_request,
                   Customer,
                   Countries,
                   Sta_message_groups,
                   Sta_message,
                   Sta_support_groups,
                   Sta_support_detail
                   
                   )

import pdb
T = TypeVar("T")

class BaseRepo:
              @staticmethod
              def get_all_data_help(db:Session,
                                   model:Generic[T]):
                            sql = (db.query(model)
                                   .filter(model.is_deleted == 'f')
                                   .all()
                                   )
                            
                            return sql
              
              @staticmethod
              def get_data_ticket_id(db:Session,
                                     request:Sta_request):
                            sql = (db.query(request)
                                   .filter(request.id == 1)
                                   .all()
                                   )
                            return sql
              

              @staticmethod
              def get_data_all_country(db:Session,
                                       country:Countries):
                            sql = (db.query(country)
                                   .filter(country.is_deleted == 'f')
                                   .all()
                                   )
                            return sql
              
              
              @staticmethod
              def prepare_update(db:Session,
                                 request:Sta_request,
                                 today:str,
                                 new_id:int):
                            sql = db.query(request).filter(request.id == new_id).first()
                            sql.ticket_id = today

                            return sql
              
              @staticmethod
              def check_data_user(db:Session,
                                  customer:Customer,
                                  id:int):
                            sql = db.query(customer).filter(customer.id == id).first()

                            return sql
              
              @staticmethod
              def check_email_data(db:Session,
                                   customer:Customer,
                                   email:str):
                            sql = (db.query(customer)
                                   .filter(customer.email == email)
                                   .filter(customer.is_deleted == 'f')
                                   .first()
                                   )
                            return sql
   
              @staticmethod
              def insert_data_next_value(db:Session,
                                         request:Sta_request,
                                         help_type:Sta_help_type,
                                         sta_message_groups:Sta_message_groups,
                                         station_id:int,
                                         channel_id:int,
                                         name:str,
                                         description:str,
                                         form_member_id:int,
                                         receive_member_id:int,
                                         message_type_id:int,
                                         message_status_id:int,
                                         reference_id:int,
                                         message_mode:str,
                                         form_customer_id:int,
                                         ticket_id:int,
                                         request_id:int,
                                         is_attach_file:bool,
                                         user_id:int,
                                         update_time:datetime):
                     
                     values = {
                            'is_deleted': False,
                            'created': func.CURRENT_TIMESTAMP(),
                            'created_by': user_id,
                            'modified': None,
                            'modified_by': None,
                            'station_id': station_id,
                            'channel_id': channel_id,
                            'name': 'ส่งคำขอ',
                            'description': help_type.name,
                            'form_member_id': None,
                            'receive_member_id': None,
                            'message_type_id': 1,
                            'message_status_id': 2,
                            'object': 'w-g',
                            'reference_id': None,
                            'message_mode': 'w-g',
                            'is_attach_file': is_attach_file,
                            'form_customer_id': user_id,
                            'ticket_id': ticket_id,
                            'request_id': request_id
                            }
                     query = sta_message_groups(**values)

                     db.add(query)
                     db.commit()
                     return True
              

              @staticmethod
              def get_next_value_data_message(db:Session,
                                              message_group:Sta_message_groups,
                                              request:Sta_request,
                                              help_type:Sta_help_type,
                                              request_id:int):
                     sql =  (db.query(
                            func.nextval('sta_message_groups_id_seq').label('nextval'),
                            request.created_by,
                            request.ticket_id,
                            request.id,
                            help_type.name)
                            .join(help_type, request.help_type_id == help_type.id)
                            .filter(request.is_deleted == 'f')
                            .filter(request.id == request_id)
                            .one()

                     )
                     return sql

              
              @staticmethod
              def get_next_value_data_message_2(db:Session,
                                              message_group:Sta_message_groups,
                                              request:Sta_request,
                                              help_type:Sta_help_type,
                                              report:Sta_report_type,
                                              country:Countries,
                                              message_group_id:int):
                     sql =  (db.query(
                            func.nextval('sta_messages_id_seq').label('nextval'),
                            message_group.id,
                            request.ticket_id,
                            help_type.name,
                            request.email,
                            country.name,
                            report.name,
                            request.link,
                            request.description,
                            request.file_name,
                            request.created,
                            request.created_by,
                            request.id)
                            .join(request,  message_group.request_id == request.id)
                            .join(help_type, request.help_type_id == help_type.id)
                            .join(report, request.report_type_id == report.id)
                            .join(country, request.country_id == country.id)
                            .filter(request.is_deleted == 'f')
                            .filter(message_group.id == message_group_id)
                            .one()
                     )
                     return sql
              
              @staticmethod
              def find_next_value_request_id(db:Session,
                                             message_group:Sta_message_groups,
                                             message:Sta_message,
                                             request:Sta_request,
                                             request_id:int,
                                             message_id:int):
                     
                     sql =  (db.query(
                            func.nextval('sta_message_files_id_seq').label('nextval'),
                            message_group.id,
                            message.id,
                            request.file_name,
                            request.file_path,
                            request.file_type,
                            request.file_size,
                            request.object_key)
                            .join(message,  message_group.id == message.message_group_id)
                            .join(request, message_group.request_id == request.id)
                            .filter(request.is_deleted == 'f')
                            .filter(request.id == request_id)
                            .filter(message.id == message_id)
                            .one()
                     )
                     
                     return sql
              
              @staticmethod
              def get_data_support_group(db:Session,
                                         support:Sta_support_groups,
                                         keyword:str):
                     if keyword is not None:
                            search = "%{}%".format(keyword)
                            sql = (db.query(support)
                                   .filter(support.is_deleted == 'f')
                                   .filter(or_(support.topic_en.ilike(search),support.topic_lo.ilike(search),support.topic_th.ilike(search),support.description_th.ilike(search),support.description_en.ilike(search),support.description_lo.ilike(search)))
                                   .all()
                                   )
                     else:
                            sql = (db.query(support)
                                   .filter(support.is_deleted == 'f')
                                   .all()
                                   )
                     return sql
              
              @staticmethod
              def get_data_support_detail_by_id(db:Session,
                                                sup_detail:Sta_support_detail,
                                                sup_id:int):
                     
                     sql = (db.query(Sta_support_detail)
                            .filter(sup_detail.support_group_id == sup_id)
                            .filter(sup_detail.is_deleted == 'f')
                            .filter(sup_detail.parent_id == None)
                            .all()
                            )
                     
                     return sql
              
              @staticmethod
              def get_data_support_detail_list_by_id(db:Session,
                                                sup_detail:Sta_support_detail,
                                                id:int):
                     
                     sql = (db.query(Sta_support_detail)
                            .filter(sup_detail.id == id)
                            .filter(sup_detail.is_deleted == 'f')
                            .all()
                            )
                     
                     return sql
              
              @staticmethod
              def get_data_support_detail_parent_by_id(db:Session,
                                                sup_detail:Sta_support_detail,
                                                parent_id:int):
                     
                     sql = (db.query(Sta_support_detail)
                            .filter(sup_detail.is_deleted == 'f')
                            .filter(sup_detail.parent_id == parent_id)
                            .all()
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
              def  rollback(db: Session):
                            db.rollback()
                            return False
              
              