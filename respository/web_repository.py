from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, null,or_ ,func , cast ,Date ,asc, not_

from datetime import datetime, timedelta
from jose import JWTError, jwt
from config import SECRET_KEY_WEB, ALGORITHM_WEB
from datetime import datetime, timedelta

from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials,OAuth2PasswordBearer
from fastapi import Request, HTTPException


from model import  Users , Member

import pdb


T = TypeVar("T")

class JWTRepo:
    def generate_token(data: dict, expires_delta: Optional[timedelta] = None):

        to_encode = data.copy()
        to_encode2 = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            
            expire = datetime.utcnow() + timedelta(days = 365*2)
            expires = datetime.utcnow() + timedelta(days = 365*2)
        to_encode.update({"exp": expire})
        to_encode2.update({"exp": expires})
       
        
        

        encode_jwt = jwt.encode(to_encode, SECRET_KEY_WEB, algorithm=ALGORITHM_WEB)
        encode_jwt_refresh = jwt.encode(to_encode2, SECRET_KEY_WEB, algorithm=ALGORITHM_WEB)
        return encode_jwt , encode_jwt_refresh

    def decode_token(token: str): #ใช้เวลาตอนอ่านจาก JWTBearer
        try:
            decode_token = jwt.decode(token, SECRET_KEY_WEB, algorithms=[ALGORITHM_WEB])
            return decode_token if decode_token["expires"] >= datetime.time() else None
        except Exception as ex:
          
          return {ex}



class JWTBearer(HTTPBearer):
    
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        
        if credentials: #ถ้ามี token
            
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=401, detail="Invalid authentication sheme."
                )
            
            if credentials.credentials is not None : #check ว่าถ้ามี token
                
                check_payload = self.verfity_jwt(credentials.credentials)
                
                if check_payload is False:
                   
                    raise HTTPException(
                        status_code=401, detail="Invalid token or Token is Expire"
                    )
                else:
                    return credentials.credentials
            
            else:
                HTTPException(
                        status_code=401, detail="Not Found Token"
                    )


                  
                
        else: #ถ้าไม่มีค่า
            raise HTTPException(status=401, detail="Invalid authorization code.")
    
        
    def verfity_jwt(Self, jwttoken: str): #check jwt ว่ามีข้อมูลหรือไม่
        isTokenValid: bool = False
        
        try:
            payload = jwt.decode(jwttoken, SECRET_KEY_WEB, algorithms=[ALGORITHM_WEB])
        except:
            payload = None 
        
        
        if payload:
            isTokenValid = True
        
        return isTokenValid
    
    def refresh_jwt(jwttoken: str):
        try:
            payload = jwt.decode(jwttoken, SECRET_KEY_WEB, algorithms=[ALGORITHM_WEB])
            
            time_add = datetime.now() + timedelta(days = 365*2)
            expire = int(time_add.timestamp())
            
            payload.update({"exp": expire})

            access_token = jwt.encode(payload, SECRET_KEY_WEB, algorithm=ALGORITHM_WEB)

            
            return access_token , jwttoken
        except:
            payload = None
            return HTTPException(
                        status_code=401, detail="Not Found Token"
                    )
        

class Ex_Decode:

    def decode_token(token: str): #ใช้ตอน Ex_decode
         try:
          decode_token = jwt.decode(token, SECRET_KEY_WEB, algorithms=[ALGORITHM_WEB])
          date_time= datetime.fromtimestamp( decode_token["exp"] )
          
          return decode_token if date_time >= datetime.now() else None 
         
         except Exception as ex:
          
          return {ex}