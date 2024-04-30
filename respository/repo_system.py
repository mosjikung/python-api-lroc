from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, null,or_ ,func , cast ,Date ,asc ,select ,extract ,Integer


from datetime import datetime, timedelta ,date
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM


from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from model import (Users,
                   Sta_station,
                   Member,
                   Sta_file_medias
                   )

import pdb


T = TypeVar("T")

class BaseRepo:
              def get_all_station(db: Session,
                            model:Generic[T]
                            ):
                            sql =  (db.query(model)
                                    .all()
                                    )
                            return sql
              
              def check_list_update(db: Session,
                            model:Generic[T],
                            url:str,
                            id:int,
                            ):

                           
                            sql =  (db.query(model)
                                    .filter(model.id == id)
                                    .first()
                                    )
                            sql.icon_path = url
                            sql.modified_by = 1
                            return sql
              
              def get_all_member(db: Session,
                            model:Generic[T]
                            ):

                           
                            sql =  (db.query(model)
                                    .all()
                                    )
                            return sql
              


              def check_list_update_member(db: Session,
                            model:Generic[T],
                            url:str,
                            id:int
                            ):

                           
                            sql =  (db.query(model)
                                    .filter(model.id == id)
                                    .first()
                                    )
                            sql.avatar_img = url
                            sql.modified_by = 1
                            return sql
              


              def check_list_update_playlist(db: Session,
                            model:Generic[T],
                            url:str,
                            id:int
                            ):

                           
                            sql =  (db.query(model)
                                    .filter(model.id == id)
                                    .first()
                                    )
                            sql.file_path = url
                            sql.modified_by = 1
                            return sql
              

              def check_list_update_partner(db: Session,
                            model:Generic[T],
                            url:str,
                            id:int
                            ):

                            
                            sql =  (db.query(model)
                                    .filter(model.id == id)
                                    .first()
                                    )
                            sql.file_path = url
                            sql.modified_by = 1
                            return sql
              

              def check_list_update_file_medias(db: Session,
                            model:Generic[T],
                            url:str,
                            id:int
                            ):

                            
                            sql =  (db.query(model)
                                    .filter(model.id == id)
                                    .first()
                                    )
                            sql.file_path = url
                            sql.modified_by = 1
                            return sql
              
              def check_list_update_sta_channel(db: Session,
                            model:Generic[T],
                            url:str,
                            id:int
                            ):

                            
                            sql =  (db.query(model)
                                    .filter(model.id == id)
                                    .first()
                                    )
                            sql.icon_path = url
                            sql.modified_by = 1
                            return sql
              
              @staticmethod
              def check_data_file_media(db:Session,
                                        file_media:Sta_file_medias):

                        sql = (db.query(file_media)
                               .filter(file_media.is_deleted == 'f')
                               .filter(file_media.bpm == None)
                               .filter(file_media.object_key.isnot(None))
                               .filter(cast(file_media.file_size, Integer) < 6000000)
                               .order_by(desc(file_media.id))
                               .limit(1)
                               .all()
                               )
                        return sql
              
              @staticmethod
              def check_data_file_media_id(db:Session,
                                        file_media:Sta_file_medias,
                                        id:int):

                        sql = (db.query(file_media)
                               .filter(file_media.is_deleted == 'f')
                               .filter(file_media.bpm == None)
                               .filter(file_media.object_key.isnot(None))
                               #.filter(cast(file_media.file_size, Integer) < 6000000)
                               .filter(file_media.id == id)
                               .all()
                               )
                        return sql
              
              @staticmethod
              def prepare_update_file_medias(db:Session,
                                             file_media:Sta_file_medias,
                                             bpm:int,
                                             id:int,
                                             update_time:datetime):
                        sql = (db.query(file_media)
                               .filter(file_media.id == id)
                               .first()
                               )
                        if sql is not None:
                                sql.bpm = bpm
                                sql.modified = update_time

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