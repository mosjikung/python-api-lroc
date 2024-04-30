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

from model import (Users , 
                   Sta_categories , 
                   Sta_station , 
                   Sta_station_schedule ,
                   Sta_period_types,
                   Sta_audit_statuses,
                   Sta_process_statuses,
                   Sta_broadcast_statuses,
                   Sta_period_times,
                   Sta_station_statuses,
                   Member
                   )

import pdb


T = TypeVar("T")
