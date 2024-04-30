from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List , Optional
from schema import (
    RequestSchema,
    ResponseSchema,
    TokenResponse,
    UserSigupSchema,
    UserSiginSchema,
    Updatestationstatus,
    Updatestatusregis
)
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from respository.repository import JWTRepo, JWTBearer, UsersRepo, BaseRepo ,Ex_Decode
from minio_handler import MinioHandler
from model import (
     Users ,
     Sta_station , 
     Sta_station_schedule,
     Member,
     Sta_station_activities,
     Sta_station_playlist,
     Sta_station_period,
     Sta_station_member,
     Sta_channel_member,
     Sta_station_statuses,
     Sta_approve_statuses,
     Sta_process_statuses,
     Sta_broadcast_statuses,
     Sta_period_status,
     Sta_categories,
     Sta_channel,
     Sta_broadcast,
     Countries,
     Sta_station_schedule_activitie
     )
from datetime import datetime, timedelta
import pdb
from sqlalchemy.exc import SQLAlchemyError



router = APIRouter(
              prefix="",
              tags=['Station'],
              responses ={404:{
                            'message' : "Not found"
              }}
              
)


# encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""
    Authentication Router
"""




"""
    Users Router
"""




@router.patch("/update-station-schedule")
async def update_station_schedule( station_schedule_id:int ,
                                   type : str ,
                                   process_status_id : Optional[int] = None ,
                                   db: Session = Depends(get_db)):
 
    update_status = BaseRepo.update_status_station( db,Sta_station_schedule,station_schedule_id,process_status_id,type)
    update_check = BaseRepo.update(db,update_status)
    if update_status is None:
        return ResponseSchema(
        code="200", status="Ok", message="Data not Found"
            ).dict(exclude_none=True)
    else:
        return ResponseSchema(
        code="200", status="Ok", message="Sucess retrieve data"
            ).dict(exclude_none=True)
    
    
@router.patch("/set-station-status",dependencies=[Depends(JWTBearer())])
async def update_station_status(request:Updatestationstatus,
                                token: str = Depends(JWTBearer()),
                                db: Session = Depends(get_db)):
    decode_token = Ex_Decode.decode_token(token)
    user_id = decode_token["id"]
    update_time = datetime.now()
    if request.suspend_date_start == 'string':
        request.suspend_date_start = None
    if request.suspend_date_end == 'string':
        request.suspend_date_end = None
    if request.suspend_comment == 'string' and request.suspend_date_start is not None and request.suspend_date_end is not None:
        request.suspend_comment = ''
    elif request.suspend_comment == 'string' and request.suspend_date_start is None and request.suspend_date_end is  None:
        request.suspend_comment = None
    if request.disable_comment == 'string':
        request.disable_comment = None
    
    
    if request.suspend_date_start is not None and request.suspend_date_end is not None:
        convert_date_suspend_start = datetime.strptime(request.suspend_date_start, '%Y-%m-%d')
        convert_date_suspend_end = datetime.strptime(request.suspend_date_end, '%Y-%m-%d')
    if request.suspend_date_start is None and request.suspend_date_end is None and request.suspend_comment is None and request.disable_comment is None and request.station_status_id == 3:
        update_deleted = BaseRepo.update_status_delete(db,
                                                Sta_station,
                                                request.id,
                                                user_id,
                                                request.station_status_id,
                                                update_time)
        
        try:
                results_update_deleted = BaseRepo.update(db,update_deleted)
        except Exception as e:
                results_update_deleted= db.rollback()

        if results_update_deleted == True:
                     insert_deleted = Sta_station_activities(
                            is_deleted=False,
                            created=update_time,
                            created_by=user_id,
                            name='ลบสถานี',
                            description='ลบสถานี',
                            status_id=request.station_status_id,
                            station_id = request.id,
                            reference_id = request.id
                    )
                     results_insert = BaseRepo.insert(db,insert_deleted)

        find_data_schedule = BaseRepo.find_schedule(db,
                                                                Sta_station_schedule,
                                                                request.id)  
        if find_data_schedule is not None:
                for x in find_data_schedule:
                                            update_delete_schedule = BaseRepo.check_station_schedule(db,
                                                            Sta_station_schedule,
                                                            x.id,
                                                            user_id,
                                                            update_time)
                                            
                                            
                                            try:
                                                results_update_delete_schedule = BaseRepo.update(db,update_delete_schedule)
                                            
                                                    
                                            except Exception as e:
                                                results_update_delete_schedule = db.rollback()


                                            if results_update_delete_schedule == True:
                                                    insert_delete_suchedule = Sta_station_schedule_activitie(
                                                            is_deleted = False,
                                                            created=update_time,
                                                            created_by=user_id,
                                                            name="ลบผังรายการ",
                                                            description="รายการ" + ' ' + str(x.name),
                                                            station_schedule_id = x.id,
                                                            reference_id = x.id,
                                                            object = "station_schedules",
                                                            icon = "icon-clock.svg",
                                                            type_user = "users"
                        
                                                    )
                                                    results_insert = BaseRepo.insert(db,insert_delete_suchedule)
                                            

                                            find_data_period = BaseRepo.find_period(db,
                                                                                    Sta_station_period,
                                                                                    x.id)
                                            
                                            
                                            if find_data_period is not None:
                                                for y in find_data_period:
                                                        update_delete_period = BaseRepo.check_period_4(db,
                                                                    Sta_station_period,
                                                                    y.id,
                                                                    user_id,
                                                                    update_time)
                                                        
                                                        try:
                                                            results_update_delete_period = BaseRepo.update(db,update_delete_period)
                                                            
                                                        except Exception as e:
                                                            results_update_delete_period = db.rollback()


                                                        if results_update_delete_period == True:
                                                                insert_delete_period = Sta_station_schedule_activitie(
                                                                    is_deleted = False,
                                                                    created=update_time,
                                                                    created_by=user_id,
                                                                    name="ลบผังย่อยรายการ",
                                                                    description="รายการ" + ' ' + str(y.name),
                                                                    station_schedule_id = x.id,
                                                                    reference_id = y.id,
                                                                    object = "station_periods",
                                                                    icon = "icon-clock.svg",
                                                                    type_user = "users"
                                                        )
                                                                results_insert = BaseRepo.insert(db,insert_delete_period)
        
    elif request.suspend_date_start is None and request.suspend_date_end is None and request.suspend_comment is None and request.disable_comment is None and request.station_status_id == 1:
        print("----------------------------------------------1-----------------------------------------------------")
        current_time = datetime.now()
        date = current_time.strftime("%Y-%m-%d")
        time = current_time.strftime("%H:%M:%S")

        check_status_station_status_id = BaseRepo.check_status_station(db,
                                                                       Sta_station,
                                                                       request.id)
        old_status = check_status_station_status_id.station_status_id

        update_use = BaseRepo.update_status_use(db,
                                                Sta_station,
                                                request.id,
                                                user_id,
                                                request.station_status_id,
                                                update_time)
        
        try:
                results_update = BaseRepo.update(db,update_use)
        except Exception as e:
                results_update = db.rollback()

        

        if results_update == True:
                     insert_suspend = Sta_station_activities(
                            is_deleted=False,
                            created=update_time,
                            created_by=user_id,
                            name='เปิดใช้งานสถานี',
                            description='เปิดใช้งานสถานี',
                            status_id=request.station_status_id,
                            station_id = request.id,
                            reference_id = request.id
                    )
                     results_insert = BaseRepo.insert(db,insert_suspend)

        
        
        if old_status == 4 or old_status == 2 or old_status == 3:
            
      
                #check หา status ว่าของเดิมคืออะไร
            check_data_schedule = BaseRepo.find_schedule(db,
                                                        Sta_station_schedule,
                                                        request.id,
                                                        )
            
            
                    
            
            for x in check_data_schedule:
                if x.schedule_time_start is not None:
                    #string
                    date_data = x.schedule_date.strftime("%Y-%m-%d")
                    time_data_start= x.schedule_time_start.strftime("%H:%M:%S")
                    time_data_end= x.schedule_time_end.strftime("%H:%M:%S")

                    date_from_data = x.schedule_date
                    time_start = x.schedule_time_start
                    time_end = x.schedule_time_end
                    datetime_start = datetime.combine(date_from_data,time_start)
                    datetime_end = datetime.combine(date_from_data, time_end)

                    
                

                    different_time_start_end =  datetime_end - datetime_start
                    diff_time_start_end = different_time_start_end.total_seconds()/60 #เวลา duration schedule นั้นๆ
                    
                    different_time_schedule =   current_time - datetime_start
                    diff_time = different_time_schedule.total_seconds()/60 #เวลาที่เหลือของ schedule นั้นๆ
                
                    
                    check_data_period = BaseRepo.find_period(db,
                                                            Sta_station_period,
                                                            x.id,
                                                            )
                    list_array = []
                    for y in check_data_period:
                        
                        
                        date_from_data = x.schedule_date
                        time_start = y.period_time_start
                        time_end = y.period_time_end
                        datetime_start = datetime.combine(date_from_data,time_start)
                        datetime_end = datetime.combine(date_from_data, time_end)
                        
                        different_time_start_end =  datetime_end - datetime_start
                        diff_time_start_end = different_time_start_end.total_seconds()/60 #เวลา duration schedule นั้นๆ
                    
                        different_time_schedule =    datetime_end - current_time
                        diff_time = different_time_schedule.total_seconds()/60 #เวลาที่เหลือของ schedule นั้นๆ

                       
                        if date < date_data:
                                broadcast_status_id = 3
                                update_resume_period = BaseRepo.update_resume_period(db,
                                                                                    Sta_station_period,
                                                                                    y.id,
                                                                                    user_id,
                                                                                    current_time,
                                                                                    broadcast_status_id)
                                
                                list_array.append(broadcast_status_id)
                                try:
                                    results_update = BaseRepo.update(db,update_resume_period)
                                except Exception as e:
                                    results_update = db.rollback()

                                if results_update == True:
                                    insert_suspend = Sta_station_schedule_activitie(
                                                            is_deleted = False,
                                                            created=update_time,
                                                            created_by=user_id,
                                                            name="รอออกอากาศ",
                                                            description="รายการ" + ' ' + str(y.name),
                                                            reference_id = y.id,
                                                            station_schedule_id = x.id,
                                                            object = "station_periods",
                                                            icon = "icon-clock.svg",
                                                            type_user = "users"
                        
                        
                                                    )
                                results_insert = BaseRepo.insert(db,insert_suspend)
                        else:     
                            if time_data_start <= time <= time_data_end and diff_time > diff_time_start_end:
                                    broadcast_status_id = 3
                                    update_resume_period = BaseRepo.update_resume_period(db,
                                                                                        Sta_station_period,
                                                                                        y.id,
                                                                                        user_id,
                                                                                        current_time,
                                                                                        broadcast_status_id)
                                    
                                    list_array.append(broadcast_status_id)
                                    try:
                                        results_update = BaseRepo.update(db,update_resume_period)
                                    except Exception as e:
                                        results_update = db.rollback()

                                    if results_update == True:
                                        insert_suspend = Sta_station_schedule_activitie(
                                                                is_deleted = False,
                                                                created=update_time,
                                                                created_by=user_id,
                                                                name="รอออกอากาศ",
                                                                description="รายการ" + ' ' + str(y.name),
                                                                reference_id = y.id,
                                                                station_schedule_id = x.id,
                                                                object = "station_periods",
                                                                icon = "icon-clock.svg",
                                                                type_user = "users"
                            
                            
                                                        )
                                    results_insert = BaseRepo.insert(db,insert_suspend)
                            elif time_data_start <= time <= time_data_end and diff_time <= diff_time_start_end:
                                    broadcast_status_id = 4
                                    update_resume_period = BaseRepo.update_resume_period(db,
                                                                                        Sta_station_period,
                                                                                        y.id,
                                                                                        user_id,
                                                                                        current_time,
                                                                                        broadcast_status_id)
                                    list_array.append(broadcast_status_id)
                                    try:
                                        results_update = BaseRepo.update(db,update_resume_period)
                                    except Exception as e:
                                        results_update = db.rollback()

                                    if update_resume_period == True:
                                        insert_suspend = Sta_station_schedule_activitie(
                                                                is_deleted = False,
                                                                created=update_time,
                                                                created_by=user_id,
                                                                name="หยุดออกอากาศ",
                                                                description="รายการ" + ' ' + str(y.name),
                                                                reference_id = y.id,
                                                                station_schedule_id = x.id,
                                                                object = "station_periods",
                                                                icon = "icon-clock.svg",
                                                                type_user = "users"
                            
                                                                
                            
                                                        )
                                        results_insert = BaseRepo.insert(db,insert_suspend)
                            else:
                                    broadcast_status_id = 7
                                    update_resume_period = BaseRepo.update_resume_period(db,
                                                                                        Sta_station_period,
                                                                                        y.id,
                                                                                        user_id,
                                                                                        current_time,
                                                                                        broadcast_status_id)
                                    
                                    list_array.append(broadcast_status_id)
                                    try:
                                        results_update = BaseRepo.update(db,update_resume_period)
                                    except Exception as e:
                                        results_update = db.rollback()
                                    if results_update == True:
                                        insert_suspend = Sta_station_schedule_activitie(
                                                                is_deleted = False,
                                                                created=update_time,
                                                                created_by=user_id,
                                                                name="ออกอากาศแล้ว",
                                                                description="รายการ" + ' ' +  str(y.name),
                                                                reference_id = y.id,
                                                                station_schedule_id = x.id,
                                                                object = "station_periods",
                                                                icon = "icon-clock.svg",
                                                                type_user = "users"
                            
                                                        )
                                        results_insert = BaseRepo.insert(db,insert_suspend)
                    
                    if 3 in list_array:
                        broadcast_status_id = 3
                        update_resume_schdule = BaseRepo.update_resume_shchedule_special(db,
                                                                                    Sta_station_schedule,
                                                                                    x.id,
                                                                                    user_id,
                                                                                    current_time,
                                                                                    broadcast_status_id)
                        try:
                                results_update = BaseRepo.update(db,update_resume_schdule)
                        except Exception as e:
                                results_update = db.rollback()

                        if results_update == True:
                                insert_suspend = Sta_station_schedule_activitie(
                                                            is_deleted = False,
                                                            created=update_time,
                                                            created_by=user_id,
                                                            name="รอออกอากาศ",
                                                            description="รายการ" + ' ' + str(x.name),
                                                            reference_id = x.id,
                                                            station_schedule_id = x.id,
                                                            object = "station_schedules",
                                                            icon = "icon-clock.svg",
                                                            type_user = "users"
                        
                                                    )
                                results_insert = BaseRepo.insert(db,insert_suspend) 
                
                
                
                    else:
                        broadcast_status_id = 7
                        update_resume_schdule = BaseRepo.update_resume_shchedule(db,
                                                                                    Sta_station_schedule,
                                                                                    x.id,
                                                                                    user_id,
                                                                                    current_time,
                                                                                    broadcast_status_id)
                        try:
                                results_update = BaseRepo.update(db,update_resume_schdule)
                        except Exception as e:
                                results_update = db.rollback()

                        if results_update == True:
                                insert_suspend = Sta_station_schedule_activitie(
                                                            is_deleted = False,
                                                            created=update_time,
                                                            created_by=user_id,
                                                            name="ออกอากาศแล้ว",
                                                            description="รายการ" + ' ' + str(x.name),
                                                            reference_id = x.id,
                                                            station_schedule_id = x.id,
                                                            object = "station_schedules",
                                                            icon = "icon-clock.svg",
                                                            type_user = "users"
                        
                                                    )
                                results_insert = BaseRepo.insert(db,insert_suspend) 
                        
                
                



        elif old_status == 5:
            
      
                #check หา status ว่าของเดิมคืออะไร
            check_data_schedule = BaseRepo.find_schedule(db,
                                                        Sta_station_schedule,
                                                        request.id,
                                                        )
                    
            
            for x in check_data_schedule:
                if x.schedule_time_start is not None:
                    #string
                    date_data = x.schedule_date.strftime("%Y-%m-%d")
                    time_data_start= x.schedule_time_start.strftime("%H:%M:%S")
                    time_data_end= x.schedule_time_end.strftime("%H:%M:%S")

                    date_from_data = x.schedule_date
                    time_start = x.schedule_time_start
                    time_end = x.schedule_time_end
                    datetime_start = datetime.combine(date_from_data,time_start)
                    datetime_end = datetime.combine(date_from_data, time_end)

                    
                

                    different_time_start_end =  datetime_end - datetime_start
                    diff_time_start_end = different_time_start_end.total_seconds()/60 #เวลา duration schedule นั้นๆ
                    
                    different_time_schedule =   current_time - datetime_start
                    diff_time = different_time_schedule.total_seconds()/60 #เวลาที่เหลือของ schedule นั้นๆ
                
                    
                    check_data_period = BaseRepo.find_period(db,
                                                            Sta_station_period,
                                                            x.id,
                                                            )
                    list_array = []
                    for y in check_data_period:
                        

                        date_from_data = x.schedule_date
                        time_start = y.period_time_start
                        time_end = y.period_time_end
                        datetime_start = datetime.combine(date_from_data,time_start)
                        datetime_end = datetime.combine(date_from_data, time_end)
                        
                        different_time_start_end =  datetime_end - datetime_start
                        diff_time_start_end = different_time_start_end.total_seconds()/60 #เวลา duration schedule นั้นๆ
                    
                        different_time_schedule =    datetime_end - current_time
                        diff_time = different_time_schedule.total_seconds()/60 #เวลาที่เหลือของ schedule นั้นๆ

                        
                        
                        if time_data_start <= time <= time_data_end and diff_time > diff_time_start_end:
                                broadcast_status_id = 3
                                update_resume_period = BaseRepo.update_resume_period(db,
                                                                                    Sta_station_period,
                                                                                    y.id,
                                                                                    user_id,
                                                                                    current_time,
                                                                                    broadcast_status_id)
                                
                                list_array.append(broadcast_status_id)
                                try:
                                    results_update = BaseRepo.update(db,update_resume_period)
                                except Exception as e:
                                    results_update = db.rollback()

                                if results_update == True:
                                    insert_suspend = Sta_station_schedule_activitie(
                                                            is_deleted = False,
                                                            created=update_time,
                                                            created_by=user_id,
                                                            name="รอออกอากาศ",
                                                            description="รายการ" + ' ' + str(y.name),
                                                            reference_id = y.id,
                                                            station_schedule_id = x.id,
                                                            object = "station_periods",
                                                            icon = "icon-clock.svg",
                                                            type_user = "users"
                        
                                                    )
                                results_insert = BaseRepo.insert(db,insert_suspend)
                        elif time_data_start <= time <= time_data_end and diff_time <= diff_time_start_end:
                                broadcast_status_id = 6
                                update_resume_period = BaseRepo.update_resume_period(db,
                                                                                    Sta_station_period,
                                                                                    y.id,
                                                                                    user_id,
                                                                                    current_time,
                                                                                    broadcast_status_id)
                                list_array.append(broadcast_status_id)
                                try:
                                    results_update = BaseRepo.update(db,update_resume_period)
                                except Exception as e:
                                    results_update = db.rollback()

                                if update_resume_period == True:
                                    insert_suspend = Sta_station_schedule_activitie(
                                                            is_deleted = False,
                                                            created=update_time,
                                                            created_by=user_id,
                                                            name="ห้ามออกอากาศ",
                                                            description="รายการ" + ' ' + str(y.name),
                                                            reference_id = y.id,
                                                            station_schedule_id = x.id,
                                                            object = "station_periods",
                                                            icon = "icon-clock.svg",
                                                            type_user = "users"
                        
                                                    )
                                    results_insert = BaseRepo.insert(db,insert_suspend)
                        else:
                                broadcast_status_id = 7
                                update_resume_period = BaseRepo.update_resume_period(db,
                                                                                    Sta_station_period,
                                                                                    y.id,
                                                                                    user_id,
                                                                                    current_time,
                                                                                    broadcast_status_id)
                                
                                list_array.append(broadcast_status_id)
                                try:
                                    results_update = BaseRepo.update(db,update_resume_period)
                                except Exception as e:
                                    results_update = db.rollback()
                                if results_update == True:
                                    insert_suspend = Sta_station_schedule_activitie(
                                                            is_deleted = False,
                                                            created=update_time,
                                                            created_by=user_id,
                                                            name="ออกอากาศแล้ว",
                                                            description="รายการ" + ' ' + str(y.name),
                                                            reference_id = y.id,
                                                            station_schedule_id = x.id,
                                                            object = "station_periods",
                                                            icon = "icon-clock.svg",
                                                            type_user = "users"
                        
                                                    )
                                    results_insert = BaseRepo.insert(db,insert_suspend)
                    
                    if 3 in list_array:
                        broadcast_status_id = 3
                        update_resume_schdule = BaseRepo.update_resume_shchedule_special(db,
                                                                                    Sta_station_schedule,
                                                                                    x.id,
                                                                                    user_id,
                                                                                    current_time,
                                                                                    broadcast_status_id)
                        try:
                                results_update = BaseRepo.update(db,update_resume_schdule)
                        except Exception as e:
                                results_update = db.rollback()

                        if results_update == True:
                                insert_suspend = Sta_station_schedule_activitie(
                                                            is_deleted = False,
                                                            created=update_time,
                                                            created_by=user_id,
                                                            name="รอออกอากาศ",
                                                            description="รายการ" + ' ' + str(x.name),
                                                            reference_id = x.id,
                                                            station_schedule_id = x.id,
                                                            object = "station_schedules",
                                                            icon = "icon-clock.svg",
                                                            type_user = "users" 
                        
                                                    )
                                results_insert = BaseRepo.insert(db,insert_suspend) 
                
                
                
                    else:
                        broadcast_status_id = 7
                        update_resume_schdule = BaseRepo.update_resume_shchedule(db,
                                                                                    Sta_station_schedule,
                                                                                    x.id,
                                                                                    user_id,
                                                                                    current_time,
                                                                                    broadcast_status_id)
                        try:
                                results_update = BaseRepo.update(db,update_resume_schdule)
                        except Exception as e:
                                results_update = db.rollback()

                        if results_update == True:
                                insert_suspend = Sta_station_schedule_activitie(
                                                            is_deleted = False,
                                                            created=update_time,
                                                            created_by=user_id,
                                                            name="ออกอากาศแล้ว",
                                                            description="รายการ" + ' ' + str(x.name),
                                                            reference_id = x.id,
                                                            station_schedule_id = x.id,
                                                            object = "station_schedules",
                                                            icon = "icon-clock.svg",
                                                            type_user = "users"
                        
                                                    )
                                results_insert = BaseRepo.insert(db,insert_suspend)

    elif request.suspend_date_start is not None and request.suspend_date_end is not None and request.suspend_comment is not None and request.disable_comment is None and request.station_status_id == 2:
        print("2")
        update_use = BaseRepo.update_status_suspend(db,
                                     Sta_station,
                                     user_id,
                                     request.id,
                                     request.station_status_id,
                                     convert_date_suspend_start,
                                     convert_date_suspend_end,
                                     request.suspend_comment,
                                     request.disable_comment,
                                     update_time)

        try:
            results_update_use = BaseRepo.update(db,update_use)
                                                            
        except Exception as e:
            
            results_update_use = db.rollback()

        if results_update_use == True:
                                                    insert_delete_suchedule = Sta_station_activities(
                                                                                    is_deleted=False,
                                                                                    created=update_time,
                                                                                    created_by=user_id,
                                                                                    name='ระงับสถานี',
                                                                                    description='ระงับสถานี',
                                                                                    status_id=request.station_status_id,
                                                                                    station_id = request.id,
                                                                                    reference_id = request.id
                                                                            )
                                                    results_insert = BaseRepo.insert(db,insert_delete_suchedule)



        find_data_schedule = BaseRepo.find_schedule(db,
                                                                Sta_station_schedule,
                                                                request.id)
        
        
        
        if find_data_schedule is not None:
                for x in find_data_schedule:

                    
                    update_schedule = BaseRepo.update_status_suspend_schedule(db,
                                                                    Sta_station_schedule,
                                                                    user_id,
                                                                    x.id,
                                                                    update_time)
                    
                    try:
                        results_update_use = BaseRepo.update(db,update_schedule)
                                                            
                    except Exception as e:
            
                        results_update_use = db.rollback()
                    if results_update_use == True:
                                                    insert_delete_suchedule = Sta_station_schedule_activitie(
                                                            is_deleted = False,
                                                            created=update_time,
                                                            created_by=user_id,
                                                            name="ระงับการใช้งานผังรายการ",
                                                            description="รายการ" + ' ' + str(x.name),
                                                            station_schedule_id = x.id,
                                                            reference_id = x.id,
                                                            object = "station_schedules",
                                                            icon = "icon-clock.svg",
                                                            type_user = "users"
                        
                                                    )
                                                    results_insert = BaseRepo.insert(db,insert_delete_suchedule)
                    
                    find_data_period = BaseRepo.find_period(db,
                                                                                    Sta_station_period,
                                                                                    x.id)
                    
                    if find_data_period is not None:
                            for y in find_data_period:

                                update_period = BaseRepo.update_status_suspend_period(db,
                                                              Sta_station_period,
                                                              user_id,
                                                              y.id,
                                                              update_time)
        
                                
                                try:
                                    results_update_use = BaseRepo.update(db,update_period)
                                                            
                                except Exception as e:
            
                                    results_update_use = db.rollback()
                                
                                if results_update_use == True:
                                                    insert_delete_suchedule = Sta_station_schedule_activitie(
                                                            is_deleted = False,
                                                            created=update_time,
                                                            created_by=user_id,
                                                            name="ระงับการใช้งานผังย่อยรายการ",
                                                            description="รายการ" + ' ' + str(y.name),
                                                            station_schedule_id = x.id,
                                                            reference_id = y.id,
                                                            object = "station_periods",
                                                            icon = "icon-clock.svg",
                                                            type_user = "users"
                        
                                                    )
                                                    results_insert = BaseRepo.insert(db,insert_delete_suchedule)
                                

        
        
    elif request.suspend_date_start is None and request.suspend_date_end is None and request.suspend_comment is None and request.disable_comment is not None:
        print("3")
        update_close = BaseRepo.update_status_close(db,
                                     Sta_station,
                                     user_id,
                                     request.id,
                                     request.station_status_id,
                                     request.disable_comment,
                                     update_time)
        
        try:
                results_update_close = BaseRepo.update(db,update_close)
        except Exception as e:
                results_update_close = db.rollback()

        if results_update_close == True:
                     insert_close = Sta_station_activities(
                                                        is_deleted=False,
                                                        created=update_time,
                                                        created_by=user_id,
                                                        name='ปิดสถานี',
                                                        description='ปิดสถานี',
                                                        status_id=request.station_status_id,
                                                        station_id = request.id,
                                                        reference_id = request.id
                                                )
                     results_insert = BaseRepo.insert(db,insert_close)

        find_data_schedule = BaseRepo.find_schedule(db,
                                                                Sta_station_schedule,
                                                                request.id)
        if find_data_schedule is not None:
            for x in find_data_schedule:
                                            update_close_schedule = BaseRepo.check_station_schedule(db,
                                                            Sta_station_schedule,
                                                            x.id,
                                                            user_id,
                                                            update_time)
                                            
                                            
                                            try:
                                                results_update_close_close = BaseRepo.update(db,update_close_schedule)
                                            
                                                    
                                            except Exception as e:
                                                results_update_close_close = db.rollback()


                                            if results_update_close_close == True:
                                                    insert_close_suchedule = Sta_station_schedule_activitie(
                                                            is_deleted = False,
                                                            created=update_time,
                                                            created_by=user_id,
                                                            name="ปิดการใช้งานผังรายการ",
                                                            description="รายการ" + ' ' + str(x.name),
                                                            station_schedule_id = x.id,
                                                            reference_id = x.id,
                                                            object = "station_schedules",
                                                            icon = "icon-clock.svg",
                                                            type_user = "users"
                        
                                                    )
                                                    results_insert = BaseRepo.insert(db,insert_close_suchedule)

                                            find_data_period = BaseRepo.find_period(db,
                                                                                    Sta_station_period,
                                                                                    x.id)
                                            
                                            
                                            if find_data_period is not None:
                                                for y in find_data_period:
                                                        update_close_period = BaseRepo.check_period_4(db,
                                                                    Sta_station_period,
                                                                    y.id,
                                                                    user_id,
                                                                    update_time)
                                                        
                                                        try:
                                                            results_update_close_period = BaseRepo.update(db,update_close_period)
                                                            
                                                        except Exception as e:
                                                            results_update_close_period = db.rollback()


                                                        if results_update_close_period == True:
                                                                insert_close_period = Sta_station_schedule_activitie(
                                                                    is_deleted = False,
                                                                    created=update_time,
                                                                    created_by=user_id,
                                                                    name="ปิดการใช้งานผังย่อยรายการ",
                                                                    description="รายการ" + ' ' + str(y.name),
                                                                    station_schedule_id = x.id,
                                                                    reference_id = y.id,
                                                                    object = "station_periods",
                                                                    icon = "icon-clock.svg",
                                                                    type_user = "users"
                                                        )
                                                                results_insert = BaseRepo.insert(db,insert_close_period)
        
        

    return ResponseSchema(
        code="200", status="Ok", message="Update Data Success"
        ).dict(exclude_none=True)


@router.get("/get-all-list-station-register",dependencies=[Depends(JWTBearer())])
async def update_station_status(offset:Optional[int]=None,
                                limit:Optional[int]=None,
                                order_direction:Optional[str]=None,
                                keyword:Optional[str]=None,
                                type:Optional[str]=None,
                                db: Session = Depends(get_db)):
    
    results_all = []
    last_results = []
     
    count_total = BaseRepo.get_total_data(db,
                                        Sta_station,
                                        Member,
                                        Sta_station_member,
                                        Sta_station_statuses,
                                        Sta_approve_statuses,
                                        Countries)
    
 
    
    count_new = BaseRepo.get_new_data(db,
                                        Sta_station,
                                        Member,
                                        Sta_station_member,
                                        Sta_station_statuses,
                                        Sta_approve_statuses,
                                        Countries)
  
    
    count_approve = BaseRepo.get_approve_data(db,
                                        Sta_station,
                                        Member,
                                        Sta_station_member,
                                        Sta_station_statuses,
                                        Sta_approve_statuses,
                                        Countries)

    
    count_disapprove = BaseRepo.get_disapprove_data(db,
                                        Sta_station,
                                        Member,
                                        Sta_station_member,
                                        Sta_station_statuses,
                                        Sta_approve_statuses,
                                        Countries)

    results_data = BaseRepo.get_all_list_regis(db,
                                               Sta_station,
                                               Member,
                                               Sta_station_member,
                                               Sta_station_statuses,
                                               Sta_approve_statuses,
                                               Countries,
                                               offset,
                                               limit,
                                               order_direction,
                                               keyword,
                                               type,)
    
    results_count = BaseRepo.count_all_list_regis(db,
                                                    Sta_station,
                                                    Member,
                                                    Sta_station_member,
                                                    Sta_station_statuses,
                                                    Sta_approve_statuses,
                                                    Countries,
                                                    keyword,
                                                    type,)
    
    
    for sta_stations, members, sta_station_members, sta_station_statuses, sta_approve_statuses,countries in results_data:
            bucket_name = 'member'
            if members.object_key is not None:
                    
                object_name = members.object_key
                  
                url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
                  
                 
            else:
                url = None
        
            bucket_name2 = 'stations'
            if sta_stations.object_key is not None:
                    
                object_name2 = sta_stations.object_key
                  
                url2 = MinioHandler().get_instance().presigned_get_object(bucket_name2, object_name2)
                  
                 
            else:
                url2 = None
            if sta_station_members.is_owner == True:
                 role = 'เจ้าของสถานี'
            else:
                 role = 'เจ้าหน้าที่สถานี'
            results_all.append({
                'id':sta_stations.id,
                'station_name':sta_stations.name,
                'created':sta_stations.created,
                'approve_status_id':sta_stations.approve_status_id,
                'approve_description':sta_stations.approve_description,
                'station_status_id':sta_stations.station_status_id,
                'role':role,
                'station_img':url2,
                'country':countries.name,
                'member':{
                'member_id':members.id,
                'email':members.email_verify,
                'avatar_img':url,
                'first_name':members.first_name,
                'last_name':members.last_name,
                'username':members.username
                }
            })
    
    if type is None:
        last_results = [{
                'count_total':results_count,
                'count_new':count_new,
                'count_approve':count_approve,
                'count_disapprove':count_disapprove,
                'data':results_all
            }
            ]
    elif type == 'total' and keyword is not None:
        last_results = [{
                'count_total':results_count,
                'count_new':count_new,
                'count_approve':count_approve,
                'count_disapprove':count_disapprove,
                'data':results_all
            }
            ]
        
    elif type == 'new' and keyword is not None:
        last_results = [{
                'count_total':count_total,
                'count_new':results_count,
                'count_approve':count_approve,
                'count_disapprove':count_disapprove,
                'data':results_all
            }
            ]

    elif type == 'approve' and keyword is not None:
        last_results = [{
                'count_total':count_total,
                'count_new':count_new,
                'count_approve':results_count,
                'count_disapprove':count_disapprove,
                'data':results_all
            }
            ]
        
    elif type == 'disapproved' and keyword is not None:
        last_results = [{
                'count_total':count_total,
                'count_new':count_new,
                'count_approve':count_approve,
                'count_disapprove':results_count,
                'data':results_all
            }
            ]
    else:
         last_results = [{
                'count_total':count_total,
                'count_new':count_new,
                'count_approve':count_approve,
                'count_disapprove':count_disapprove,
                'data':results_all
            }
            ]
         
 

    return ResponseSchema(
        code="200", status="Ok", message="Update Data Success",result=last_results
        ).dict(exclude_none=True)


@router.patch("/update-station-approve",dependencies=[Depends(JWTBearer())])
async def update_station_status(request:Updatestatusregis,
                                token: str = Depends(JWTBearer()),
                                db: Session = Depends(get_db)):
    update_time = datetime.now()
    current_time = datetime.now()
    date = current_time.strftime("%Y-%m-%d")
    time = current_time.strftime("%H:%M:%S")
    decode_token = Ex_Decode.decode_token(token)
    user_id = decode_token["id"]
    is_deleted = False

    

    if request.approve_status_id == 1: 
        results_data = BaseRepo.update_station_regis(db,
                                                        Sta_station,
                                                        request.id,
                                                        request.approve_description,
                                                        request.approve_status_id,
                                                        user_id,
                                                        update_time)
        try:
                results_update = BaseRepo.update(db,results_data)
        except Exception as e:
                results_update = db.rollback()
        
        if results_update == True:
            update_result = BaseRepo.update(db,results_data)
            create_data = Sta_station_activities(
                            is_deleted=is_deleted,
                            created=update_time,
                            created_by=user_id,
                            name='อนุมัติ',
                            description=request.approve_description,
                            status_id=request.approve_status_id,
                            station_id = request.id,
                            reference_id = request.id
                    )

        
    elif request.approve_status_id == 2:

        results_data = BaseRepo.update_station_regis(db,
                                                        Sta_station,
                                                        request.id,
                                                        request.approve_description,
                                                        request.approve_status_id,
                                                        user_id,
                                                        update_time)
        
        try:
                results_update = BaseRepo.update(db,results_data)
        except Exception as e:
                results_update = db.rollback()
        
        if results_update == True:
            create_data = Sta_station_activities(
                            is_deleted=is_deleted,
                            created=update_time,
                            created_by=user_id,
                            name='ไม่อนุมัติ',
                            description=request.approve_description,
                            status_id=request.approve_status_id,
                            station_id = request.id,
                            reference_id = request.id
                    )
    
    elif request.approve_status_id == 5:

         results_data = BaseRepo.update_station_regis(db,
                                                        Sta_station,
                                                        request.id,
                                                        request.approve_description,
                                                        request.approve_status_id,
                                                        user_id,
                                                        update_time)
         try:
                results_update_ban = BaseRepo.update(db,results_data)
         except Exception as e:
                results_update_ban= db.rollback()

         if results_update_ban == True:
                     
                     insert_ban = Sta_station_activities(
                                                        is_deleted=False,
                                                        created=update_time,
                                                        created_by=user_id,
                                                        name='แบนสถานี',
                                                        description='สถานี' + ' ' + str(results_data.name),
                                                        status_id=request.approve_status_id,
                                                        station_id = request.id,
                                                        reference_id = request.id
                                                )
                     results_insert = BaseRepo.insert(db,insert_ban)
                
         find_data_schedule = BaseRepo.find_schedule(db,
                                                                Sta_station_schedule,
                                                                request.id)  
         if find_data_schedule is not None:
                    for x in find_data_schedule:
                                            
                                            update_delete_schedule = BaseRepo.check_station_schedule_ban(db,
                                                            Sta_station_schedule,
                                                            x.id,
                                                            user_id,
                                                            update_time)
                                            try:
                                                results_update_delete_schedule = BaseRepo.update(db,update_delete_schedule)
                                            
                                                    
                                            except Exception as e:
                                                results_update_delete_schedule = db.rollback()


                                            if results_update_delete_schedule == True:
                                                    insert_delete_suchedule = Sta_station_schedule_activitie(
                                                            is_deleted = False,
                                                            created=update_time,
                                                            created_by=user_id,
                                                            name="แบนผังรายการ",
                                                            description="รายการ" + ' ' + str(x.name),
                                                            station_schedule_id = x.id,
                                                            reference_id = x.id,
                                                            object = "station_schedules",
                                                            icon = "icon-clock.svg",
                                                            type_user = "users"
                        
                                                    )
                                                    results_insert = BaseRepo.insert(db,insert_delete_suchedule)
                                            

                                            find_data_period = BaseRepo.find_period(db,
                                                                                    Sta_station_period,
                                                                                    x.id)
                                            
                                            
                                            if find_data_period is not None:
                                                for y in find_data_period:
                                                        update_delete_period = BaseRepo.check_period(db,
                                                                    Sta_station_period,
                                                                    y.id,
                                                                    user_id,
                                                                    update_time)
                                                        
                                                        try:
                                                            results_update_delete_period = BaseRepo.update(db,update_delete_period)
                                                            
                                                        except Exception as e:
                                                            results_update_delete_period = db.rollback()


                                                        if results_update_delete_period == True:
                                                                insert_delete_period = Sta_station_schedule_activitie(
                                                                    is_deleted = False,
                                                                    created=update_time,
                                                                    created_by=user_id,
                                                                    name="แบนผังย่อยรายการ",
                                                                    description="รายการ" + ' ' + str(y.name),
                                                                    station_schedule_id = x.id,
                                                                    reference_id = y.id,
                                                                    object = "station_periods",
                                                                    icon = "icon-clock.svg",
                                                                    type_user = "users"
                                                        )
                                                                results_insert = BaseRepo.insert(db,insert_delete_period)
        
    
    
        
         
    elif request.approve_status_id == 6:
         results_data = BaseRepo.update_station_regis(db,
                                                        Sta_station,
                                                        request.id,
                                                        request.approve_description,
                                                        request.approve_status_id,
                                                        user_id,
                                                        update_time)
        
         
         update_result = BaseRepo.update(db,results_data)
         create_data = Sta_station_activities(
                        is_deleted=is_deleted,
                        created=update_time,
                        created_by=user_id,
                        name='ยกเลิกแบน',
                        description="ยกเลิกแบน" + ' ' + str(results_data.name),
                        status_id=request.approve_status_id,
                        station_id = request.id,
                        reference_id = request.id
                )
         create_results = BaseRepo.insert(db,create_data)

         check_data_schedule = BaseRepo.find_schedule(db,
                                                        Sta_station_schedule,
                                                        request.id,
                                                        )
            
            
                    
            
         for x in check_data_schedule:
                if x.schedule_time_start is not None:
                    #string
                    date_data = x.schedule_date.strftime("%Y-%m-%d")
                    time_data_start= x.schedule_time_start.strftime("%H:%M:%S")
                    time_data_end= x.schedule_time_end.strftime("%H:%M:%S")

                    date_from_data = x.schedule_date
                    time_start = x.schedule_time_start
                    time_end = x.schedule_time_end
                    datetime_start = datetime.combine(date_from_data,time_start)
                    datetime_end = datetime.combine(date_from_data, time_end)

                    
                

                    different_time_start_end =  datetime_end - datetime_start
                    diff_time_start_end = different_time_start_end.total_seconds()/60 #เวลา duration schedule นั้นๆ
                    
                    different_time_schedule =   current_time - datetime_start
                    diff_time = different_time_schedule.total_seconds()/60 #เวลาที่เหลือของ schedule นั้นๆ
                
                    
                    check_data_period = BaseRepo.find_period(db,
                                                            Sta_station_period,
                                                            x.id,
                                                            )
                    list_array = []
                    for y in check_data_period:
                        
                        
                        date_from_data = x.schedule_date
                        time_start = y.period_time_start
                        time_end = y.period_time_end
                        datetime_start = datetime.combine(date_from_data,time_start)
                        datetime_end = datetime.combine(date_from_data, time_end)
                        
                        different_time_start_end =  datetime_end - datetime_start
                        diff_time_start_end = different_time_start_end.total_seconds()/60 #เวลา duration schedule นั้นๆ
                    
                        different_time_schedule =    datetime_end - current_time
                        diff_time = different_time_schedule.total_seconds()/60 #เวลาที่เหลือของ schedule นั้นๆ

                       
                        if date < date_data:
                                broadcast_status_id = 3
                                update_resume_period = BaseRepo.update_resume_period(db,
                                                                                    Sta_station_period,
                                                                                    y.id,
                                                                                    user_id,
                                                                                    current_time,
                                                                                    broadcast_status_id)
                                
                                list_array.append(broadcast_status_id)
                                try:
                                    results_update = BaseRepo.update(db,update_resume_period)
                                except Exception as e:
                                    results_update = db.rollback()

                                if results_update == True:
                                    insert_suspend = Sta_station_schedule_activitie(
                                                            is_deleted = False,
                                                            created=update_time,
                                                            created_by=user_id,
                                                            name="ยกเลิกแบนผังย่อยรายการ",
                                                            description="รายการ" + ' ' + str(y.name),
                                                            reference_id = y.id,
                                                            station_schedule_id = x.id,
                                                            object = "station_periods",
                                                            icon = "icon-clock.svg",
                                                            type_user = "users"
                        
                        
                                                    )
                                results_insert = BaseRepo.insert(db,insert_suspend)
                        else:     
                            if time_data_start <= time <= time_data_end and diff_time > diff_time_start_end:
                                    broadcast_status_id = 3
                                    update_resume_period = BaseRepo.update_resume_period(db,
                                                                                        Sta_station_period,
                                                                                        y.id,
                                                                                        user_id,
                                                                                        current_time,
                                                                                        broadcast_status_id)
                                    
                                    list_array.append(broadcast_status_id)
                                    try:
                                        results_update = BaseRepo.update(db,update_resume_period)
                                    except Exception as e:
                                        results_update = db.rollback()

                                    if results_update == True:
                                        insert_suspend = Sta_station_schedule_activitie(
                                                                is_deleted = False,
                                                                created=update_time,
                                                                created_by=user_id,
                                                                name="ยกเลิกแบนผังย่อยรายการ",
                                                                description="รายการ" + ' ' + str(y.name),
                                                                reference_id = y.id,
                                                                station_schedule_id = x.id,
                                                                object = "station_periods",
                                                                icon = "icon-clock.svg",
                                                                type_user = "users"
                            
                            
                                                        )
                                    results_insert = BaseRepo.insert(db,insert_suspend)
                            elif time_data_start <= time <= time_data_end and diff_time <= diff_time_start_end:
                                    broadcast_status_id = 4
                                    update_resume_period = BaseRepo.update_resume_period(db,
                                                                                        Sta_station_period,
                                                                                        y.id,
                                                                                        user_id,
                                                                                        current_time,
                                                                                        broadcast_status_id)
                                    list_array.append(broadcast_status_id)
                                    try:
                                        results_update = BaseRepo.update(db,update_resume_period)
                                    except Exception as e:
                                        results_update = db.rollback()

                                    if update_resume_period == True:
                                        insert_suspend = Sta_station_schedule_activitie(
                                                                is_deleted = False,
                                                                created=update_time,
                                                                created_by=user_id,
                                                                name="ยกเลิกแบนผังย่อยรายการ",
                                                                description="รายการ" + ' ' + str(y.name),
                                                                reference_id = y.id,
                                                                station_schedule_id = x.id,
                                                                object = "station_periods",
                                                                icon = "icon-clock.svg",
                                                                type_user = "users"
                            
                                                                
                            
                                                        )
                                        results_insert = BaseRepo.insert(db,insert_suspend)
                            else:
                                    broadcast_status_id = 7
                                    update_resume_period = BaseRepo.update_resume_period(db,
                                                                                        Sta_station_period,
                                                                                        y.id,
                                                                                        user_id,
                                                                                        current_time,
                                                                                        broadcast_status_id)
                                    
                                    list_array.append(broadcast_status_id)
                                    try:
                                        results_update = BaseRepo.update(db,update_resume_period)
                                    except Exception as e:
                                        results_update = db.rollback()
                                    if results_update == True:
                                        insert_suspend = Sta_station_schedule_activitie(
                                                                is_deleted = False,
                                                                created=update_time,
                                                                created_by=user_id,
                                                                name="ยกเลิกแบนผังย่อยรายการ",
                                                                description="รายการ" + ' ' + str(y.name),
                                                                reference_id = y.id,
                                                                station_schedule_id = x.id,
                                                                object = "station_periods",
                                                                icon = "icon-clock.svg",
                                                                type_user = "users"
                            
                                                        )
                                        results_insert = BaseRepo.insert(db,insert_suspend)
                    
                    if 3 in list_array:
                        broadcast_status_id = 3
                        update_resume_schdule = BaseRepo.update_resume_shchedule_special(db,
                                                                                    Sta_station_schedule,
                                                                                    x.id,
                                                                                    user_id,
                                                                                    current_time,
                                                                                    broadcast_status_id)
                        try:
                                results_update = BaseRepo.update(db,update_resume_schdule)
                        except Exception as e:
                                results_update = db.rollback()

                        if results_update == True:
                                insert_suspend = Sta_station_schedule_activitie(
                                                            is_deleted = False,
                                                            created=update_time,
                                                            created_by=user_id,
                                                            name="ยกเลิกแบนผังรายการ",
                                                            description="รายการ" + ' ' + str(x.name),
                                                            reference_id = x.id,
                                                            station_schedule_id = x.id,
                                                            object = "station_schedules",
                                                            icon = "icon-clock.svg",
                                                            type_user = "users"
                        
                                                    )
                                results_insert = BaseRepo.insert(db,insert_suspend) 
                
                
                
                    else:
                        broadcast_status_id = 7
                        update_resume_schdule = BaseRepo.update_resume_shchedule(db,
                                                                                    Sta_station_schedule,
                                                                                    x.id,
                                                                                    user_id,
                                                                                    current_time,
                                                                                    broadcast_status_id)
                        try:
                                results_update = BaseRepo.update(db,update_resume_schdule)
                        except Exception as e:
                                results_update = db.rollback()

                        if results_update == True:
                                insert_suspend = Sta_station_schedule_activitie(
                                                            is_deleted = False,
                                                            created=update_time,
                                                            created_by=user_id,
                                                            name="ยกเลิกแบนผังรายการ",
                                                            description="รายการ" + ' ' + str(x.name),
                                                            reference_id = x.id,
                                                            station_schedule_id = x.id,
                                                            object = "station_schedules",
                                                            icon = "icon-clock.svg",
                                                            type_user = "users"
                        
                                                    )
                                results_insert = BaseRepo.insert(db,insert_suspend)
    return ResponseSchema(
        code="200", status="Ok", message="Update Data Success"
        ).dict(exclude_none=True)




@router.get("/get-station-detail",dependencies=[Depends(JWTBearer())])
async def update_station_status(id:Optional[int]=None,db: Session = Depends(get_db)):
    results = BaseRepo.get_station_detail(db,
                                          Sta_station,
                                          Sta_station_statuses,
                                          Countries,
                                          id)
    results_all = []
    for sta_stations , sta_station_statuses , countries in results:
         
        bucket_name = 'stations'
        if sta_stations.object_key is not None:
                    
                object_name = sta_stations.object_key
                  
                url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
                  
                 
        else:
                url = None
        results_all.append({
              'id':sta_stations.id,
              'name':sta_stations.name,
              'created':sta_stations.created,
              'icon_path':url,
              'description':sta_stations.description,
              'status_id':sta_station_statuses.id,
              'status_name':sta_station_statuses.name,
              'approve_date':sta_stations.approve_date,
              'count_like':sta_stations.count_like,
              'count_share':sta_stations.count_share,
              'count_listen':sta_stations.count_listen,
              'count_comment':sta_stations.count_comment,
              'country_name':countries.name,
              'code':sta_stations.code
         })
         
        
    return ResponseSchema(
        code="200", status="Ok", message="Found Data",result=results_all
        ).dict(exclude_none=True)

@router.get("/get-broadcast-main",dependencies=[Depends(JWTBearer())])
async def get_broadcast_main(id:Optional[int]=None,db: Session = Depends(get_db)):
    update_time = datetime.now()
    current_date = update_time.strftime("%Y-%m-%d")

  
    results = BaseRepo.get_broadcast_main(db,
                                          Sta_station_schedule,
                                          current_date,
                                          id)

    results_all = []
    if results is None:
         results_all = [{
         'id':None,
         'broadcast_url':None,
         'broadcast_status_id':None
    }]
    else:
        results_all = [{
            'id':results.id,
            'broadcast_url':results.broadcast_url,
            'broadcast_status_id':results.broadcast_status_id
        }]
    
    return ResponseSchema(
        code="200", status="Ok", message="Found Data",result=results_all
        ).dict(exclude_none=True)



@router.get("/get-all-station-playlist",dependencies=[Depends(JWTBearer())])
async def update_station_status(id:Optional[int]=None,db: Session = Depends(get_db)):
      
        results_playlist = []
        results_station_period = BaseRepo.get_data_station_period(db,
                                                                  Sta_station_schedule,
                                                                  Sta_station_period,
                                                                  Sta_station_playlist,
                                                                  id)
       
        for sta_station_schedules , sta_station_periods, sta_station_playlists in results_station_period:

             results_playlist.append({
                  'schedule_date':sta_station_schedules.schedule_date,
                  'period_time_start':sta_station_periods.period_time_start,
                  'period_time_end':sta_station_periods.period_time_end,
                  'period_id':sta_station_periods.id,
                  'period_name':sta_station_periods.name,
                  'playlist_file_name':sta_station_playlists.file_name,
                  'playlist_file_path':sta_station_playlists.file_path,
                  'playlist_id':sta_station_playlists.id
             })
             
        if results_playlist != []:
            return ResponseSchema(
            code="200", status="Ok", message="Found Data",result=results_playlist
            ).dict(exclude_none=True)
        else:
             return ResponseSchema(
            code="200", status="Ok", message="Can't Found Data",result=results_playlist
            ).dict(exclude_none=True) 


        
@router.get("/get-member",dependencies=[Depends(JWTBearer())])
async def update_station_status(id:Optional[int]=None,db: Session = Depends(get_db)):
        results_station = BaseRepo.get_data_member_all(db,
                                            Sta_station,
                                            Sta_station_member,
                                            Member,
                                            id)
        
        resutls_all = []

        for sta_stations, sta_station_members, members in results_station:

           
            resutls_all.append({
                 'id':members.id,
                 'first_name':members.first_name,
                 'last_name':members.last_name,
                 'name':str(members.first_name)+ ' ' + str(members.last_name),
                 'email':members.email_verify,
                 'mobile':members.mobile_no_verify,
                 'avatar_img':members.avatar_img
            })
        
        
        
        return ResponseSchema(
        code="200", status="Ok", message="Found Data",result=resutls_all
        ).dict(exclude_none=True)


@router.get("/get-detail-station-schedule-broadcast-main",dependencies=[Depends(JWTBearer())])
async def get_detail_station_schedule_broadcast(id:Optional[int]=None,db: Session = Depends(get_db)):
    
    get_data_station = BaseRepo.get_data_all(db,
                                            Sta_station,
                                            Sta_station_statuses,
                                            Sta_station_schedule,
                                            Sta_station_period,
                                            Sta_process_statuses,
                                            Sta_broadcast_statuses,
                                            Sta_period_status,
                                            Sta_categories,
                                            Sta_broadcast,
                                            id
                                            )
    

    last_results = []
    
    for sta_stations,sta_station_statuses,sta_station_schedules,sta_station_periods,sta_process_statuses,sta_broadcast_statuses,sta_period_statuses,sta_categories,sta_broadcasts,broadcast_a in get_data_station:
        object_name = sta_stations.object_key
        bucket_name = 'stations'
        if sta_stations.object_key is not None:
                object_name = sta_stations.object_key
                url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
        else:
                url = None

        object_name2 = sta_station_periods.object_key
        bucket_name2 = 'stations'
        if sta_station_periods.object_key is not None:
                object_name2 = sta_station_periods.object_key
                url2 = MinioHandler().get_instance().presigned_get_object(bucket_name2, object_name2)
        else:
                url2 = None
        if sta_broadcast_statuses is None:
            results_broadcast_status = ''
        else:
            results_broadcast_status = sta_broadcast_statuses.name

        if sta_broadcasts is None:
             results_broadcast = ''
        else:
             results_broadcast = broadcast_a.name
        last_results.append({
            'station_id':sta_stations.id,
            'station_name':sta_stations.name,
            'station_icon_path':url,
            'station_description':sta_stations.description,
            'station_status_id':sta_station_statuses.id,
            'station_status_name':sta_station_statuses.name,
            'station_count_like':sta_stations.count_like,
            'station_count_share':sta_stations.count_share,
            'station_count_listen':sta_stations.count_listen,
            'station_count_comment':sta_stations.count_comment,
            'process_status':sta_process_statuses.name,
            'broadcast_status':results_broadcast_status,
            'period_id':sta_station_periods.id,
            'period_name':sta_station_periods.name,
            'period_icon_path':url2,
            'period_broadcast_url':sta_station_periods.broadcast_url,
            'schedule_date':sta_station_schedules.schedule_date,
            'period_time_start':sta_station_periods.period_time_start,
            'period_time_end':sta_station_periods.period_time_end,
            'period_status':sta_period_statuses.name,
            'catagorie_name':sta_categories.name,
            'broadcast':results_broadcast,
        })
 

    
    
    

    return ResponseSchema(
         code="200", status="Ok", message="Sucess retrieve data", result=last_results
     ).dict(exclude_none=True)


@router.get("/get-station-schedule-broadcast-url",dependencies=[Depends(JWTBearer())])
async def get_detail_station_schedule_broadcast(id:Optional[int]=None,db: Session = Depends(get_db)):
     
     update_time = datetime.now()
     date = update_time.strftime("%Y-%m-%d")
   
     

     get_data_station = BaseRepo.get_data_url_all(db,
                                            Sta_station_schedule,
                                            Sta_station_period,
                                            date,
                                            id
                                            )
     results = []
     
     for sta_station_schedules, sta_station_periods in get_data_station:
          

     
        bucket_name = 'stations'
        if sta_station_periods.object_key is not None:
                        
                        object_name = sta_station_periods.object_key
                    
                        url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
                    
                    
        else:
                        url = None
  
    
     
        results.append({
             'id':sta_station_periods.id,
             'name':sta_station_periods.name,
             'icon_path':url,
             'broadcast_url':sta_station_periods.broadcast_url,
             'period_time_start':sta_station_periods.period_time_start,
             'period_time_end':sta_station_periods.period_time_end,
             'schedule_date':sta_station_schedules.schedule_date,
             'broadcast_status_id':sta_station_periods.broadcast_status_id
        })
     
    
          
        
     return ResponseSchema(
         code="200", status="Ok", message="Sucess retrieve data", result=results
     ).dict(exclude_none=True)    


@router.get("/get-all-activity",dependencies=[Depends(JWTBearer())])
async def get_all_activity(id:Optional[int]=None,db: Session = Depends(get_db)):
     results = BaseRepo.get_all_activity(db,
                                         Sta_station,
                                         id)
     
     results_all = {
          'id':results.id,
          'created':results.created,
          'approve_status_id':results.approve_status_id,
          'approve_description':results.approve_description,
          'reply_date':results.approve_date
     } 

     return ResponseSchema(
         code="200", status="Ok", message="Sucess retrieve data", result=results_all
     ).dict(exclude_none=True)





# @router.patch("/update-station-schedule-period-status-id",dependencies=[Depends(JWTBearer())])
# async def get_all_summary_dashboard(id:Optional[int]=None,
#                                     broadcast_status_id:Optional[int]=None,
#                                     token: str = Depends(JWTBearer()),
#                                     tpye:Optional[str]=None,
#                                     db: Session = Depends(get_db)):

#     time_update = datetime.now()
#     decode_token = Ex_Decode.decode_token(token)
#     user_id = decode_token["id"]

#     check_station = BaseRepo.check_station(db,
#                                            Sta_station,
#                                            id,
#                                            broadcast_status_id,
#                                            user_id,
#                                            time_update)
    
#     if check_station is not None:
#         results_update = BaseRepo.update(db,check_station)

#     for x in check_station:
#           check_station_schedule = BaseRepo.check_station_schedule(db,
#                                            Sta_station_schedule,
#                                            x.id,
#                                            broadcast_status_id,
#                                            user_id,
#                                            time_update)
#           if check_station_schedule is not None:
#                 results_update2 = BaseRepo.update(db,check_station)
    
#           for y in check_station_schedule:
#                 check_period = BaseRepo.check_period(db,
#                                                     Sta_station_schedule,
#                                                     y.id,
#                                                     broadcast_status_id,
#                                                     user_id,
#                                                     time_update)
                
#                 results_update2 = BaseRepo.update(db,check_period)


#     if check_station is None:
#          return ResponseSchema(
#          code="200", status="Ok", message="ID Station not found"
#          ).dict(exclude_none=True)
    
#     elif check_period is None:
#          return ResponseSchema(
#          code="200", status="Ok", message="ID Period not found"
#          ).dict(exclude_none=True)
    
#     else:
#          return ResponseSchema(
#          code="200", status="Ok", message="Update Successfull!!"
#          ).dict(exclude_none=True)
    
        

        
        



    
