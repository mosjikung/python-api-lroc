from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile , Form
from typing import List , Optional
from schema import (
    RequestSchema,
    ResponseSchema,
    Insertstationmember,
    Insertfilemedia,
    Mainresp,
    Updatefilemedia,
    Insertfiletype,
    Updatefiletype,
    Updatestatusfilemedia
)
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from respository.repository import JWTRepo, JWTBearer, UsersRepo, BaseRepo ,Ex_Decode
from minio_handler import MinioHandler
from pydantic import  BaseModel
import mimetypes
from io import BytesIO
import os
from urllib.parse import urlparse
from model import (
     Sta_file_type_medias,
     Sta_file_medias,
     Member,
     Users
     )
from datetime import datetime, timedelta
import pdb



router = APIRouter(
              prefix="",
              tags=['File Management'],
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


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""
    Authentication Router
"""
@router.get("/get-all-list-file-media",dependencies=[Depends(JWTBearer())])
async def get_all_file_media(offset:Optional[int]=None,
                             limit:Optional[int]=None,
                             order_direction:Optional[str]=None,
                             file_type_media_id:Optional[int]=None,
                             keyword:Optional[str]=None,
                             db: Session = Depends(get_db)):
     _file_medias = UsersRepo.get_data_station_user(db, Sta_file_medias,offset,limit,order_direction,keyword,file_type_media_id)
     count_medias = UsersRepo.count_data_station_user(db,Sta_file_medias,keyword,file_type_media_id)
     results_data = []
     results_all = []
     for sta_file_medias in _file_medias:
          bucket_name = 'stations'
          if sta_file_medias.object_key is not None:
                
                object_name = sta_file_medias.object_key
                url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
          else:
                url = None
          
          find_member = BaseRepo.find_data_member(db,
                                                 Users,
                                                 sta_file_medias.created_by)
          
          if find_member is None:
               name = ''
          else:
               name = find_member.first_name

          results_data.append({
               'id':sta_file_medias.id,
               'created':sta_file_medias.created,
               'created_by':name,
               'name':sta_file_medias.name,
               'file_type_media_id':sta_file_medias.file_type_media_id,
               'file_name':sta_file_medias.file_name,
               'file_path':url,
               'file_type':sta_file_medias.file_type,
               'file_size':sta_file_medias.file_size,
               'time_duration':sta_file_medias.time_duration,
               'file_status_id':sta_file_medias.file_status_id
          })

          results_all = [{
               'count_query':count_medias,
               'data':results_data
          }]
        
     
   
     return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=results_all
    ).dict(exclude_none=True)



@router.delete("/delete-file-media",dependencies=[Depends(JWTBearer())])
async def Delete_file_media(id:Optional[int]= None ,token: str = Depends(JWTBearer()),db: Session = Depends(get_db)):
     time_update = datetime.now()
     decode_token = Ex_Decode.decode_token(token)
     user_id = decode_token["id"]
     _file_medias = BaseRepo.delete_by_id(db, Sta_file_medias,id,user_id,time_update)
     results  = BaseRepo.update(db, _file_medias)
     if results == True:
          object_name = _file_medias.object_key
          bucket_name = 'stations'
          url = MinioHandler().get_instance().delete_object(bucket_name, object_name)
     return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data").dict(exclude_none=True)




@router.put("/update-file-media",dependencies=[Depends(JWTBearer())])
async def Update_file_media(file_type_media_id: int = Form(),
                            name:str = Form(),
                            id:int = Form(),
                            token: str = Depends(JWTBearer()),
                            db: Session = Depends(get_db),
                            file: UploadFile = File(None)):
     
     time_update = datetime.now()
     decode_token = Ex_Decode.decode_token(token)
     user_id = decode_token["id"]
     
     if file is not None:
          data = file.file.read()
          bucket_name = 'stations'
          file_namex = " ".join(file.filename.strip().split())
          file_size = file.size
          mime_type, _ = mimetypes.guess_type(file.filename)
          if file_size <= 157286400:    #157286400
               data_file = MinioHandler().get_instance().fput_object_song(
               bucket_name = bucket_name,
               file_name=file_namex,
               file_data=BytesIO(data),
               content_type=file.content_type
               )
               
               url = data_file["url"]
               parsed_url = urlparse(url)
               object_key = os.path.basename(parsed_url.path)
               update_file_media = UsersRepo.update_file_media_with_key(db,
                                                       Sta_file_medias,
                                                       id,
                                                       user_id,
                                                       time_update,
                                                       name,
                                                       file_type_media_id,
                                                       object_key,
                                                       url,
                                                       file_size,
                                                       mime_type,
                                                       file_namex
                                                       )
               return ResponseSchema(
               code="200", status="Ok", message="Sucess retrieve data").dict(exclude_none=True)
          else:
               return ResponseSchema(
               code="200", status="Ok", message="canNotUploadFileIsBig").dict(exclude_none=True)

     else:

          update_file_media = UsersRepo.update_file_media(db,
                                                     Sta_file_medias,
                                                     id,
                                                     user_id,
                                                     time_update,
                                                     name,
                                                     file_type_media_id
                                                     )
          results  = BaseRepo.update(db, update_file_media)
          return ResponseSchema(
          code="200", status="Ok", message="Sucess retrieve data").dict(exclude_none=True)


@router.get("/get-all-list-file-type-media",dependencies=[Depends(JWTBearer())])
async def get_all_list_file_type_media(offset:Optional[int]=None,
                                       limit:Optional[int]=None,
                                       order_direction:Optional[str]=None,
                                       keyword:Optional[str]=None,
                                       db: Session = Depends(get_db)):
     results_all = []
     _file_medias = UsersRepo.get_all_data_list_file_type_media(db, Sta_file_type_medias , offset,limit,order_direction,keyword)
     
     for x in _file_medias:
          _count_data_medias = BaseRepo.count_data_list_media(db,
                                                              Sta_file_medias,
                                                              x.id)
          results_all.append({
               'id':x.id,
               'name':x.name,
               'description':x.description,
               'created':x.created,
               'amount':_count_data_medias
          })
     
     return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=results_all
    ).dict(exclude_none=True)

@router.post("/create-file-media",dependencies=[Depends(JWTBearer())])
async def create_file_media(file_type_media_id: int = Form(),
                            name:str = Form(),
                            time_duration:str = Form(),
                            token: str = Depends(JWTBearer()),
                            db: Session = Depends(get_db),
                            file: UploadFile = File(...)):
     
     
     file_size = file.size
     #file_ext = file.filename.split('.')[-1]
     mime_type, _ = mimetypes.guess_type(file.filename)

     if file_size <= 157286400:    #157286400
          data = file.file.read()
          bucket_name = 'stations'
          file_namex = " ".join(file.filename.strip().split())
          data_file = MinioHandler().get_instance().fput_object_song(
               bucket_name = bucket_name,
               file_name=file_namex,
               file_data=BytesIO(data),
               content_type=file.content_type
          )
          
          decode_token = Ex_Decode.decode_token(token)
          user_id = decode_token['id']
          file_name_send = data_file["file_name"]
          url_send = data_file["url"]
          time_update = datetime.now()
          _station_member = Sta_file_medias(
                         created=time_update,
                         created_by=user_id,
                         name=name,
                         file_type_media_id =file_type_media_id,
                         file_name=file_namex,
                         file_path = url_send,
                         object_key= file_name_send,
                         time_duration = time_duration,
                         file_size = file_size,
                         file_type = mime_type

               )
          BaseRepo.insert(db, _station_member)

          return data_file
     else:
          return ResponseSchema(
        code="200", status="Ok", message="canNotUploadFileIsBig").dict(exclude_none=True)

  

@router.delete("/delete-file-type-media",dependencies=[Depends(JWTBearer())])
async def delete_file_type_media(id:Optional[int]=None ,token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
     decode_token = Ex_Decode.decode_token(token)
     user_id = decode_token['id']
     update_time = datetime.now()
     _file_medias = BaseRepo.delete_by_id(db, Sta_file_type_medias,id,user_id,update_time)
    
     results  = BaseRepo.update(db, _file_medias)
     return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data").dict(exclude_none=True)


@router.put("/update-file-type-media",dependencies=[Depends(JWTBearer())])
async def update_file_type_media(request:Updatefiletype ,token: str = Depends(JWTBearer()) , db: Session = Depends(get_db)):
     time_update = datetime.now()
     decode_token = Ex_Decode.decode_token(token)
     user_id = decode_token['id']
     _file_medias = BaseRepo.update_file_type_media(db, 
                                          Sta_file_type_medias,
                                          request.id,
                                          time_update,
                                          user_id,
                                          request.name,
                                          request.description)
    
     results  = BaseRepo.update(db, _file_medias)
     return ResponseSchema(
        code="200", status="Ok", message="Update Data Success").dict(exclude_none=True)
         

@router.post("/create-file-type-media",dependencies=[Depends(JWTBearer())])
async def create_file_type_media(request:Insertfiletype,token: str = Depends(JWTBearer()),db: Session = Depends(get_db)):
     decode_token = Ex_Decode.decode_token(token)
     user_id = decode_token['id']
     time_update = datetime.now()
     is_deleted = False
     file_type_media = Sta_file_type_medias(
                    is_deleted=is_deleted,
                    created=time_update,
                    created_by=user_id,
                    name=request.name,
                    description=request.description
            )
     results  = BaseRepo.insert(db, file_type_media)
     return ResponseSchema(
        code="200", status="Ok", message="Sucess Create data").dict(exclude_none=True)


@router.patch("/update-status-file-media",dependencies=[Depends(JWTBearer())])
async def Update_status_file_media(request:Updatestatusfilemedia,token: str = Depends(JWTBearer()),db: Session = Depends(get_db)):
     time_update = datetime.now()
     decode_token = Ex_Decode.decode_token(token)
     user_id = decode_token["id"]

     update_file_media = UsersRepo.update_file_status_media(db,
                                                     Sta_file_medias,
                                                     user_id,
                                                     request.file_status_id,
                                                     request.id,
                                                     time_update,
                                                     )
     results  = BaseRepo.update(db, update_file_media)
     
     return ResponseSchema(
        code="200", status="Ok", message="Update Data Success").dict(exclude_none=True)


