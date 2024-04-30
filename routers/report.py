from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List , Optional
from schema import (
    RequestSchema,
    ResponseSchema,
    Createscheduletype,
    Updatescheduletype
)
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from respository.repository import JWTRepo, JWTBearer, UsersRepo, BaseRepo ,Ex_Decode
from respository.repo_report import BaseRepo
from model import (Sta_schedule_catagorie,
                   Stat_customer_detail,
                   Stat_customer_action_detail
                   )
from datetime import datetime, timedelta ,date
import pdb


router = APIRouter(
              prefix="",
              tags=['Report'],
              responses ={404:{
                            'message' : "Not found"
              }}
              
)

# encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@router.get("/get-all-report-top",dependencies=[Depends(JWTBearer())])
async def get_all_report_top(id:Optional[int]=None,
                                      db: Session = Depends(get_db)):
    results = BaseRepo.get_all_data_report_1(db,Stat_customer_action_detail,id)

    results2 = BaseRepo.get_all_data_report_2(db,Stat_customer_action_detail,id)

    results3 = BaseRepo.get_all_data_report_3(db,Stat_customer_action_detail,id)

    results4 = BaseRepo.get_all_data_report_4(db,Stat_customer_action_detail,id)
    
    last_results = {
        'day':results,
        '7days':results2,
        'month':results3,
        'last_month':results4

    }
    

    return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=last_results
    )


@router.get("/get-all-report-by-date",dependencies=[Depends(JWTBearer())])
async def get_all_report_bottom(date_start:Optional[str]=None,
                                date_end:Optional[str]=None,
                                type:Optional[str]=None,
                                id:Optional[int]=None,
                                db: Session = Depends(get_db)):
    results = BaseRepo.get_all_data_report(db,Stat_customer_action_detail,date_start,date_end,type,id)
    if type == 'day':
        last_results=[]
        
        for action , total  in results:
            last_results.append({
                'action_date':action,
                'TOTAL':total
            })
            
        return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=last_results
    )
    elif type == 'month':
        last_results = []
        for month , year , TOTAL in results:
            last_results.append({
                'month':month,
                'year':year,
                'TOTAL':TOTAL
            })

        return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data", result=last_results
    )


    
    
    
    

    





