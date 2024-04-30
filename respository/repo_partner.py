from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, null,or_ ,func , cast ,Date ,asc ,case ,distinct
from datetime import datetime, timedelta ,date
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM
from sqlalchemy.sql.expression import nulls_last


from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from model import (Sta_partner
                   
                   )

import pdb



T = TypeVar("T")

class BaseRepo:
              @staticmethod
              def get_data_partner(db:Session,
                                  model:Generic[T]):
                            sql = (db.query(model).all())
                            
                            return sql