from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile , Form
from typing import List , Optional
from schema import (
    RequestSchema,
    ResponseSchema,
    TokenResponse,
    UserSigupSchema,
    UserSiginSchema,
    UploadFileResponse,
    CustomException,
    Createmessages,
    Updatemessagestatus,
    Createmessagenone
    
)

from io import BytesIO
from pydantic import BaseModel
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from config import MAIL_USERNAME,MAIL_PASSWORD,MAIL_FROM2,MAIL_PORT,MAIL_SERVER,MAIL_FROM_NAME

from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from respository.repo_message import BaseRepo
from fastapi import File, UploadFile
from respository.repository import JWTRepo, JWTBearer, UsersRepo ,Ex_Decode

from model import (
     Member,
     Sta_message,
     Sta_message_files,
     Sta_message_groups,
     Sta_message_statuses,
     Sta_message_type,
     Users,
     Customer
     

     )
from datetime import datetime, timedelta
import pdb
from minio import Minio
from minio_handler import MinioHandler
import mimetypes
from pathlib import Path
from io import BytesIO
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv('.env')



router = APIRouter(
              prefix="",
              tags=['message'],
              responses ={404:{
                            'message' : "Not found"
              }}
              
)

class UploadFileResponse(BaseModel):
    bucket_name: str
    file_name: str
    url: str	




class CustomException(Exception):
    http_code: int
    code: str
    message: str

    def __init__(self, http_code: int = None, code: str = None, message: str = None):
        self.http_code = http_code if http_code else 500
        self.code = code if code else str(self.http_code)
        self.message = message



class Envs:
    MAIL_USERNAME = MAIL_USERNAME
    MAIL_PASSWORD = MAIL_PASSWORD
    MAIL_FROM = MAIL_FROM2
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

@router.get("/get-all-message",dependencies=[Depends(JWTBearer())])
async def get_all_message(offset:Optional[int]=None,
                                         limit:Optional[int]=None,
                                         type:Optional[str]=None,
                                         order_direction:Optional[str]=None,
                                         keyword:Optional[str]=None,
                                         db: Session = Depends(get_db)):
              #decode_token = Ex_Decode.decode_token(token)
              #user_id = decode_token['id']
              results_message = BaseRepo.get_all_message(db,
                                                         Sta_message,
                                                         Member,
                                                         offset,
                                                         limit,
                                                         type,
                                                         order_direction,
                                                         keyword,
                                                         #user_id
              )
              
              result_list = []
              
              for sta_messages , members in results_message:
               result_people = BaseRepo.search_name(db,
                                                    Member,
                                                    members.id
                                                    )
              
               result_list.append({
                    'id':sta_messages.id,
                    'name':sta_messages.name,
                    'description':sta_messages.description,
                    'message_type_id':sta_messages.message_type_id,
                    'file_name':sta_messages.file_name,
                    'file_path':sta_messages.file_path,
                    'file_type':sta_messages.file_type,
                    'file_size':sta_messages.file_size,
                    'tag_color':sta_messages.tag_color,
                    'created':sta_messages.created,
                    'modified':sta_messages.modified,
                    'file':'Example',
                    'from':result_people.first_name,
                    'to':members.first_name
                    

                 })
               
               return ResponseSchema(
                 code="200", status="Ok", message="Success save data" , result=result_list
                ).dict(exclude_none=True)
              
@router.get("/get-file-message",dependencies=[Depends(JWTBearer())])
async def get_all_message(id:Optional[int]=None,db: Session = Depends(get_db)):
        results_search_message = BaseRepo.search_data_message(db,
                                                              Sta_message,
                                                              Member,
                                                              id)
        
        result_list = []
        for sta_messages , members in results_message:
               result_people = BaseRepo.search_name(db,
                                                    Member,
                                                    members.id
                                                    )
               result_list.append({
                    'id':sta_messages.id,
                    'name':sta_messages.name,
                    'description':sta_messages.description,
                    'message_type_id':sta_messages.message_type_id,
                    'file_name':sta_messages.file_name,
                    'file_path':sta_messages.file_path,
                    'file_type':sta_messages.file_type,
                    'file_size':sta_messages.file_size,
                    'tag_color':sta_messages.tag_color,
                    'created':sta_messages.created,
                    'modified':sta_messages.modified,
                    'file':'Example',
                    'from':result_people.first_name,
                    'to':members.first_name
                    

                 })

        return ResponseSchema(
                 code="200", status="Ok", message="Success save data" , result=result_list
                ).dict(exclude_none=True)

#dependencies=[Depends(JWTBearer())]
#token:str = Depends(JWTBearer()),
@router.post("/create-all_message",dependencies=[Depends(JWTBearer())])
async def create_message(file: UploadFile = File(None),
                         name:Optional[str]=None,
                         description:Optional[str]=None,
                         type_send:Optional[str]=None,
                         type_message:Optional[str]=None,
                         db: Session = Depends(get_db)):
        #decode_token = Ex_Decode.decode_token(token)
        #username = decode_token["id"] ###JWT
        test_id = 1
        update_time = datetime.now()
        ##minio)
        if file is not None:
                bucket_name = 'message'
                data = file.file.read()
                file_name = " ".join(file.filename.strip().split())
                data_file = MinioHandler().get_instance().put_object(
                bucket_name=bucket_name,
                file_name=file_name,
                file_data=BytesIO(data),
                content_type=file.content_type
                )
                file_name_send = data_file["file_name"]
                url_send = data_file["url"]
                return data_file
        else:
                 
                 return ("Not File Found")
        

        
        
        

# @router.post("/reply-message",dependencies=[Depends(JWTBearer())])
# async def reply_message(db: Session = Depends(get_db)):
#         pass

# @router.delete("/delete-message",dependencies=[Depends(JWTBearer())])
# async def delete_message(id:Optional[int]=None,db: Session = Depends(get_db)):
#         delete_message = BaseRepo.delete_item(db,Sta_message,id)

#         result = BaseRepo.update(db, delete_message)
#         return ResponseSchema(
#                  code="200", status="Ok", message="Delete_Success"
#                 ).dict(exclude_none=True)









# @router.get("/get-message-type",dependencies=[Depends(JWTBearer())]) #click to see detail on message
# async def get_message_type(id:Optional[int]=None,db: Session = Depends(get_db)):
#         results_search_message_type = BaseRepo.search_data_message_type(db,
#                                                               Sta_message,
#                                                               Member,
#                                                               id)
        
#         result_list = []
#         for sta_messages , members in results_search_message_type:
#                result_people = BaseRepo.search_name(db,
#                                                     Member,
#                                                     members.id
#                                                     )
#                result_list.append({
#                     'id':sta_messages.id,
#                     'name':sta_messages.name,
#                     'description':sta_messages.description,
#                     'message_type_id':sta_messages.message_type_id,
#                     'file_name':sta_messages.file_name,
#                     'file_path':sta_messages.file_path,
#                     'file_type':sta_messages.file_type,
#                     'file_size':sta_messages.file_size,
#                     'tag_color':sta_messages.tag_color,
#                     'created':sta_messages.created,
#                     'modified':sta_messages.modified,
#                     'file':'Example',
#                     'from':result_people.first_name,
#                     'to':members.first_name
                    

#                  })

#         return ResponseSchema(
#                  code="200", status="Ok", message="Success save data" , result=result_list
#                 ).dict(exclude_none=True)


@router.post("/create-message-type",dependencies=[Depends(JWTBearer())])
async def create_message(db: Session = Depends(get_db)):
        pass


@router.delete("/delete-message-type",dependencies=[Depends(JWTBearer())])
async def delete_message(id:Optional[int]=None,db: Session = Depends(get_db)):
        delete_message = BaseRepo.delete_item(db,Sta_message,id)

        result = BaseRepo.update(db, delete_message)
        return ResponseSchema(
                 code="200", status="Ok", message="Delete_Success"
                ).dict(exclude_none=True)


@router.get("/get-message-all-deleted",dependencies=[Depends(JWTBearer())])
async def get_message_delete(offset:Optional[int]=None , limit:Optional[int]=None , keyword:Optional[str]=None, db: Session = Depends(get_db)):


        get_delete_message_all = BaseRepo.get_delete_message_all(db,
                                                                 Sta_message_groups,
                                                                 offset,
                                                                 limit)
        
        
        results_all = []
        for sta_message_groups in get_delete_message_all:
               if sta_message_groups.message_mode == 'c-g' or sta_message_groups.message_mode == 's-g':
                        
                        get_delete_message = BaseRepo.get_delete_message(db,
                                                                        Sta_message_groups,
                                                                        Member,
                                                                        Sta_message_type,
                                                                        keyword,
                                                                        sta_message_groups.id
                                                                )
                        
                        
                        for sta_message_groups , members, sta_message_types in get_delete_message:
                                
                                results_all.append({
                                        'id':sta_message_groups.id,
                                        'username':members.username,
                                        'avatar_img':members.avatar_img,
                                        'name':sta_message_groups.name,
                                        'name_type':sta_message_types.name,
                                        'created':sta_message_groups.created,
                                        'message_mode':sta_message_groups.message_mode,
                                        'email':members.email_verify,
                                        'is_attach_file':sta_message_groups.is_attach_file,
                                        'is_read':sta_message_groups.is_read,
                                        'type_id':sta_message_groups.message_type_id,
                                        'is_attach_file':sta_message_groups.is_attach_file
                                })
                                


                        
               
               elif sta_message_groups.message_mode == 'w-g':
                       
                        get_delete_message= BaseRepo.get_delete_message_web(db,
                                                                        Sta_message_groups,
                                                                        Customer,
                                                                        Sta_message_type,
                                                                        keyword,
                                                                        sta_message_groups.id
                                                                )
                        
                        
                        for sta_message_groups , customers, sta_message_types in get_delete_message:
                              
                               
                                results_all.append({
                                        'id':sta_message_groups.id,
                                        'username':customers.email,
                                        'avatar_img':customers.avatar_img,
                                        'name':sta_message_groups.name,
                                        'name_type':sta_message_types.name,
                                        'created':sta_message_groups.created,
                                        'message_mode':sta_message_groups.message_mode,
                                        'email':customers.email,
                                        'is_attach_file':sta_message_groups.is_attach_file,
                                        'cus_case_id':sta_message_groups.ticket_id,
                                        'is_read':sta_message_groups.is_read,
                                        'type_id':sta_message_groups.message_type_id,
                                        'is_attach_file':sta_message_groups.is_attach_file
                                })

                        
  
        return ResponseSchema(
                 code="200", status="Ok", message="Delete_Success",result=results_all
                ).dict(exclude_none=True)
@router.get("/get-message-group-by-status",dependencies=[Depends(JWTBearer())])
async def get_message_delete_by_status(offset:Optional[int]=None , limit:Optional[int]=None , keyword:Optional[str]=None, db: Session = Depends(get_db)):

        get_delete_message_all = BaseRepo.get_message_by_status(db,
                                                                 Sta_message_groups,
                                                                 offset,
                                                                 limit)
        
        results_all = []
        
        results = []
        for sta_message_groups in get_delete_message_all:
                
                results_all.append({
                        'id':sta_message_groups.id,
                        'name':sta_message_groups.name,
                        'message_mode':sta_message_groups.message_mode
                })
                if sta_message_groups.message_mode == 'c-g' or sta_message_groups.message_mode == 's-g':
                        
        
                        get_delete_message = BaseRepo.get_message_group_by_status(db,
                                                                        Sta_message_groups,
                                                                        Member,
                                                                        Sta_message_type,
                                                                        keyword,
                                                                        sta_message_groups.id
                                                                )
                        
                        for sta_message_groups , members, sta_message_types in get_delete_message:
                                
                                results.append({
                                        'id':sta_message_groups.id,
                                        'username':members.username,
                                        'avatar_img':members.avatar_img,
                                        'name':sta_message_groups.name,
                                        'name_type':sta_message_types.name,
                                        'created':sta_message_groups.created,
                                        'is_read':sta_message_groups.is_read,
                                        'type_id':sta_message_groups.message_type_id,
                                        'is_attach_file':sta_message_groups.is_attach_file,
                                        'message_mode':sta_message_groups.message_mode,
                                })
                        
                        

                elif sta_message_groups.message_mode == 'w-g':
                       
                        get_delete_message = BaseRepo.get_message_group_by_status_web(db,
                                                                        Sta_message_groups,
                                                                        Customer,
                                                                        Sta_message_type,
                                                                        keyword,
                                                                        sta_message_groups.id
                                                                )
                        
                        for sta_message_groups , customers, sta_message_types in get_delete_message:
                                
                                results.append({
                                        'id':sta_message_groups.id,
                                        'username':customers.email,
                                        'avatar_img':customers.avatar_img,
                                        'name':sta_message_groups.name,
                                        'name_type':sta_message_types.name,
                                        'created':sta_message_groups.created,
                                        'is_read':sta_message_groups.is_read,
                                        'type_id':sta_message_groups.message_type_id,
                                        'is_attach_file':sta_message_groups.is_attach_file,
                                        'message_mode':sta_message_groups.message_mode,
                                })
                       

        
        return ResponseSchema(
                 code="200", status="Ok", message="Delete_Success" , result=results
                ).dict(exclude_none=True)


@router.post("/create-message",dependencies=[Depends(JWTBearer())])
async def get_message_delete_by_status(message_group_id:int = Form(),
                                       description:str = Form(),
                                       reply_message_id:int = Form(None),
                                       message_mode:str = Form(None),
                                       files: List[UploadFile] = File([]),
                                       token: str = Depends(JWTBearer()),
                                       db: Session = Depends(get_db),
                                       ):
        
        update_time = datetime.now()
        decode_token = Ex_Decode.decode_token(token)
        user_id = decode_token["id"]
        
        if files is not None:
             for file in files:
                data = file.file.read()
                bucket_name = 'messages'
                file_namex = " ".join(file.filename.strip().split())
                file_size = file.size
                mime_type, _ = mimetypes.guess_type(file.filename)

                data_file = MinioHandler().get_instance().put_object(
                bucket_name = bucket_name,
                file_name=file_namex,
                file_data=BytesIO(data),
                content_type=file.content_type
                )
                print(mime_type)
                url = data_file["url"]
                parsed_url = urlparse(url)
                object_key = os.path.basename(parsed_url.path)

                
                
        
        if message_mode ==  'w-g':
                insert_data = Sta_message(
                                                is_deleted = False,
                                                message_group_id = message_group_id,
                                                description = description,
                                                reply_message_id = reply_message_id,
                                                created  = update_time,
                                                created_by = user_id,
                                                type_user = 'users'
                                                )
                

                results_upload = BaseRepo.insert(db, insert_data)
                if results_upload == True:

                                check_form_customer_id = BaseRepo.find_customer_id_from_sta_message_groups(db,
                                                                               Sta_message_groups,
                                                                               Customer,
                                                                               Sta_message,
                                                                               Sta_message_files,
                                                                               message_group_id
                                                                               )
                               
                                email = check_form_customer_id[1].email
                                case_id = check_form_customer_id[0].ticket_id
                                description_old = check_form_customer_id[2].description
                                lines = description_old.split('\n') 
                                html_content = "<html><body>"
                                for line in lines:
                                        parts = line.split(' : ')
                                        if len(parts) == 2:
                                                key, value = parts
                                                key = key.strip() 
                                                value = value.strip() 
                                        
                                                html_content += f"<p><strong>{key}:</strong> {value}</p>"
                                        
                                        # Close the HTML tags
                                html_content += "</body></html>"                   
                                emails = email
                                
                                if check_form_customer_id[3] is not None:
                                        link_file = check_form_customer_id[3].file_path
                                        main_value = [emails]
                                        value2 = dict({"case_id":case_id,"description_old":html_content,"description":description,"picture":link_file,"user_picture":url})
                                        message = MessageSchema(
                                        subject="แจ้งปัญหา",
                                        recipients=main_value,
                                        template_body=value2,
                                        subtype=MessageType.html,
                                        sender=("LRNOC", "Team@nrc.com")
                                        )
                                        fm = FastMail(conf)
                                        await fm.send_message(message, template_name="email_feedback_picture.html")
                                        
                                else:
                                        main_value = [emails]
                                        value2 = dict({"case_id":case_id,"description_old":html_content,"description":description,"user_picture":url})
                                        message = MessageSchema(
                                        subject="แจ้งปัญหา",
                                        recipients=main_value,
                                        template_body=value2,
                                        subtype=MessageType.html,
                                        sender=("LRNOC", "Team@nrc.com")
                                        )
                                        fm = FastMail(conf)
                                        await fm.send_message(message, template_name="email_feedback.html")
        else:
                insert_data = Sta_message( 
                                                is_deleted = False,
                                                message_group_id = message_group_id,
                                                description = description,
                                                reply_message_id = reply_message_id,
                                                created  = update_time,
                                                created_by = user_id,
                                                type_user = 'users'
                                                )
               
                results_upload = BaseRepo.insert(db, insert_data)
        if results_upload == True:
                find_message_id = BaseRepo.find_message_id(db,
                                                           Sta_message,
                                                           user_id,
                                                           message_group_id)
               

                insert_data_upload = Sta_message_files(
                                                is_deleted = False,
                                                created = update_time,
                                                created_by = user_id,
                                                message_id = find_message_id.id,
                                                file_name = file_namex,
                                                file_path = url,
                                                file_type = mime_type,
                                                file_size = file_size,
                                                object_key = object_key
                                                )


                results_message_file_upload =   BaseRepo.insert(db, insert_data_upload)

                if results_message_file_upload is True:
                        check_attach_file = BaseRepo.check_att_file(db,
                                                                   Sta_message_groups,
                                                                   message_group_id,
                                                                   user_id,
                                                                   update_time)
                        update_is_att = BaseRepo.update(db,check_attach_file)


        if results_upload == True and  results_message_file_upload == True and update_is_att == True:

                return ResponseSchema(
                 code="200", status="Ok", message="Insert Data Success"
                ).dict(exclude_none=True)
        else:
               return ResponseSchema(
                 code="200", status="Ok", message="Insert Data failed"
                ).dict(exclude_none=True)
        

@router.post("/create-message-none",dependencies=[Depends(JWTBearer())])
async def get_message_delete_by_status(request:Createmessagenone,
                                       token: str = Depends(JWTBearer()),
                                       db: Session = Depends(get_db),
                                       ):
        
        update_time = datetime.now()
        decode_token = Ex_Decode.decode_token(token)
        user_id = decode_token["id"]
        
        if request.message_mode ==  'w-g':
                insert_data = Sta_message( 
                                                is_deleted = False,
                                                message_group_id = request.message_group_id,
                                                description = request.description,
                                                reply_message_id = request.reply_message_id,
                                                created  = update_time,
                                                created_by = user_id,
                                                type_user = 'users'
                                                )

                results_upload = BaseRepo.insert(db, insert_data)

                if results_upload == True:
                                check_form_customer_id = BaseRepo.find_customer_id_from_sta_message_groups(db,
                                                                               Sta_message_groups,
                                                                               Customer,
                                                                               Sta_message,
                                                                               Sta_message_files,
                                                                               request.message_group_id
                                                                               )
                                email = check_form_customer_id[1].email
                                case_id = check_form_customer_id[0].ticket_id
                                description_old = check_form_customer_id[2].description
                                lines = description_old.split('\n')
                                html_content = "<html><body>"  
                                for line in lines:
                                        parts = line.split(' : ')
                                        if len(parts) == 2:
                                                key, value = parts
                                                key = key.strip() 
                                                value = value.strip() 
                                        
                                                html_content += f"<p><strong>{key}:</strong> {value}</p>"

                                     
                                html_content += "</body></html>"                     
                                emails = email
                                
                                if check_form_customer_id[3] is not None:
                                        link_file = check_form_customer_id[3].file_path
                                        main_value = [emails]
                                        value2 = dict({"case_id":case_id,"description_old":html_content,"description":request.description,"picture":link_file})
                                        message = MessageSchema(
                                        subject="แจ้งปัญหา",
                                        recipients=main_value,
                                        template_body=value2,
                                        subtype=MessageType.html,
                                        sender=("LRNOC", "Team@nrc.com")
                                        )
                                        fm = FastMail(conf)
                                        await fm.send_message(message, template_name="email_feedback_picture.html")
                                        
                                else:
                                        main_value = [emails]
                                        value2 = dict({"case_id":case_id,"description_old":html_content,"description":request.description})
                                        message = MessageSchema(
                                        subject="แจ้งปัญหา",
                                        recipients=main_value,
                                        template_body=value2,
                                        subtype=MessageType.html,
                                        sender=("LRNOC", "Team@nrc.com")
                                        )
                                        fm = FastMail(conf)
                                        await fm.send_message(message, template_name="email_feedback.html")

        else:
               
                insert_data = Sta_message( 
                                                is_deleted = False,
                                                message_group_id = request.message_group_id,
                                                description = request.description,
                                                reply_message_id = request.reply_message_id,
                                                created  = update_time,
                                                created_by = user_id,
                                                type_user = 'customer'
                                                )

                results_upload = BaseRepo.insert(db, insert_data)
               

        if results_upload == True:

                return ResponseSchema(
                 code="200", status="Ok", message="insertDataSuccess"
                ).dict(exclude_none=True)
        else:
                return ResponseSchema(
                 code="200", status="Ok", message="insertDataFailed"
                ).dict(exclude_none=True)
        

@router.get("/get-all-message-by-id",dependencies=[Depends(JWTBearer())])
async def get_all_message_by_id(id:Optional[int]=None,db: Session = Depends(get_db)):   
        results_data = BaseRepo.message_by_id(db,
                                             Sta_message_groups,
                                             Sta_message,
                                             Sta_message_files,
                                             id)
        
        
        results = []
        for sta_message_groups,sta_messages  in results_data:
            
            if sta_messages.created_by is not None and sta_messages.type_user is not None:
                
                if sta_messages.type_user == 'members':
                        results_users = BaseRepo.search_users(db,
                                                             Member,
                                                             sta_messages.created_by)
                elif sta_messages.type_user == 'users':
                        results_users = BaseRepo.search_users(db,
                                                             Users,
                                                             sta_messages.created_by)
                        
                elif sta_messages.type_user == 'customers':
                        results_users = BaseRepo.search_users(db,
                                                             Customer,
                                                             sta_messages.created_by)
                
               
                
                find_data_message_file = BaseRepo.find_message_file(db,
                                                                    Sta_message_files,
                                                                    sta_messages.id)
                
                
                
                if find_data_message_file != []:
   
                        
                        data_file = []
                        for x in find_data_message_file:
                                
                                data_file.append({
                                                'id':x.id,
                                                'file_name':x.file_name,
                                                'file_path':x.file_path,
                                                'file_type':x.file_type,
                                                'file_size':x.file_size
                                })
                else:
                        data_file = []
                        for x in find_data_message_file:
                                data_file.append({
                                                'id':None,
                                                'file_name':None,
                                                'file_path':None,
                                                'file_type':None,
                                                'file_size':None
                                })

                if sta_messages.type_user == 'members':
                        results.append({
                                        'id':sta_message_groups.id,
                                        'id_message':sta_messages.id,
                                        'name':sta_messages.name,
                                        'created':sta_messages.created,
                                        'description':sta_messages.description,
                                        'type_user':sta_messages.type_user,
                                        'created_by':sta_messages.created_by,
                                        'username':results_users.username,
                                        'email_verify':results_users.email_verify,
                                        'avatar_img':results_users.avatar_img,
                                        'message_status_id':sta_message_groups.message_status_id,
                                        'message_type_id':sta_message_groups.message_type_id,
                                        'message_mode':sta_message_groups.message_mode,
                                        'file':data_file
                                        
                                        
                                })
                elif sta_messages.type_user == 'users':
                        results.append({
                                        'id':sta_message_groups.id,
                                        'id_message':sta_messages.id,
                                        'name':sta_messages.name,
                                        'created':sta_messages.created,
                                        'description':sta_messages.description,
                                        'type_user':sta_messages.type_user,
                                        'created_by':sta_messages.created_by,
                                        'username':results_users.username,
                                        'email_verify':results_users.username,
                                        'avatar_img':results_users.avatar_img,
                                        'message_status_id':sta_message_groups.message_status_id,
                                        'message_type_id':sta_message_groups.message_type_id,
                                        'message_mode':sta_message_groups.message_mode,
                                        'file':data_file
                                        
                                })
                        
                elif sta_messages.type_user == 'customers':
                        results.append({
                                        'id':sta_message_groups.id,
                                        'id_message':sta_messages.id,
                                        'name':sta_messages.name,
                                        'created':sta_messages.created,
                                        'description':sta_messages.description,
                                        'type_user':sta_messages.type_user,
                                        'created_by':sta_messages.created_by,
                                        'username':results_users.username,
                                        'avatar_img':results_users.avatar_img,
                                        'email_verify':results_users.email,
                                        'message_status_id':sta_message_groups.message_status_id,
                                        'message_type_id':sta_message_groups.message_type_id,
                                        'message_mode':sta_message_groups.message_mode,
                                        'file':data_file
                                        
                                })
                
        if results_data != []:
                        
                        update_message_group = BaseRepo.update_message_group_status(db,
                                                                                    Sta_message_groups,
                                                                                    id)
                        
                        results_update_message_group = BaseRepo.update(db,update_message_group)
                        if results_update_message_group == False:
                                return ResponseSchema(
                                        code="200", status="Ok", message="updateFailed",
                                        ).dict(exclude_none=True)
        else:
                return ResponseSchema(
                        code="200", status="Ok", message="dataNotFound", result=results
                        ).dict(exclude_none=True)      

        return ResponseSchema(
                        code="200", status="Ok", message="dataFound", result=results
                        ).dict(exclude_none=True)
                
               
                


@router.post("/update-message-status-for-trash",dependencies=[Depends(JWTBearer())])
async def update_message_status_for_trash(request:Updatemessagestatus,token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
        update_time = datetime.now()
        decode_token = Ex_Decode.decode_token(token)
        user_id = decode_token["id"]
        data = BaseRepo.update_message_trash(db,
                                            Sta_message_groups,
                                            request.id,
                                            update_time,
                                            user_id)
       
       
        results_update = BaseRepo.update(db,data)
        return ResponseSchema(
                 code="200", status="Ok", message="Update Success"
                ).dict(exclude_none=True)



@router.post("/delete-message-group",dependencies=[Depends(JWTBearer())])
async def delete_message_group(request:Updatemessagestatus,token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
        update_time = datetime.now()
        decode_token = Ex_Decode.decode_token(token)
        user_id = decode_token["id"]
        data = BaseRepo.update_message_group(db,
                                            Sta_message_groups,
                                            request.id,
                                            update_time,
                                            user_id)
       
        results_update = BaseRepo.update(db,data)
        return ResponseSchema(
                 code="200", status="Ok", message="Update Success"
                ).dict(exclude_none=True)

@router.get("/count-message-group",dependencies=[Depends(JWTBearer())])
async def count_message_group(type:Optional[str] = None,db: Session = Depends(get_db)):
        get_count_data  = BaseRepo.count_message_group(db,
                                                       Sta_message_groups,
                                                       type)
        
        
        
        
        return ResponseSchema(
                 code="200", status="Ok", message="Update Success",result=get_count_data
                ).dict(exclude_none=True)

@router.post("/update-message-group-status-id",dependencies=[Depends(JWTBearer())])
async def update_message_group_status_id(request:Updatemessagestatus,token: str = Depends(JWTBearer()),db: Session = Depends(get_db)):
        decode_token = Ex_Decode.decode_token(token)
        user_id = decode_token["id"]
        update_time = datetime.now()
        get_data_prepare_update = BaseRepo.get_data_message_group(db,
                                                                  Sta_message_groups,
                                                                  request.id,
                                                                  user_id,
                                                                  update_time)
        
        
        if get_data_prepare_update is not None:
                results_update = BaseRepo.update(db,get_data_prepare_update)
                if results_update == True:
                        return ResponseSchema(
                        code="200", status="Ok", message="updateSuccess"
                        ).dict(exclude_none=True)
        else:
                return ResponseSchema(
                 code="200", status="Ok", message="notFoundData"
                ).dict(exclude_none=True)









        





