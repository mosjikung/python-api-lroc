from fastapi import APIRouter, Depends
import os
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from typing import List , Optional
from schema import (
    RequestSchema,
    ResponseSchema,
    TokenResponse,
    UserSigupSchema,
    UserSiginSchema,
    Updatestationmember,
    Insertstationmember,
    Mainresp,
    Checkemaildata,
    ChangePasswordResp,
    Checkemaildatachannel,
    Setdatastation,
    Deleteduser
)

from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from pathlib import Path
from passlib.context import CryptContext
from respository.repository import JWTRepo, JWTBearer, UsersRepo, BaseRepo ,Ex_Decode
from respository.respodatauserstation import BaseDataUser
from model import (Sta_station , 
                   Member,
                   Sta_station_member,
                   Sta_station_schedule,
                   Sta_channel_member,
                   Sta_channel,
                   Sta_station_member_waitings,
                   Sta_channel_member_waitings,
                   Sta_station_channel,
                   Users
                   )
from datetime import datetime, timedelta
import pdb
from config import MAIL_USERNAME,MAIL_PASSWORD,MAIL_FROM,MAIL_PORT,MAIL_SERVER,MAIL_FROM_NAME
from minio_handler import MinioHandler
import hashlib
import random
import string




router = APIRouter(
              prefix="",
              tags=['Data users stations'],
              responses ={404:{
                            'message' : "No found"
              }}
              
)


# encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""
    Authentication Router
"""

from dotenv import load_dotenv
load_dotenv('.env')

class Envs:
    MAIL_USERNAME = MAIL_USERNAME
    MAIL_PASSWORD = MAIL_PASSWORD
    MAIL_FROM = MAIL_FROM
    MAIL_PORT = int(MAIL_PORT)
    MAIL_SERVER = MAIL_SERVER
    MAIL_FROM_NAME = MAIL_FROM_NAME



def __init__(self, http_code: int = None, code: str = None, message: str = None):
        self.http_code = http_code if http_code else 500
        self.code = code if code else str(self.http_code)
        self.message = message
	

conf = ConnectionConfig(
    MAIL_USERNAME = Envs.MAIL_USERNAME,
    MAIL_PASSWORD = Envs.MAIL_PASSWORD,
    MAIL_FROM = Envs.MAIL_FROM,
    MAIL_PORT = Envs.MAIL_PORT,
    MAIL_SERVER = Envs.MAIL_SERVER,
    MAIL_FROM_NAME= Envs.MAIL_FROM_NAME,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER = Path(__file__).parent / '../templates/email'
)


def ramdomword():
    password_length = 12

    #define the pool of characters to choose from
    characters = string.ascii_letters + string.digits + string.punctuation

    # generate a random password
    word = ''.join(random.choice(characters) for i in range(password_length))

    return word





@router.get("/get-all-list-member",dependencies=[Depends(JWTBearer())])
async def get_all_list_member(offset:Optional[int]=None,
                            limit:Optional[int]=None,
                            type:Optional[str]=None,
                            order_direction:Optional[str]=None,
                            member_types_id:Optional[int]=None,
                            keyword:Optional[str]=None,
                            db: Session = Depends(get_db)):
    
    
    results_list = []
    last_results = []
    count_memberx = BaseDataUser.find_all_member_type_1_none(db,Member,Sta_station,Sta_station_member)
    count_memberx2 = BaseDataUser.find_all_member_type_2_none(db,Member,Sta_channel,Sta_channel_member)

    if member_types_id == 1:
     
     _member = BaseDataUser.find__data_member_type_1(db,Member,Sta_station,Sta_station_member,offset,limit,type,order_direction,keyword)
     count_member = BaseDataUser.find_all_member_type_1(db,Member,Sta_station,Sta_station_member,type,order_direction,keyword)
     
     for members , sta_stations , sta_station_members  in _member:
        bucket_name = 'member'
        if members.object_key is not None:
                    
                object_name = members.object_key
                  
                url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
                  
                 
        else:
                url = None
      
        
        if sta_station_members is None:
             role_station = None
             is_owner = None
        else:
                if sta_station_members.is_owner == True:
                    role_station = 'เจ้าของสถานี'
                    is_owner = True
                else:
                    role_station = 'ทีมงานสถานี'
                    is_owner = False
        if sta_stations is None:
             sta_station_id = None
             sta_station_name = None
             sta_station_modified = None
        else:
             sta_station_id = sta_stations.id
             sta_station_name = sta_stations.name
             sta_station_modified = sta_stations.modified
             
        results_list.append({
            'id':members.id,
            'member_role_id':members.member_role_id,
            'station_id':sta_station_id,
            'first_name':members.first_name,
            'last_name':members.last_name,
            'display_name':members.display_name,
            'email':members.email_verify,
            'avatar_img':url,
            'station_name':sta_station_name,
            'is_owner':is_owner,
            'role':role_station,
            'modified':sta_station_modified,
            'username':members.username,
            'register_for':members.member_type_id,
            'created':members.created

        })
     
    if member_types_id == 2:
     _member = BaseDataUser.find__data_member_type_2(db,
                                                     Member,
                                                     Sta_channel,
                                                     Sta_channel_member,
                                                     offset,
                                                     limit,
                                                     type,
                                                     order_direction,
                                                     keyword)
     count_member2 = BaseDataUser.find_all_member_type_2(db,Member,Sta_channel,Sta_channel_member,type,order_direction,keyword)
     
     for members , sta_channels , sta_channel_members   in _member:
        
        if sta_channel_members is None:
             role_station = None
             is_owner = None
        else:
                if sta_channel_members.is_owner == True:
                    role_station = 'เจ้าของรายการ'
                    is_owner = True
                else:
                    role_station = 'ทีมงานรายการ'
                    is_owner = False
        if sta_channels is None:
             sta_channels_id = None
             sta_channels_name = None
             sta_channels_modified = None
        else:
             sta_channels_id = sta_channels.id
             sta_channels_name = sta_channels.name
             sta_channels_modified = sta_channels.modified
        results_list.append({
            'id':members.id,
            'member_role_id':members.member_role_id,
            'station_id':sta_channels_id,
            'first_name':members.first_name,
            'last_name':members.last_name,
            'display_name':members.display_name,
            'email':members.email_verify,
            'avatar_img':members.avatar_img,
            'station_name':sta_channels_name,
            'is_owner':is_owner,
            'role':role_station,
            'modified':sta_channels_modified,
            'username':members.username,
            'register_for':members.member_type_id

        })
        
     
     
    if member_types_id is None:
     _member = BaseDataUser.find__data_member_type_1(db,Member,Sta_station,Sta_station_member,offset,limit,type,order_direction,keyword)
     count_member = BaseDataUser.find_all_member_type_1(db,Member,Sta_station,Sta_station_member,type,order_direction,keyword)
     count_member2 = BaseDataUser.find_all_member_type_2(db,Member,Sta_channel,Sta_channel_member,type,order_direction,keyword)
    
     
     for members , sta_stations , sta_station_members   in _member:
        bucket_name = 'member'
        if members.object_key is not None:
                    
                object_name = members.object_key
                  
                url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
                  
                 
        else:
                url = None

        if sta_station_members is None:
             role_station = None
             is_owner = None
        else:
                if sta_station_members.is_owner == True:
                    role_station = 'เจ้าของสถานี'
                    is_owner = True
                else:
                    role_station = 'ทีมงานสถานี'
                    is_owner = False
        if sta_stations is None:
             sta_station_id = None
             sta_station_name = None
             sta_station_modified = None
        else:
             sta_station_id = sta_stations.id
             sta_station_name = sta_stations.name
             sta_station_modified = sta_stations.modified
             
        results_list.append({
            'id':members.id,
            'member_role_id':members.member_role_id,
            'station_id':sta_station_id,
            'first_name':members.first_name,
            'last_name':members.last_name,
            'display_name':members.display_name,
            'email':members.email_verify,
            'avatar_img':url,
            'station_name':sta_station_name,
            'is_owner':is_owner,
            'role':role_station,
            'modified':sta_station_modified,
            'username':members.username,
            'register_for':members.member_type_id

        })
     
    if (member_types_id == 1 or member_types_id is None) and keyword is None:
         last_results = [
        {
           'count_station':count_memberx,
           'count_schedule':count_memberx2,
           'data':results_list
        }
     ]
    elif (member_types_id == 1 or member_types_id is None) and keyword is not None:
        last_results = [
        {
           'count_station':count_member,
           'count_schedule':count_memberx2,
           'data':results_list
        }
        ]
    elif (member_types_id == 2) and keyword is None:
        last_results = [
        {
           'count_station':count_memberx,
           'count_schedule':count_memberx2,
           'data':results_list
        }
        ]
    elif (member_types_id == 2) and keyword is not None:
        last_results = [
        {
           'count_station':count_memberx,
           'count_schedule':count_member2,
           'data':results_list
        }
        ]
  
    
    
    try:
        return ResponseSchema(
            code="200", status="Ok", message="Success save data" , result=last_results
        ).dict(exclude_none=True)
    except Exception as error:
        print(error.args)
        return ResponseSchema(
            code="500", status="Error", message="Internal Server Error"
        ).dict(exclude_none=True)
    

@router.patch("/delete-station-member/{id}")
async def delete_station_member(db: Session = Depends(get_db)):
    _del_member = UsersRepo.find_all_member(db,Sta_station_member)
    results  = BaseRepo.update(db, _del_member)
 
   
    return ResponseSchema(
        code="200", status="Ok", message="Update successfull"
    )


@router.put("/update-station-member")
async def update_station_member(request:Updatestationmember,  db: Session = Depends(get_db)):
        time_update = datetime.now()
        Update_data = BaseRepo.update_station_member(db,
                                          request.id,
                                          Sta_station_member ,
                                          time_update,
                                          request.member_id,
                                          request.station_id,
                                          request.is_owner,
                                        )
        results  = BaseRepo.update(db, Update_data)
        

        if Update_data is None:
            return ResponseSchema(
             code="404", status="Ok", message="Query Has Problem", result=Mainresp(result=False, message="Query Has Problem")
            ).dict(exclude_none=True)
        else:
            return ResponseSchema(
             code="200", status="Ok", message="Data Update Successful", result=Mainresp(result=True, message="Data Update Successful")
            ).dict(exclude_none=True)

@router.post("/create-station-member")
async def create_station_member(request:Insertstationmember,  db: Session = Depends(get_db)):
        
        time_update = datetime.now()
        try:
        # insert user to db
            _station_member = Sta_station_member(
                    created=time_update,
                    created_by=request.member_id,
                    station_id=request.station_id,
                    member_id = request.member_id,
                    is_owner=request.is_owner,
            )
            BaseRepo.insert(db, _station_member)
            return ResponseSchema(
            code="200", status="Ok", message="Success save data"
             ).dict(exclude_none=True)
        except Exception as error:
            return ResponseSchema(
            code="500", status="Error", message="Internal Server Error"
            ).dict(exclude_none=True)

@router.post("/check-email-data-station",dependencies=[Depends(JWTBearer())])
async def check_email_data(request:Checkemaildata,token: str = Depends(JWTBearer()),  db: Session = Depends(get_db)):
        results_check_email = BaseDataUser.check_email_station(db,
                                                           Member,
                                                           request.email
                                                           )
        results_check_station = BaseDataUser.check_data_station(db,
                                                              Sta_station,
                                                              request.station_id)
        
        
        time_update = datetime.now()
        decode_token = Ex_Decode.decode_token(token)
        user_id = decode_token["id"]
        user_name = decode_token["sub"]
        find_username = BaseDataUser.find_user_name(db,
                                                     Users,
                                                     user_id,
                                                     user_name)
        
        if results_check_email is None:
           
            
            check_email_waiting = BaseDataUser.check_duplicate_email_station(db,
                                                                         Sta_station_member_waitings,
                                                                         request.email)
            
            if check_email_waiting is None:
                emails = request.email
                uniqe_link = ramdomword()
                result_link = hashlib.md5(uniqe_link.encode())
                uniqe_real_link = result_link.hexdigest()
                #md5
                value_type = "station"
                expire =  datetime.now() + timedelta(hours=48)
                main_value = [emails]
                value2 = dict({"user_id":user_name,"first_name":find_username.first_name,"last_name":find_username.last_name ,"title":"Invite you to join","email":emails ,"station":results_check_station.name,"unique_link":uniqe_real_link,"value_type":value_type})
                message = MessageSchema(
                    subject="Invite you to join",
                    recipients=main_value,
                    template_body=value2,
                    subtype=MessageType.html,
                    sender=("LRNOC", "app.cloud.service@gmail.com")
                    )

                _station_member = Sta_station_member_waitings(
                        created=time_update,
                        created_by=user_id,
                        station_id=request.station_id,
                        unique_link = uniqe_real_link,
                        expire_time = expire,
                        email = emails,
                        station_role_id = 2
                        
                )
                BaseRepo.insert(db, _station_member)
                
            else:
                
                emails = request.email
                uniqe_link = ramdomword()
                result_link = hashlib.md5(uniqe_link.encode())
                uniqe_real_link = result_link.hexdigest()
                #md5
                value_type = "station"
                expire =  datetime.now() + timedelta(hours=48)
                main_value = [emails]
                value2 = dict({"user_id":user_name ,"first_name":find_username.first_name,"last_name":find_username.last_name ,"title":"Invite you to join","email":emails ,"station":results_check_station.name,"unique_link":uniqe_real_link,"value_type":value_type})
                message = MessageSchema(
                    subject="Invite you to join",
                    recipients=main_value,
                    template_body=value2,
                    subtype=MessageType.html,
                    sender=("LRNOC", "app.cloud.service@gmail.com")
                    )
                _update_data = BaseDataUser.update_station_waitting_by_id(db,
                                                             Sta_station_member_waitings,
                                                             check_email_waiting.id,
                                                             time_update,
                                                             uniqe_real_link,
                                                             expire)
                

                BaseRepo.update(db, _update_data)
            
            fm = FastMail(conf)
            await fm.send_message(message, template_name="email_template.html")
            if fm.send_message is None:
                return  ResponseSchema(
                code="404", status="Ok", message="Error sent Mail", result=ChangePasswordResp(result=False, message="Error sent Email")
                ).dict(exclude_none=True)

            else:
              return  ResponseSchema(
             code="200", status="Ok", message="Data Not Found", result=ChangePasswordResp(result=True, message="Email Has been Sent")
            ).dict(exclude_none=True)
        else:
             return  ResponseSchema(
                code="200", status="Ok", message="Data Found", result=ChangePasswordResp(result=False, message="emailAlreadyRegistered")
                ).dict(exclude_none=True)


@router.post("/check-email-data-channel",dependencies=[Depends(JWTBearer())])
async def check_email_data(request:Checkemaildatachannel,token: str = Depends(JWTBearer()),  db: Session = Depends(get_db)):
        results_check_email = BaseDataUser.check_email_station(db,
                                                           Member,
                                                           request.email
                                                           )
        results_check_channel = BaseDataUser.check_data_station(db,
                                                              Sta_channel,
                                                              request.channel_id)
        time_update = datetime.now()
        decode_token = Ex_Decode.decode_token(token)
        user_id = decode_token["id"]
        user_name = decode_token["sub"]
        find_username = BaseDataUser.find_user_name(db,
                                                     Users,
                                                     user_id,
                                                     user_name)
        if results_check_email is None:
           
            
            check_email_waiting = BaseDataUser.check_duplicate_email_station(db,
                                                                         Sta_channel_member_waitings,
                                                                         request.email)
            
            if check_email_waiting is None:
                emails = request.email
                uniqe_link = ramdomword()
                result_link = hashlib.md5(uniqe_link.encode())
                uniqe_real_link = result_link.hexdigest()
                #md5
                value_type = "channel"
                expire =  datetime.now() + timedelta(hours=48)
                main_value = [emails]
                value2 = dict({"user_id":user_name ,"first_name":find_username.first_name,"last_name":find_username.last_name ,"title":"Invite you to join","email":emails ,"channel":results_check_channel.name,"unique_link":uniqe_real_link,"value_type":value_type})
                message = MessageSchema(
                    subject="Invite you to join",
                    recipients=main_value,
                    template_body=value2,
                    subtype=MessageType.html
                    )

                _channel_member = Sta_channel_member_waitings(
                        created=time_update,
                        created_by=user_id,
                        channel_id=request.channel_id,
                        unique_link = uniqe_real_link,
                        expire_time = expire,
                        email = emails,
                        channel_role_id = 2
                        
                )
                BaseRepo.insert(db, _channel_member)
                
            else:
                
                emails = request.email
                uniqe_link = ramdomword()
                result_link = hashlib.md5(uniqe_link.encode())
                uniqe_real_link = result_link.hexdigest()
                #md5
                value_type = "channel"
                expire =  datetime.now() + timedelta(hours=48)
                main_value = [emails]
                value2 = dict({"user_id":user_name ,"first_name":find_username.first_name,"last_name":find_username.last_name ,"title":"Invite you to join","email":emails ,"channel":results_check_channel.name,"unique_link":uniqe_real_link,"value_type":value_type})
                message = MessageSchema(
                    subject="Invite you to join",
                    recipients=main_value,
                    template_body=value2,
                    subtype=MessageType.html
                    )
                _update_data = BaseDataUser.update_channel_waitting_by_id(db,
                                                             Sta_channel_member_waitings,
                                                             check_email_waiting.id,
                                                             time_update,
                                                             uniqe_real_link,
                                                             expire)
                
                results_update = BaseRepo.update(db,_update_data)
            
            fm = FastMail(conf)
            await fm.send_message(message, template_name="email_template2.html")
            if fm.send_message is None:
                return  ResponseSchema(
                code="404", status="Ok", message="Error sent Mail", result=ChangePasswordResp(result=False, message="Error sent Email")
                ).dict(exclude_none=True)

            else:
              return  ResponseSchema(
             code="200", status="Ok", message="Data Not Found", result=ChangePasswordResp(result=True, message="Email Has been Sent")
            ).dict(exclude_none=True)
        else:
             return  ResponseSchema(
                code="200", status="Ok", message="Data Found", result=ChangePasswordResp(result=False, message="This email has already been registered.")
                ).dict(exclude_none=True)
        

@router.patch("/set-data-station",dependencies=[Depends(JWTBearer())])
async def set_data_station(request:Setdatastation,token: str = Depends(JWTBearer()),  db: Session = Depends(get_db)):
     check_data_station = BaseDataUser.check_data_station_update(db,
                                                                 Sta_station_member,
                                                                 request.id,
                                                                 request.station_id,
                                                                 request.is_owner)
     resutls_update = BaseRepo.update(db,check_data_station)


@router.patch("/set-data-channel",dependencies=[Depends(JWTBearer())])
async def set_data_channel(request:Setdatastation,token: str = Depends(JWTBearer()),  db: Session = Depends(get_db)):
     check_data_channel = BaseDataUser.check_data_channel_update(db,
                                                                 Sta_channel_member,
                                                                 request.id,
                                                                 request.station_id,
                                                                 request.is_owner)
     resutls_update = BaseRepo.update(db,check_data_channel)


@router.get("/get-all-channel",dependencies=[Depends(JWTBearer())])
async def get_all_activity(db: Session = Depends(get_db)):
      resutls = BaseDataUser.get_channel(db,
                                     Sta_channel)
      resutls_all = []
      for x in resutls:
        resutls_all.append({
                'id':x.id,
                'name':x.name
        })
      return ResponseSchema(
         code="200", status="Ok", message="Sucess retrieve data", result=resutls_all
     ).dict(exclude_none=True)

@router.delete("/delete-user-station",dependencies=[Depends(JWTBearer())])
async def deleted_user_station(id:Optional[int]=None, db: Session = Depends(get_db)):
    
    resutls = BaseDataUser.delete_user_station(db,
                                     Member,
                                     id)
    resutls_update = BaseRepo.update(db,resutls)
    return ResponseSchema(
         code="200", status="Ok", message="Deleted Success"
     ).dict(exclude_none=True)
    
    

            


            


        

      