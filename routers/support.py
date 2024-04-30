from fastapi import APIRouter, Depends ,HTTPException , Header
from fastapi.responses import JSONResponse
from typing import List , Optional
from schema import (
    RequestSchema,
    ResponseSchema,
    UploadFileResponse,
    Insertmessagegroup

)
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from config import MAIL_USERNAME,MAIL_PASSWORD,MAIL_FROM2,MAIL_PORT,MAIL_SERVER,MAIL_FROM_NAME
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from respository.repo_support import BaseRepo
from passlib.context import CryptContext
from respository.repo_support import BaseRepo
from respository.web_repository import JWTRepo,JWTBearer,Ex_Decode
from fastapi import File, UploadFile , Form

from model import (
              Sta_help_type,
              Sta_report_type,
              Sta_request,
              Customer,
              Countries,
              Sta_message_groups,
              Sta_message,
              Sta_message_files,
              Sta_support_groups,
              Sta_support_detail
    
     )
from datetime import datetime, timedelta
import pdb
from minio_handler import MinioHandler
from minio import Minio
import mimetypes
from io import BytesIO
from pathlib import Path
import os
from urllib.parse import urlparse



router = APIRouter(
              prefix="",
              tags=['support'],
              responses ={404:{
                            'message' : "Not found"
              }}
              
)

from dotenv import load_dotenv
load_dotenv('.env')

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



@router.get("/get-all-help-type-web")
async def get_all_help_type_web(db: Session = Depends(get_db)):
 
              get_data_help = BaseRepo.get_all_data_help( db,
                                                   Sta_help_type)
              results = []
              for sta_help_types in get_data_help:
                            results.append({
                            'id':sta_help_types.id,
                            'name':sta_help_types.name
                            })

              return ResponseSchema(
                            code="200", status="Ok", message="foundData" ,result=results
                            ).dict(exclude_none=True)



@router.get("/get-all-report-type-web")
async def get_all_report_type_web(lang: str = Header(None), db: Session = Depends(get_db)):
        
              get_data_help = BaseRepo.get_all_data_help( db,
                                                   Sta_report_type)
              results = []
              if lang  is None:
                      lang = "th"

              for sta_help_types in get_data_help:
                                if lang == "th":
                                        results.append({
                                        'id':sta_help_types.id,
                                        'name':sta_help_types.name_th
                                        })
                                elif lang == "en":
                                        results.append({
                                        'id':sta_help_types.id,
                                        'name':sta_help_types.name_en
                                        })
                                elif lang == "lo":
                                        results.append({
                                        'id':sta_help_types.id,
                                        'name':sta_help_types.name_lo
                                        })
                        

              return ResponseSchema(
                            code="200", status="Ok", message="foundData" ,result=results
                            ).dict(exclude_none=True)

@router.get("/get-ticket-id-request-web")
async def get_all_ticket_id_web(db: Session = Depends(get_db)):
              get_data_ticket_id = BaseRepo.get_data_ticket_id(db,
                                                               Sta_request)
              
              results = []

              for sta_requests in get_data_ticket_id:
                      results.append({
                              'ticket_id':sta_requests.ticket_id
                      })

              return ResponseSchema(
                            code="200", status="Ok", message="foundData" ,result=results
                            ).dict(exclude_none=True)


@router.get("/get-all-country-web")
async def get_all_country_web(lang: str = Header(None),db: Session = Depends(get_db)):
                get_data_country = BaseRepo.get_data_all_country(db,
                                                                Countries)
                if lang is None:
                        lang = "th"

                
                results = []
                for Country in get_data_country:
                        if lang == "th":
                                results.append({
                                        'id':Country.id,
                                        'name':Country.name_th
                                })
                        elif lang == "en":
                                results.append({
                                        'id':Country.id,
                                        'name':Country.name_en
                                })
                        elif lang == "lo":
                                results.append({
                                        'id':Country.id,
                                        'name':Country.name_lo
                                })


                return ResponseSchema(
                                code="200", status="Ok", message="foundData" ,result=results
                                ).dict(exclude_none=True)


@router.post("/insert-request-web",dependencies=[Depends(JWTBearer())])
async def insert_request_web(
                             help_type_id:int = Form(None),
                             report_type_id:int = Form(None),
                             country_id:int = Form(None),
                             email:str = Form(None),
                             link:str = Form(None),
                             description:str = Form(None),
                             file: UploadFile = File(None),
                             token: str = Depends(JWTBearer()),            
                             db: Session = Depends(get_db)):
              
                update_time = datetime.now()
                decode_token = Ex_Decode.decode_token(token)
                user_id = decode_token["id"]

                check_found_email = BaseRepo.check_email_data(db,
                                                         Customer,
                                                         email)
                
                if check_found_email is not None:
                        status_check_in = True
                else:
                        status_check_in = False

                if file is not None:
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
                                
                                if status_check_in == True:
                                        insert_data = Sta_request(
                                        is_deleted = False,
                                        help_type_id = help_type_id,
                                        report_type_id = report_type_id,
                                        country_id = country_id,
                                        email = email,
                                        link = link,
                                        description = description,
                                        created = update_time,
                                        created_by = user_id,
                                        modified = None,
                                        modified_by = None,
                                        object_key = object_key,
                                        file_name = file_namex,
                                        file_path = url,
                                        file_type = mime_type,
                                        file_size = file_size,
                                        )
                                        
                                        results_insert = BaseRepo.insert(db,insert_data)
                                        if results_insert == True:
                                                new_id = insert_data.id
                                                formatted_date = update_time.strftime("%Y%m%d")
                                                formatted_date_mail = update_time.strftime("%Y-%m-%d %H:%M")
                                                new_id = insert_data.id
                                                request_id = insert_data.id
                                                today = f"CAS-"+formatted_date+str(new_id)
                                                prepare_update = BaseRepo.prepare_update(db,
                                                                                        Sta_request,
                                                                                        today,
                                                                                        new_id)
                                                results_update = BaseRepo.update(db,prepare_update)
                                                check_data_user = BaseRepo.check_data_user(db,
                                                                                        Customer,
                                                                                        user_id
                                                                                        )
                                                
                                                emails = check_data_user.email

                                                main_value = [emails]
                                                value2 = dict({"case_id":today,"date":formatted_date_mail})
                                                message = MessageSchema(
                                                subject="แจ้งปัญหา",
                                                recipients=main_value,
                                                template_body=value2,
                                                subtype=MessageType.html,
                                                sender=("LRNOC", "Team@nrc.com")
                                                )
                                                fm = FastMail(conf)
                                                await fm.send_message(message, template_name="email_send_request.html")
                                else:
                                        return ResponseSchema(
                code="200", status="Ok", message="emailNotFound" 
                ).dict(exclude_none=True)

                                
                                        
                
                else:
                                if status_check_in == True:
                                        insert_data = Sta_request(
                                        is_deleted = False,
                                        help_type_id = help_type_id,
                                        report_type_id = report_type_id,
                                        country_id = country_id,
                                        email = email,
                                        link = link,
                                        description = description,
                                        created = update_time,
                                        created_by = user_id,
                                        modified = None,
                                        modified_by = None,
                                        object_key = None,
                                        file_name = None,
                                        file_path = None,
                                        file_type = None,
                                        file_size = None,
                                        )
                                        results_insert = BaseRepo.insert(db,insert_data)
                                        if results_insert == True:
                                        
                                                formatted_date = update_time.strftime("%Y%m%d")
                                                formatted_date_mail = update_time.strftime("%Y-%m-%d %H:%M")
                                                new_id = insert_data.id
                                                request_id = insert_data.id
                                                today = f"CAS-"+formatted_date+str(new_id)

                                                
                                                
                                                prepare_update = BaseRepo.prepare_update(db,
                                                                                        Sta_request,
                                                                                        today,
                                                                                        new_id)
                                                results_update = BaseRepo.update(db,prepare_update)
                                                
                                                
                                                check_data_user = BaseRepo.check_data_user(db,
                                                                                        Customer,
                                                                                        user_id)
                                                
                                                

                                                emails = check_data_user.email

                                                main_value = [emails]
                                                value2 = dict({"case_id":today,"date":formatted_date_mail})
                                                message = MessageSchema(
                                                subject="แจ้งปัญหา",
                                                recipients=main_value,
                                                template_body=value2,
                                                subtype=MessageType.html,
                                                sender=("LRNOC", "Team@nrc.com")
                                                )
                                                fm = FastMail(conf)
                                                await fm.send_message(message, template_name="email_send_request.html")
                                else:
                                        return ResponseSchema(
                code="200", status="Ok", message="emailNotFound" 
                ).dict(exclude_none=True)
                                
                #---------------------------------------------------------------------------------------------
                
                if file is not None:
                                is_attach_file = True
                else:
                                is_attach_file = False
                        
                select_next_value = BaseRepo.get_next_value_data_message(db,
                                                                        Sta_message_groups,
                                                                        Sta_request,
                                                                        Sta_help_type,
                                                                        request_id)
                id_next_value = select_next_value[0]
                created_by = select_next_value[1]
                ticket_id = select_next_value[2]
                request_id = select_next_value[3]
                help_type_name = select_next_value[4]
                #try:
                insert_data = Sta_message_groups(
                                                        id = id_next_value,
                                                        is_deleted = False,
                                                        created = update_time,
                                                        created_by = created_by,
                                                        modified = None,
                                                        modified_by = None,
                                                        station_id = None,
                                                        channel_id = None,
                                                        name = 'ส่งคำขอ',
                                                        description =help_type_name,
                                                        form_member_id = None,
                                                        receive_member_id = None,
                                                        message_type_id = 1,
                                                        message_status_id = 2,
                                                        object = None,
                                                        reference_id = None,
                                                        message_mode = 'w-g',
                                                        is_attach_file = is_attach_file,
                                                        form_customer_id = created_by,
                                                        ticket_id = ticket_id,
                                                        request_id = request_id
                                                        )
                        
                results_insert = BaseRepo.insert(db,insert_data)

                message_group_id = insert_data.id

                select_next_value2 = BaseRepo.get_next_value_data_message_2(db,
                                                                                Sta_message_groups,
                                                                                Sta_request,
                                                                                Sta_help_type,
                                                                                Sta_report_type,
                                                                                Countries,
                                                                                message_group_id)
                        
                date_time = select_next_value2[10].strftime('%Y-%m-%d %H:%M:%S')
                insert_data2  = Sta_message(
                                id = select_next_value2[0],
                                is_deleted = False,
                                created  = update_time,
                                created_by = select_next_value2[11],
                                modified = None,
                                modified_by = None,
                                message_group_id = select_next_value2[1],
                                name = 'ส่งคำขอ',
                                description = (
                                        'เลขที่ : ' + str(select_next_value2[2]) + '\n' +
                                        'เรื่อง : ' + str(select_next_value2[3]) + '\n' +
                                        'อีเมล : ' + str(select_next_value2[4]) + '\n' +
                                        'ประเทศ : ' + str(select_next_value2[5]) + '\n' +
                                        'ฉันต้องการรายงาน : ' + str(select_next_value2[6]) + '\n' +
                                        'โปรไฟล์ของผู้ใช้ที่รายงาน : ' + str(select_next_value2[7]) + '\n' +
                                        'รายละเอียดเพิ่มเติม : ' + str(select_next_value2[8]) + '\n' 
                                        ),
                                reply_message_id = None,
                                type_user = 'customers'
                        )
                results_insert = BaseRepo.insert(db,insert_data2)
                message_id = select_next_value2[0]
                request_id = select_next_value2[12]
                
                if file is not None:
                                find_next_value_request_id = BaseRepo.find_next_value_request_id(db,
                                                                                                Sta_message_groups,
                                                                                                Sta_message,
                                                                                                Sta_request,
                                                                                                request_id,
                                                                                                message_id)
                                
                                insert_data = Sta_message_files(
                                id = find_next_value_request_id[0],
                                is_deleted = False,
                                created_by = user_id,
                                created = update_time,
                                modified = None,
                                modified_by = None,
                                message_id = message_id,
                                object_key = find_next_value_request_id[7],
                                file_name = find_next_value_request_id[3],
                                file_path = find_next_value_request_id[4],
                                file_type = find_next_value_request_id[5],
                                file_size = find_next_value_request_id[6],
                                )      
                           
                                results_insert = BaseRepo.insert(db,insert_data)
                results_ticket_id={
                        'ticket_id':today
                }
                # except Exception as e:
                #         db.rollback()
                #         raise HTTPException(status_code=500, detail="dataError")
                if results_insert == True:
                        return ResponseSchema(
                code="200", status="Ok", message="insertDataSucessfull" ,result=results_ticket_id
                ).dict(exclude_none=True)


@router.get("/get-support-group")
async def get_support_groups(lang: str = Header(None),keyword:Optional[str]=None,db: Session = Depends(get_db)):
        get_data_support_group = BaseRepo.get_data_support_group(db,
                                                                 Sta_support_groups,
                                                                 keyword)
       
        
        if lang is None:
                lang = "th"

        if get_data_support_group == []:
                return ResponseSchema(
                code="200", status="Ok", message="canNotFoundData"
                ).dict(exclude_none=True)
        
        results = []
        for support_groups in get_data_support_group:
                if lang == "th":
                        results.append({
                                'id':support_groups.id,
                                'topic':support_groups.topic_th,
                                'description':support_groups.description_th
                        })
                elif lang == "en":
                        results.append({
                                'id':support_groups.id,
                                'topic':support_groups.topic_en,
                                'description':support_groups.description_en
                        })

                elif lang == "lo":
                         results.append({
                                'id':support_groups.id,
                                'topic':support_groups.topic_lo,
                                'description':support_groups.description_lo
                        })
                         
        return ResponseSchema(
                code="200", status="Ok", message="canFoundData" ,result=results
                ).dict(exclude_none=True)


@router.get("/get-support-detail")
async def get_support_detail(lang: str = Header(None),support_group_id:Optional[int]=None,db: Session = Depends(get_db)):
        if lang is None:
                lang = "th"
      
        get_all_detail = BaseRepo.get_data_support_detail_by_id(db,
                                                                Sta_support_detail,
                                                                support_group_id)
        if get_all_detail is None:
                return ResponseSchema(
                code="200", status="Ok", message="canNotFoundData"
                ).dict(exclude_none=True)
        else:
                results = []
                for support_detail in get_all_detail:
                        if lang == "th":
                                results.append({
                                        'id':support_detail.id,
                                        'topic':support_detail.topic_th,
                                        'description':support_detail.description_th,
                                        'link':support_detail.link
                                })
                        elif lang == "en":
                                results.append({
                                        'id':support_detail.id,
                                        'topic':support_detail.topic_en,
                                        'description':support_detail.description_en,
                                        'link':support_detail.link
                                })

                        elif lang == "lo":
                                results.append({
                                        'id':support_detail.id,
                                        'topic':support_detail.topic_lo,
                                        'description':support_detail.description_lo,
                                        'link':support_detail.link
                                })

                return ResponseSchema(
                code="200", status="Ok", message="canFoundData" ,result=results
                ).dict(exclude_none=True)
        

@router.get("/get-support-detail-list")
async def get_support_detail_list(lang: str = Header(None),parent_id:Optional[int]=None,db: Session = Depends(get_db)):
        if lang is None:
                lang = "th"
      
        get_all_detail = BaseRepo.get_data_support_detail_parent_by_id(db,
                                                                Sta_support_detail,
                                                                parent_id)
        if get_all_detail is None:
                return ResponseSchema(
                code="200", status="Ok", message="canNotFoundData"
                ).dict(exclude_none=True)
        else:
                results = []
                for support_detail in get_all_detail:
                        if lang == "th":
                                results.append({
                                        'id':support_detail.id,
                                        'topic':support_detail.topic_th,
                                        'description':support_detail.description_th
                                })
                        elif lang == "en":
                                results.append({
                                        'id':support_detail.id,
                                        'topic':support_detail.topic_en,
                                        'description':support_detail.description_en
                                })

                        elif lang == "lo":
                                results.append({
                                        'id':support_detail.id,
                                        'topic':support_detail.topic_lo,
                                        'description':support_detail.description_lo
                                })

                return ResponseSchema(
                code="200", status="Ok", message="canFoundData" ,result=results
                ).dict(exclude_none=True)
        
@router.get("/get-support-detail-list-by-id")
async def get_support_detail_list(lang: str = Header(None),id:Optional[int]=None,db: Session = Depends(get_db)):
        if lang is None:
                lang = "th"
      
        get_all_detail = BaseRepo.get_data_support_detail_list_by_id(db,
                                                                Sta_support_detail,
                                                                id)
        if get_all_detail is None:
                return ResponseSchema(
                code="200", status="Ok", message="canNotFoundData"
                ).dict(exclude_none=True)
        else:
                results = []
                for support_detail in get_all_detail:
                        if lang == "th":
                                results.append({
                                        'id':support_detail.id,
                                        'topic':support_detail.topic_th,
                                        'description':support_detail.description_th,
                                        'link':support_detail.link
                                })
                        elif lang == "en":
                                results.append({
                                        'id':support_detail.id,
                                        'topic':support_detail.topic_en,
                                        'description':support_detail.description_en,
                                        'link':support_detail.link
                                })

                        elif lang == "lo":
                                results.append({
                                        'id':support_detail.id,
                                        'topic':support_detail.topic_lo,
                                        'description':support_detail.description_lo,
                                        'link':support_detail.link
                                })

                return ResponseSchema(
                code="200", status="Ok", message="canFoundData" ,result=results
                ).dict(exclude_none=True)
        




        




    


    
    
