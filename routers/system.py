from fastapi import APIRouter, Depends , Response , Header
from fastapi.responses import JSONResponse
from typing import List , Optional
from schema import ( 
    ResponseSchema,

)
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from respository.repo_system import  BaseRepo
from minio_handler import MinioHandler

from model import (
     Users ,
     Sta_station , 
     Sta_station_schedule,
     Member,
     Sta_station_period,
     Sta_playlist,
     Sta_station_playlist,
     Sta_partner,
     Sta_message_files,
     Sta_file_medias,
     Sta_channel_playlists,
     Sta_channel
    
     )
from datetime import datetime, timedelta
import pdb
from sqlalchemy.exc import SQLAlchemyError

import librosa
import requests
import io
import tempfile
import os




router = APIRouter(
              prefix="",
              tags=['System'],
              responses ={404:{
                            'message' : "Not found"
              }}
              
)


# encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""
    Authentication Router
"""
def check_date_update(date):
        update_time_true = datetime.now()
        update_time_5_days = update_time_true + timedelta(days=5)
        time_difference =   update_time_true - date
        cal_days =  time_difference.days
        if cal_days > 5:
                return True
        else:
                return False
        
def calculate_bpm(audio_url):
 # ดึงไฟล์เสียงจาก URL
        
    response = requests.get(audio_url)
    
    # สร้าง temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(response.content)
        temp_filepath = temp_file.name
    
    # โหลดไฟล์เสียง
    y, sr = librosa.load(temp_filepath)

    # คำนวณ tempo ของเพลง
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

    # ลบ temporary file
    os.remove(temp_filepath)

    return tempo
    





@router.get("/update-path-imgage-station")
async def get_update_path_image_station(db: Session = Depends(get_db)):
    
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_time_log = datetime.now().strftime("%Y-%m-%d")
    update_station = BaseRepo.get_all_station(db,
                                          Sta_station)
    log_file = "log/log_update_path_minio.txt"

    for sta_stations in update_station:
        bucket_name = 'stations'
        # created = sta_stations.created
        # modified = sta_stations.modified
        # if modified is not None:
        #     results_check = check_date_update(modified)
        # else:
        #     results_check = check_date_update(created)


        #if results_check == True:
        if sta_stations.object_key is not None and sta_stations.object_key != '':
                            object_name = sta_stations.object_key
                            url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
                            check_list_update = BaseRepo.check_list_update(db,
                                                    Sta_station,
                                                    url,
                                                    sta_stations.id
                                                    )
                            results_update = BaseRepo.update(db,check_list_update)
        else:
                            url = None
        
        
    if results_update == True:
            with open(log_file, "a") as file:
                file.write(f"Time = {update_time}: Sta_stations update path image from minio success \n\n\n")
            return ResponseSchema(
            code="200", status="Ok", message="upDateSuccess"
            ).dict(exclude_none=True)
    
    else:
            with open(log_file, "a") as file:
                file.write(f"Time = {update_time}: Sta_stations update path image from minio failed \n\n\n")
            return ResponseSchema(
            code="200", status="Ok", message="upDateHasProblem"
                ).dict(exclude_none=True)

@router.get("/update-path-imgage-station-schedule")
async def get_update_path_image_station_schedule(db: Session = Depends(get_db)):
    
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_time_log = datetime.now().strftime("%Y-%m-%d")
    update_schedule = BaseRepo.get_all_station(db,
                                          Sta_station_schedule)
    log_file = "log/log_update_path_minio.txt"

    for sta_station_schedules in update_schedule:
        bucket_name = 'stations'
        # created = sta_station_schedules.created
        # modified = sta_station_schedules.modified
        # if modified is not None:
        #     results_check = check_date_update(modified)
        # else:
        #     results_check = check_date_update(created)
    
        #if results_check == True:
        if sta_station_schedules.object_key is not None and sta_station_schedules.object_key != '':
                            object_name2 = sta_station_schedules.object_key
                            url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name2)
                            check_list_update = BaseRepo.check_list_update(db,
                                                       Sta_station_schedule,
                                                       url,
                                                       sta_station_schedules.id
                                                       )
                            results_update = BaseRepo.update(db,check_list_update)
        else:
                            url = None

    if results_update == True:
            with open(log_file, "a") as file:
                file.write(f"Time = {update_time}: Sta_station_schedule update path image from minio success \n\n\n")
            return ResponseSchema(
            code="200", status="Ok", message="upDateSuccess"
            ).dict(exclude_none=True)
    
    else:
            with open(log_file, "a") as file:
                file.write(f"Time = {update_time}: Sta_station_schedule update path image from minio failed \n\n\n")
            return ResponseSchema(
            code="200", status="Ok", message="upDateHasProblem"
            ).dict(exclude_none=True)


@router.get("/update-path-imgage-station-period")
async def get_update_path_image_station_period(db: Session = Depends(get_db)):
    
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_time_log = datetime.now().strftime("%Y-%m-%d")
    id = 1730
    update_period = BaseRepo.get_all_station(db,
                                          Sta_station_period)
    log_file = "log/log_update_path_minio.txt"
    
    # for sta_station_periods in update_period:
    #     bucket_name = 'stations'
    #     created = sta_station_schedules.created
    #     modified = sta_station_schedules.modified
    #     if modified is not None:
    #         results_check = check_date_update(modified)
    #     else:
    #         results_check = check_date_update(created)
    
    for sta_station_periods in update_period:
        bucket_name = 'stations'
        if sta_station_periods.object_key is not None and sta_station_periods.object_key != '':
                            object_name3 = sta_station_periods.object_key
                            url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name3)
                            check_list_update = BaseRepo.check_list_update(db,
                                                       Sta_station_period,
                                                       url,
                                                       sta_station_periods.id
                                                       )
                            results_update = BaseRepo.update(db,check_list_update)
        else:
                            url = None


    if results_update == True:
                with open(log_file, "a") as file:
                    file.write(f"Time = {update_time}: Sta_station_period update path image from minio success \n\n\n")
                return ResponseSchema(
                code="200", status="Ok", message="upDateSuccess"
                ).dict(exclude_none=True)
        
    else:
                with open(log_file, "a") as file:
                    file.write(f"Time = {update_time}: Sta_station_period update path image from minio failed \n\n\n")
                return ResponseSchema(
                code="200", status="Ok", message="upDateHasProblem"
            ).dict(exclude_none=True)


@router.get("/update-path-imgage-member")
async def get_update_path_image_member(db: Session = Depends(get_db)):
    
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_time_log = datetime.now().strftime("%Y-%m-%d")
    update_member = BaseRepo.get_all_member(db,
                                          Member)
    log_file = "log/log_update_path_minio.txt"
    
    for members in update_member:
        bucket_name = 'member'
        if members.object_key is not None and members.object_key != '':
                            object_name = members.object_key
                            url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
                            check_list_update = BaseRepo.check_list_update_member(db,
                                                       Member,
                                                       url,
                                                       members.id
                                                       )
                            results_update = BaseRepo.update(db,check_list_update)
        else:
                            url = None

    
    if results_update == True:
                with open(log_file, "a") as file:
                    file.write(f"Time = {update_time}: Members update path image from minio success \n\n\n")
                return ResponseSchema(
                code="200", status="Ok", message="upDateSuccess"
                ).dict(exclude_none=True)
        
    else:
                with open(log_file, "a") as file:
                    file.write(f"Time = {update_time}: Members update path image from minio failed \n\n\n")
                return ResponseSchema(
                code="200", status="Ok", message="upDateHasProblem"
            ).dict(exclude_none=True)

            
@router.get("/update-path-imgage-user")
async def get_update_path_image_users(db: Session = Depends(get_db)):
    
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_time_log = datetime.now().strftime("%Y-%m-%d")

    update_member = BaseRepo.get_all_member(db,
                                          Users)
    log_file = "log/log_update_path_minio.txt"
    
    for users in update_member:
        bucket_name = 'member'
        if users.object_key is not None and users.object_key != '':
                            object_name2 = users.object_key
                            url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name2)
                            check_list_update = BaseRepo.check_list_update_member(db,
                                                       Users,
                                                       url,
                                                       users.id
                                                       )
                            results_update = BaseRepo.update(db,check_list_update)
        else:
                            url = None

    if results_update == True:
                with open(log_file, "a") as file:
                    file.write(f"Time = {update_time}: Users update path image from minio success \n\n\n")
                file.close()
                return ResponseSchema(
                code="200", status="Ok", message="upDateSuccess"
                ).dict(exclude_none=True)
        
    else:
                with open(log_file, "a") as file:
                    file.write(f"Time = {update_time}: Users update path image from minio failed \n\n\n")
                file.close()
                return ResponseSchema(
                code="200", status="Ok", message="upDateHasProblem"
            ).dict(exclude_none=True)


@router.get("/update-path-imgage-sta-station-playlist")
async def get_update_path_image_sta_station_playlist(db: Session = Depends(get_db)):
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_time_log = datetime.now().strftime("%Y-%m-%d")
    update_playlist = BaseRepo.get_all_member(db,
                                          Sta_station_playlist)
    log_file = "log/log_update_path_minio.txt"
    
    for users in update_playlist:
        bucket_name = 'stations'
        if users.object_key is not None and users.object_key != '':
                            object_name3 = users.object_key
                            url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name3)
                            check_list_update = BaseRepo.check_list_update_playlist(db,
                                                       Sta_station_playlist,
                                                       url,
                                                       users.id
                                                       )
                            results_update = BaseRepo.update(db,check_list_update)
        else:
                            url = None

    if results_update == True:
                with open(log_file, "a") as file:
                    file.write(f"Time = {update_time}: Sta_station_playlist update path image from minio success \n\n\n")
                return ResponseSchema(
                code="200", status="Ok", message="upDateSuccess"
                ).dict(exclude_none=True)
        
    else:
                with open(log_file, "a") as file:
                    file.write(f"Time = {update_time}: Sta_station_playlist update path image from minio failed \n\n\n")
                return ResponseSchema(
                code="200", status="Ok", message="upDateHasProblem"
            ).dict(exclude_none=True)


@router.get("/update-path-imgage-sta-partner")
async def get_update_path_image_sta_partner(db: Session = Depends(get_db)):
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_time_log = datetime.now().strftime("%Y-%m-%d")
    update_partner = BaseRepo.get_all_member(db,
                                          Sta_partner)
    
    log_file = "log/log_update_path_minio.txt"
    
    for users in update_partner:
        bucket_name = 'stations'
        if users.object_key is not None and users.object_key != '':
                            object_name3 = users.object_key
                            url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name3)
                            check_list_update = BaseRepo.check_list_update_partner(db,
                                                       Sta_partner,
                                                       url,
                                                       users.id
                                                       )
                            results_update = BaseRepo.update(db,check_list_update)
        else:
                            url = None

    
    if results_update == True:
                with open(log_file, "a") as file:
                    file.write(f"Time = {update_time}: Sta_partner update path image from minio success \n\n\n")
                return ResponseSchema(
                code="200", status="Ok", message="upDateSuccess"
                ).dict(exclude_none=True)
        
    else:
                with open(log_file, "a") as file:
                    file.write(f"Time = {update_time}: Sta_partner update path image from minio failed \n\n\n")
                return ResponseSchema(
                code="200", status="Ok", message="upDateHasProblem"
            ).dict(exclude_none=True)
            
    

@router.get("/update-path-imgage-sta-message-files")
async def get_update_path_image_sta_message_files(db: Session = Depends(get_db)):
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_time_log = datetime.now().strftime("%Y-%m-%d")

    update_message = BaseRepo.get_all_member(db,
                                          Sta_message_files)
    log_file = "log/log_update_path_minio.txt"
    
    
    bucket_name = 'messages'
    # created = users.created
    # modified = users.created
    # if modified is not None:
    #     results_check = check_date_update(modified)
    # else:
    #     results_check = check_date_update(created)
    
    
    # if results_check == True:
    for users in update_message:
                if users.object_key is not None and users.object_key != '':
                                    
                                        object_name4 = users.object_key
                                        url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name4)
                                        check_list_update = BaseRepo.check_list_update_partner(db,
                                                                Sta_message_files,
                                                                url,
                                                                users.id
                                                                )
                                        
                                        results_update = BaseRepo.update(db,check_list_update)
                else:
                                        url = None
    
    
    if results_update == True:
                with open(log_file, "a") as file:
                    file.write(f"Time = {update_time}: Sta_message_files update path image from minio success \n\n\n")
                return ResponseSchema(
                code="200", status="Ok", message="upDateSuccess"
                ).dict(exclude_none=True)
        
    else:
                with open(log_file, "a") as file:
                    file.write(f"Time = {update_time}: Sta_message_files update path image from minio failed \n\n\n")
                return ResponseSchema(
                code="200", status="Ok", message="upDateHasProblem"
            ).dict(exclude_none=True)
    

@router.get("/update-path-imgage-sta-file-medias")
async def get_update_path_image_sta_file_medias(db: Session = Depends(get_db)):
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_time_log = datetime.now().strftime("%Y-%m-%d")
    update_file_medias = BaseRepo.get_all_member(db,
                                          Sta_file_medias)
    
    log_file = "log/log_update_path_minio.txt"
    
    for users in update_file_medias:
        bucket_name = 'stations'
        if users.object_key is not None and users.object_key != '':
                            object_name3 = users.object_key
                            url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name3)
                            check_list_update = BaseRepo.check_list_update_file_medias(db,
                                                       Sta_file_medias,
                                                       url,
                                                       users.id
                                                       )
                            results_update = BaseRepo.update(db,check_list_update)
        else:
                            url = None

    
    if results_update == True:
                with open(log_file, "a") as file:
                    file.write(f"Time = {update_time}: Sta_file_medias update path image from minio success \n\n\n")
                return ResponseSchema(
                code="200", status="Ok", message="upDateSuccess"
                ).dict(exclude_none=True)
        
    else:
                with open(log_file, "a") as file:
                    file.write(f"Time = {update_time}: Sta_file_medias update path image from minio failed \n\n\n")
                return ResponseSchema(
                code="200", status="Ok", message="upDateHasProblem"
            ).dict(exclude_none=True)
    

@router.get("/update-path-imgage-sta-channel-playlist")
async def get_update_path_image_sta_channel_playlist(db: Session = Depends(get_db)):
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_time_log = datetime.now().strftime("%Y-%m-%d")
    update_file_ch_playlist = BaseRepo.get_all_member(db,
                                          Sta_channel_playlists)
    
    log_file = "log/log_update_path_minio.txt"
    
    for users in update_file_ch_playlist:
        bucket_name = 'stations'
        if users.object_key is not None and users.object_key != '':
                            object_name3 = users.object_key
                            url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name3)
                            check_list_update = BaseRepo.check_list_update_file_medias(db,
                                                       Sta_channel_playlists,
                                                       url,
                                                       users.id
                                                       )
                            results_update = BaseRepo.update(db,check_list_update)
        else:
                            url = None

    
    if results_update == True:
                with open(log_file, "a") as file:
                    file.write(f"Time = {update_time}: Sta_file_medias update path image from minio success \n\n\n")
                return ResponseSchema(
                code="200", status="Ok", message="upDateSuccess"
                ).dict(exclude_none=True)
        
    else:
                with open(log_file, "a") as file:
                    file.write(f"Time = {update_time}: Sta_file_medias update path image from minio failed \n\n\n")
                return ResponseSchema(
                code="200", status="Ok", message="upDateHasProblem"
            ).dict(exclude_none=True)    



@router.get("/update-path-imgage-sta-channel")
async def get_update_path_image_sta_channel(db: Session = Depends(get_db)):
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_time_log = datetime.now().strftime("%Y-%m-%d")
    update_file_ch = BaseRepo.get_all_member(db,
                                          Sta_channel)
    
    log_file = "log/log_update_path_minio.txt"
    
    for users in update_file_ch:
        bucket_name = 'stations'
        if users.object_key is not None and users.object_key != '':
                            object_name3 = users.object_key
                            url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name3)
                            check_list_update = BaseRepo.check_list_update_sta_channel(db,
                                                       Sta_channel,
                                                       url,
                                                       users.id
                                                       )
                            results_update = BaseRepo.update(db,check_list_update)
        else:
                            url = None

    
    if results_update == True:
                with open(log_file, "a") as file:
                    file.write(f"Time = {update_time}: Sta_channel update path image from minio success \n\n\n")
                return ResponseSchema(
                code="200", status="Ok", message="upDateSuccess"
                ).dict(exclude_none=True)
        
    else:
                with open(log_file, "a") as file:
                    file.write(f"Time = {update_time}: Sta_channel update path image from minio failed \n\n\n")
                return ResponseSchema(
                code="200", status="Ok", message="upDateHasProblem"
            ).dict(exclude_none=True)    


@router.get("/calculate-bpm-from-minio",summary="sta_file_medias")
async def cal_bpm_from_minio(id:Optional[int]=None,db: Session = Depends(get_db)):
        update_time = datetime.now()
        log_file = "log/log_update_path_minio.txt"
        if id is not None:
            check_data_file_meidas = BaseRepo.check_data_file_media_id(db,
                                                                    Sta_file_medias,
                                                                    id)
        else:
            check_data_file_meidas = BaseRepo.check_data_file_media(db,
                                                                    Sta_file_medias)
       
        
        results = []
        for x in check_data_file_meidas:
                    
                    if x.object_key is not None and x.bpm is None:
                            bucket_name = 'stations'
                            object_name = x.object_key
                            url = MinioHandler().get_instance().presigned_get_object(bucket_name, object_name)
                            bpm = calculate_bpm(url)
                            results.append({
                                'id':x.id,
                                'bpm':bpm
                            })

                            if bpm is not None:
                                prepair_update_file_media = BaseRepo.prepare_update_file_medias(db,
                                                                                                Sta_file_medias,
                                                                                                bpm,
                                                                                                x.id,
                                                                                                update_time
                                                                                                )
                                
                                
                                if prepair_update_file_media is not None:
                                        reuslts_update = BaseRepo.update(db,prepair_update_file_media)
                                        if reuslts_update == True:
                                            with open(log_file, "a") as file:
                                                file.write(f"Time = {update_time}: Sta_file_medias update bpm from minio success \n\n\n")
                                            return ResponseSchema(
                                                code="200", status="Ok", message="updateSuccess",result=results
                                            ).dict(exclude_none=True)
                                        
