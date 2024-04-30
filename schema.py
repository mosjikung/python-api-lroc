from typing import Generic, Optional, TypeVar, Dict
from pydantic.generics import GenericModel
from pydantic import BaseModel, Field , validator
from datetime import datetime , time
T = TypeVar("T")


class Parameter(BaseModel):
    data: Dict[str, str] = None


class RequestSchema(BaseModel):
    # parameter: Parameter = Field(...) #ดึงจาก Class Parameter
    parameter: Parameter = Field(
        {
            "data": {
                "username": "",
                "email": "",
                "phone_number": "",
                "password": "",
                "first_name": "",
                "last_name": "",
            }
        }
    )


class ResponseSchema(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[T] = None


class UserSigupSchema(BaseModel):
    username: str
    email: str
    phone_number: str
    password: str
    first_name: str
    last_name: str


class UserSiginSchema(BaseModel):
    username: str
    password: str


class UserBase(BaseModel):
    username: str
    email: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class ResultsResp(BaseModel):
    result:bool
    message:str



class Updatestationmember(BaseModel):
    id:int
    station_id : int
    member_id : int
    is_owner: str


class Insertstationmember(BaseModel):
    created_by:int
    station_id:int
    member_id:int
    is_owner:str
    is_current_station:str
    station_role_id:int

class Mainresp(BaseModel):
    result:bool
    message:str

class Insertplaylistactivity(BaseModel):
    description:str
    start_time:Optional[time]=None
    station_playlist_id:int
    id:int
    

class Insertplaylistcomment(BaseModel):
    description:str
    station_playlist_id:int
    reply_id:Optional[int]=None


class Insertfilemedia(BaseModel):
    file_type_media_id:int
    file_name:str

    



class Updatefilemedia(BaseModel):
    id:int #id_file_media
    name:str
    file_type_media_id:int


class Insertfiletype(BaseModel):
    name:str
    description:str


class Updatefiletype(BaseModel):
    id:int
    name:str
    description:str

class Updateowneruser(BaseModel):
    id:int
    schedule_id:int


class Createmessagexxxx(BaseModel):
    name:str
    description:str
    form_member_id:int
    receive_member_id:int


class Createscheduletype(BaseModel):
    name:str
    description:str

class Updatescheduletype(BaseModel):
    id:int
    name:str
    description:str

class UploadFileResponse(BaseModel):
    bucket_name: str
    file_name: str
    url: str	

class CustomException(Exception):
    http_code: int
    code: str
    message: str

class Deleteactivity(BaseModel):
    id:int

class Updateprocessstatus(BaseModel):
    period_status_id:int
    user_id:int
    period_id:int

class Findperiod(BaseModel):
    id:int

class Updatestationstatus(BaseModel):
    id:int
    station_status_id:int
    suspend_date_start:Optional[str]=None
    suspend_date_end:Optional[str]=None
    suspend_comment:Optional[str]=None
    disable_comment:Optional[str]=None


class Updatestatusfilemedia(BaseModel):
    file_status_id:int
    id:int


class Updatestatusregis(BaseModel):
    id:int
    approve_description:Optional[str]=None
    approve_status_id:int

class Updatesetperioduser(BaseModel):
    id:int

class Updateperiodstatusid(BaseModel):
    id:int
    period_status_id:int


class Updatescheduleperiodstatus(BaseModel):
    id:int
    broadcast_status_id:int

class Checkemaildata(BaseModel):
    email:str
    station_id:int
    
class ChangePasswordResp(BaseModel):
    result:bool
    message:str

class Checkemaildatachannel(BaseModel):
    email:str
    channel_id:int


class Setdatastation(BaseModel):
    station_id :int
    is_owner : bool
    id:int

class Deleteduser(BaseModel):
    id:int


class Createmessages(BaseModel):
    message_group_id:int
    name:str
    description:str
    reply_message_id:int


class Updatemessagestatus(BaseModel):
    id:int


class Insertcustomerinterest(BaseModel):
    station_id : Optional[int]=None
    schedule_id : Optional[int]=None
    period_id : Optional[int]=None

class Createcustomeractionweb(BaseModel):
    station_id : Optional[int]=None
    schedule_id : Optional[int] =None
    period_id : Optional[int]=None
    action_type : Optional[int]=None


class Insertmessagegroup(BaseModel):
    station_id : int
    channel_id : Optional[int]=None
    name : Optional[str]=None
    description : Optional[str]=None
    form_member_id : Optional[int]=None
    receive_member_id : Optional[int]=None
    message_type_id : int
    message_mode : str
    form_customer_id : Optional[int]=None

class Createmessagenone(BaseModel):
    message_group_id:int
    description:Optional[str]=None
    reply_message_id:int
    message_mode:str

class Updatechannelstatus(BaseModel):
    sta_station_channel_id : int


    



















# หน้า schema คือ Request Body
