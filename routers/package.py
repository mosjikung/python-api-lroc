from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse
from typing import List , Optional
from schema import (
    RequestSchema,
    ResponseSchema,

)
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from respository.web_repository import JWTRepo, JWTBearer,Ex_Decode
from passlib.context import CryptContext
from respository.repo_package import BaseRepo

from model import (
     Users , 
     Sta_station ,
     Stat_customer,
     Sta_station_schedule,
     Stat_customer_action_detail,
     Stat_customer_interest,
     Sta_station_period,
     Sta_channel,
     Sta_package_detail,
     Sta_package_group
    
     )
from datetime import datetime, timedelta
import pdb
from minio_handler import MinioHandler
from minio import Minio
import logging


router = APIRouter(
              prefix="",
              tags=['package'],
              responses ={404:{
                            'message' : "Not found"
              }}
              
)


logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# กำหนด handler เพื่อกำหนดที่จะเขียน log ไปที่ไฟล์
file_handler = logging.FileHandler("app.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

@router.get("/get-detail-package-web")
async def get_detail_package_web(lang: str = Header(None),db: Session = Depends(get_db)):
                try:
                        if lang is None:
                                lang = "th"
                
                        get_data_package = BaseRepo.get_data_package(db,
                                                                Sta_package_group,
                                                                Sta_package_detail,)
                        if get_data_package is None:
                                return ResponseSchema(
                                code="200", status="Ok", message="canNotFoundData"
                                ).dict(exclude_none=True)
                        else:
                                results = []
                                if lang == "th":
                                        for sta_package_groups , sta_package_details in get_data_package:
                                                results.append({
                                                        'package_group_id':sta_package_groups.id,
                                                        'package_group_name':sta_package_groups.name,
                                                        'package_group_detail':sta_package_groups.detail_th,
                                                        'package_detail_id':sta_package_details.id,
                                                        'package_detail_name':sta_package_details.name_th,
                                                        'package_group_footer':sta_package_groups.detail_footer_th,
                                                        'package_detail_sort':sta_package_details.sort
                                                })
                                elif lang == "en":
                                        for sta_package_groups , sta_package_details in get_data_package:
                                                results.append({
                                                        'package_group_id':sta_package_groups.id,
                                                        'package_group_name':sta_package_groups.name,
                                                        'package_group_detail':sta_package_groups.detail_en,
                                                        'package_detail_id':sta_package_details.id,
                                                        'package_detail_name':sta_package_details.name_en,
                                                        'package_group_footer':sta_package_groups.detail_footer_en,
                                                        'package_detail_sort':sta_package_details.sort
                                                })

                                elif lang == "lo":
                                        for sta_package_groups , sta_package_details in get_data_package:
                                                results.append({
                                                        'package_group_id':sta_package_groups.id,
                                                        'package_group_name':sta_package_groups.name,
                                                        'package_group_detail':sta_package_groups.detail_lo,
                                                        'package_detail_id':sta_package_details.id,
                                                        'package_detail_name':sta_package_details.name_lo,
                                                        'package_group_footer':sta_package_groups.detail_footer_lo,
                                                        'package_detail_sort':sta_package_details.sort
                                                })
                        

                                return ResponseSchema(
                                code="200", status="Ok", message="foundData" ,result=results
                                ).dict(exclude_none=True)
                except NameError as e:
                        logger.error(f"An error occurred: {e}", exc_info=True)
              
@router.get("/endpoint")
def read_endpoint():
    try:
        # โค้ดที่ทำงาน
        result = 1 / 0  # สร้าง error ขึ้นมา

        return {"result": result}
    except Exception as e:
        # Logging ข้อความ error
        logger.error(f"Error in endpoint /endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
              

              
