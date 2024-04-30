from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, null,or_ ,func , cast ,Date ,asc ,case


from datetime import datetime, timedelta ,date
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM


from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from model import (Sta_station , 
                   Sta_station_schedule,
                   Sta_station_period,
                   Stat_customer,
                   Stat_customer_action_detail,
                   Stat_customer_interest
                   
                   )

import pdb



T = TypeVar("T")

class BaseRepo:
              
              

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