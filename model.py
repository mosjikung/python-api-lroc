from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
    Time,
    Date,
    PrimaryKeyConstraint,
    ForeignKey,
    UniqueConstraint,
    Sequence,
    Numeric
)
from sqlalchemy.orm import relationship
from config import Base
import datetime


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {'schema' : 'system'}
    id = Column(Integer, primary_key=True)
    system_id = Column(Integer,ForeignKey("nrc.sta_station_schedules.id"))
    member_role_id = Column(Integer)
    username = Column(String)
    password = Column(String)
    avatar_name = Column(String)
    avatar_img = Column(String)
    email_verify = Column(String)
    mobile_no_verify = Column(Boolean)
    is_deleted = Column(Boolean)
    created = Column(DateTime)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    display_name = Column(String)
    tel_id = Column(Integer)
    unique_link = Column(String)
    expire_time = Column(DateTime)
    is_activated = Column(Boolean)
    unique_link_activated = Column(String)
    expire_time_activated = Column(DateTime)
    titles_id = Column(Integer)
    units_id = Column(Integer)
    type_user_id = Column(Integer)
    citizen_no = Column(String)
    is_active = Column(Boolean)
    first_name = Column(String)
    last_name = Column(String)
    postal_code = Column(String)
    alley = Column(String)
    building = Column(String)
    house_no = Column(String)
    province_id = Column(Integer)
    district_id = Column(Integer)
    sub_district_id = Column(Integer)
    street = Column(String)
    mas_unit_position_id = Column(Integer)
    unit_type_id = Column(Integer)
    phone_office = Column(String)
    parent_id = Column(Integer)
    industrial_estate_id = Column(Integer)
    member_types_id = Column(Integer)
    session_id = Column(Integer)
    language = Column(String)
    address = Column(String)
    province = Column(String)
    district = Column(String)
    sub_district = Column(String)
    country_id = Column(Integer)
    store_file_path = Column(Text)
    status = Column(Boolean)
    email = Column(String)
    member_type_id = Column(Integer)
    object_key = Column(String)
    station_schedulex = relationship("Sta_station_schedule",back_populates="userx")

class Sta_period_types(Base):
    __tablename__ = "sta_period_types"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    name = Column(String,nullable=True)
    is_deleted = Column(Boolean,nullable=True)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)

class Sta_categories(Base):
    __tablename__ = "sta_categories"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    name = Column(String,nullable=True)
    category_id = Column(Integer)
    is_deleted = Column(Boolean,nullable=True)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer,ForeignKey("system.users.id"))
    modified = Column(DateTime)
    modified_by = Column(Integer)
    file_name = Column(Text)
    file_path = Column(Text)
    file_type = Column(Text)
    file_size = Column(Text)
    station_main = relationship("Sta_station",back_populates="station_catagory")



class Sta_station_schedule(Base):
    __tablename__ = "sta_station_schedules"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,nullable=True)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    station_id = Column(Integer,ForeignKey("nrc.sta_stations.id"))
    name = Column(String)
    icon_path = Column(String)
    schedule_date = Column(DateTime)
    schedule_time = Column(DateTime)
    audit_status_id = Column(Integer)
    process_status_id = Column(Integer)
    broadcast_status_id = Column(Integer,ForeignKey("nrc.sta_broadcast_statuses.id"))
    schedule_number = Column(String)
    schedule_time_start = Column(Time)
    schedule_time_end = Column(Time)
    count_like = Column(Integer)
    count_play = Column(Integer)
    count_share = Column(Integer)
    count_comment = Column(Integer)
    comment_delete = Column(String)
    object_key = Column(String)
    schedule_category_id = Column(Integer)
    broadcast_date = Column(Date)
    broadcast_time = Column(Time)
    user_id = Column(Integer)
    broadcast_url = Column(String)
    suspend_date_start = Column(Date)
    broadcast_status_date = Column(DateTime)
    service_stop_date = Column(DateTime)
    stationx = relationship("Sta_station",back_populates="station_schedule")
    userx = relationship("Users",back_populates="station_schedulex")
    sta_schedule_broadcast = relationship("Sta_broadcast",back_populates="sta_broadcast_schedule")
    station_period_link = relationship("Sta_station_period",back_populates="station_schedule_link")
    station_broadcast_statuses_sc = relationship("Sta_broadcast_statuses",back_populates="station_schedule_sc")



class Sta_station(Base):
    __tablename__ = "sta_stations"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,nullable=True)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer,ForeignKey("system.members.id"))
    modified = Column(DateTime)
    modified_by = Column(Integer)
    name = Column(String)
    description = Column(String)
    icon_path = Column(String)
    url_station = Column(String)
    category_id = Column(Integer,ForeignKey("nrc.sta_categories.id"))
    country_id = Column(Integer)
    code = Column(Integer)
    is_enabled = Column(Boolean)
    station_status_id = Column(Integer,ForeignKey("nrc.sta_station_statuses.id"))
    is_hide_statistics = Column(Boolean)
    station_public_id = Column(Integer)
    station_comment_id = Column(Integer)
    can_download = Column(Boolean)
    can_like = Column(Boolean)
    canceled_date = Column(DateTime)
    deleted_date = Column(DateTime)
    object_key = Column(String)
    approve_status_id = Column(Integer,ForeignKey("nrc.sta_approve_statuses.id"))
    approve_description = Column(String)
    count_like = Column(Integer)
    count_share = Column(Integer)
    count_listen = Column(Integer)
    suspend_date_start = Column(Date)
    suspend_date_end = Column(Date)
    suspend_comment = Column(String)
    disable_comment = Column(String)
    approve_date = Column(DateTime)
    count_comment = Column(Integer)
    station_catagory = relationship("Sta_categories",back_populates="station_main")
    stations_status = relationship("Sta_station_statuses",back_populates="status_id")
    station_schedule = relationship("Sta_station_schedule",back_populates="stationx")
    membersx = relationship("Member",back_populates="sta_stationx")
    sta_station_to_approve_status = relationship("Sta_approve_statuses",back_populates="sta_approve_status_to_station")


class Sta_process_statuses(Base):
    __tablename__ = "sta_process_statuses"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,nullable=True)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    name = Column(String)


class Sta_period_times(Base):
    __tablename__ = "sta_period_times"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,nullable=True)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    name = Column(String)


class Sta_broadcast_statuses(Base):
    __tablename__ = "sta_broadcast_statuses"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,nullable=True)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)   
    name = Column(String)
    style = Column(String)
    sta_broadcast_xx = relationship("Sta_broadcast",back_populates="sta_broadcast_statusxx")
    station_schedule_sc = relationship("Sta_station_schedule",back_populates="station_broadcast_statuses_sc")

class Sta_audit_statuses(Base):
    __tablename__ = "sta_audit_statuses"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,nullable=True)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    name = Column(String)

class Sta_station_statuses(Base):
    __tablename__ = "sta_station_statuses"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True,)
    is_deleted = Column(Boolean,nullable=True)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    name = Column(String)
    status_id = relationship("Sta_station",back_populates="stations_status")
    


class Member(Base):
        __tablename__ = "members"
        __table_args__ = {'schema' : 'system'}
        id = Column(Integer, primary_key=True , nullable=True)
        system_id = Column(Integer , nullable=True)
        member_role_id = Column(Integer)
        username = Column(String)
        password = Column(Text)
        avatar_name = Column(String)
        avatar_img = Column(Text)
        email_verify = Column(String)
        mobile_no_verify = Column(String)
        is_deleted = Column(Boolean)
        created = Column(DateTime)
        created_by = Column(Integer)
        modified = Column(DateTime)
        modified_by = Column(Integer)
        display_name = Column(String)
        tel_id = Column(Integer)
        unique_link = Column(String)
        expire_time = Column(DateTime)
        is_activated = Column(Boolean)
        unique_link_activated = Column(String)
        expire_time_activated = Column(DateTime)
        titles_id = Column(Integer)
        units_id = Column(Integer)
        type_user_id = Column(Integer)
        citizen_no = Column(Integer)
        is_active = Column(Boolean)
        first_name = Column(String)
        last_name = Column(String)
        postal_code = Column(String)
        alley = Column(String)
        building = Column(String)
        house_no = Column(String)
        province_id = Column(Integer)
        district_id = Column(Integer)
        sub_district_id = Column(Integer)
        street = Column(String)
        mas_unit_position_id = Column(Integer)
        unit_type_id = Column(Integer)
        phone_office = Column(String)
        is_approve = Column(Boolean)
        parent_id = Column(Integer)
        industrial_estate_id = Column(Integer)
        member_type_id = Column(Integer)
        session_id = Column(Integer)
        language = Column(String)
        address = Column(String)
        province = Column(String)
        district = Column(String)
        sub_district = Column(String)
        country_id = Column(Integer)
        store_file_path = Column(Text)
        status = Column(Boolean)
        email = Column(String)
        member_types_id = Column(Integer)
        object_key = Column(String)
        phone_number = Column(String)
        station_memberx = relationship("Sta_station_member",back_populates="memberx")
        sta_stationx = relationship("Sta_station",back_populates="membersx")
        sta_channel = relationship("Sta_channel_member",back_populates="membersxx")


class Sta_station_member(Base):
    __tablename__ = "sta_station_members"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,nullable=True)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    station_id = Column(Integer)
    member_id = Column(Integer,ForeignKey("system.members.id"))
    is_owner = Column(Boolean)
    is_current_station  = Column(Boolean)
    station_role_id = Column(Integer)
    last_active_dated = Column(DateTime)
    memberx = relationship("Member",back_populates="station_memberx")
    


class Sta_station_schedule_user(Base):
    __tablename__ = "sta_station_schedule_users"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,nullable=True)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    station_schedule_id = Column(Integer)
    user_id = Column(Integer)
    process_status_id = Column(Integer)
    audit_date = Column(DateTime)



class Sta_station_period_user(Base):
    __tablename__ = "sta_station_period_users"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,nullable=True)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    station_schedule_id = Column(Integer)
    user_id = Column(Integer)
    process_status_id = Column(Integer)
    audit_date = Column(DateTime)
    station_period_id = Column(Integer)



class Sta_station_schedule_activitie(Base):
    __tablename__ = "sta_station_schedule_activities"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,nullable=True)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    station_schedule_id = Column(Integer)
    name = Column(String)
    description = Column(String)
    status_id = Column(Integer)
    object = Column(String)
    reference_id = Column(Integer)
    icon = Column(String)
    created_name = Column(String)
    created_img = Column(String)
    type_user = Column(String)
    type_activity = Column(String)


class Sta_station_playlist_activities(Base):
    __tablename__ = "sta_station_playlist_activities"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    name = Column(String)
    description = Column(String)
    start_time = Column(Time)
    end_time = Column(Time)
    station_playlist_id = Column(Integer,ForeignKey("nrc.sta_station_playlists.id"))
    station_playlist_history_id = Column(Integer)
    station_playlist_status_id = Column(Integer)
    station_playlist_link = relationship("Sta_station_playlist",back_populates="station_playlist_activities_link")

class Sta_station_playlist_comments(Base):
    __tablename__ = "sta_station_playlist_comments"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    name = Column(String)
    description = Column(String)
    station_playlist_id = Column(Integer,ForeignKey("nrc.sta_station_playlists.id"))
    station_playlist_history_id = Column(Integer)
    reply_id = Column(Integer)
    user_id = Column(Integer)
    type_user = Column(String)
    station_playlist_link_2  = relationship("Sta_station_playlist",back_populates="station_playlist_comments_link")


class Sta_station_playlist_history(Base):
    __tablename__ = "sta_station_playlist_histories"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    station_playlist_id = Column(Integer)
    file_name = Column(String)
    file_path = Column(Text)
    file_type = Column(Text)
    file_size = Column(Text)
    time_duration = Column(String)
    object_key = Column(String)


class Sta_station_playlist(Base):
    __tablename__ = "sta_station_playlists"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    station_period_id = Column(Integer,ForeignKey("nrc.sta_station_periods.id"))
    station_playlist_history_id = Column(Integer)
    file_name = Column(Text)
    file_path = Column(Text)
    file_type = Column(Text)
    file_size = Column(Text)
    time_duration = Column(String)
    order = Column(Integer)
    audit_status_id = Column(Integer)
    object_key = Column(String)
    source_ref = Column(String)
    station_playlist_status_id = Column(Integer)
    is_edit = Column(Boolean)
    station_playlist_activities_link = relationship("Sta_station_playlist_activities",back_populates="station_playlist_link")
    station_playlist_comments_link = relationship("Sta_station_playlist_comments",back_populates="station_playlist_link_2")
    station_period_link_2 = relationship("Sta_station_period",back_populates="station_playlist_link2")




class Sta_file_type_medias(Base):
    __tablename__ = "sta_file_type_medias"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    name = Column(String)
    description = Column(String)


class Sta_file_medias(Base):
    __tablename__ = "sta_file_medias"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    name = Column(String)
    file_type_media_id = Column(Integer)
    file_name = Column(String)
    file_path = Column(Text)
    file_type = Column(String)
    file_size = Column(String)
    time_duration = Column(String)
    order = Column(Integer)
    file_status_id = Column(Integer)
    object_key = Column(String)
    artist = Column(String)
    album = Column(String)
    description = Column(String)
    station_id = Column(Integer)
    channel_id = Column(Integer)
    bpm = Column(Numeric)


class Sta_channel_member(Base):
    __tablename__ = "sta_channel_members"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    channel_id = Column(Integer)
    member_id = Column(Integer,ForeignKey("system.members.id"))
    is_owner = Column(Boolean)
    is_current_channel = Column(Boolean)
    channel_role_id = Column(Integer)
    last_active_dated = Column(DateTime)
    membersxx = relationship("Member",back_populates="sta_channel")

class Sta_broadcast(Base):
    __tablename__ = "sta_broadcasts"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    station_schedule_id = Column(Integer,ForeignKey("nrc.sta_station_schedules.id"))
    broadcast_date = Column(Date)
    broadcast_time = Column(Time)
    count_like = Column(Integer)
    count_play = Column(Integer)
    count_share = Column(Integer)
    count_comment = Column(Integer)
    broadcast_history_status_id  = Column(Integer,ForeignKey("nrc.sta_broadcast_history_statuses.id"))
    broadcast_url = Column(String)
    station_period_id = Column(Integer)
    server_process_id = Column(Integer)
    broadcast_status_id = Column(Integer,ForeignKey("nrc.sta_broadcast_statuses.id"))
    sta_broadcast_schedule = relationship("Sta_station_schedule",back_populates="sta_schedule_broadcast")
    sta_broadcast_history_statusx = relationship("Sta_broadcast_history_status",back_populates="sta_broadcastx")
    sta_broadcast_statusxx = relationship("Sta_broadcast_statuses",back_populates="sta_broadcast_xx")


class Sta_broadcast_history_status(Base):
    __tablename__ = "sta_broadcast_history_statuses"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    name = Column(String)
    sta_broadcastx = relationship("Sta_broadcast",back_populates="sta_broadcast_history_statusx")


class Sta_message(Base):
    __tablename__ = "sta_messages"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,Sequence('sta_messages_id_seq'),primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    message_group_id = Column(Integer)
    name = Column(String)
    description = Column(String)
    reply_message_id = Column(Integer)
    type_user = Column(String)
   


class Sta_schedule_catagorie(Base):
    __tablename__ = "sta_schedule_categories"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    name = Column(String)
    description = Column(String)


class Sta_station_period(Base):
    __tablename__ = "sta_station_periods"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    station_schedule_id = Column(Integer,ForeignKey("nrc.sta_station_schedules.id"))
    name = Column(String)
    icon_path = Column(String)
    period_type_id = Column(Integer)
    period_time_id = Column(Integer)
    period_time_start = Column(Time)
    period_time_end = Column(Time)
    run_date = Column(Date)
    run_time = Column(Time)
    audit_status_id = Column(Integer)
    object_key = Column(String)
    period_status_id = Column(Integer,ForeignKey("nrc.sta_period_statuses.id"))
    period_category_id = Column(Integer)
    member_id = Column(Integer)
    station_channel_id = Column(Integer)
    user_id = Column(Integer)
    broadcast_url = Column(String)
    broadcast_status_id = Column(Integer)
    broadcast_type_id = Column(Integer)
    broadcast_status_date = Column(DateTime)
    audit_member_id = Column(Integer)
    audit_date = Column(Date)
    channel_id = Column(Integer)
    description = Column(String)
    count_like = Column(Integer)
    count_listen = Column(Integer)
    count_share = Column(Integer)
    station_schedule_link = relationship("Sta_station_schedule",back_populates="station_period_link")
    period_status_link = relationship("Sta_period_status",back_populates="station_schedule_link_2")
    station_playlist_link2 = relationship("Sta_station_playlist",back_populates="station_period_link_2")


class Sta_period_status(Base):
    __tablename__ = "sta_period_statuses"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    name = Column(String)
    station_schedule_link_2 = relationship("Sta_station_period",back_populates="period_status_link")

class Sta_station_activities(Base):
    __tablename__ = "sta_station_activities"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    station_id = Column(Integer)
    name = Column(String)
    description = Column(String)
    status_id = Column(String)
    object = Column(String)
    reference_id = Column(Integer)
    icon = Column(String)
    created_name = Column(String)
    created_img = Column(String)


class Countries(Base):
    __tablename__ = "countries"
    __table_args__ = {'schema' : 'master'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    name = Column(String)
    name_th =Column(String)
    name_en = Column(String)
    name_lo = Column(String)

class Sta_approve_statuses(Base):
    __tablename__ = "sta_approve_statuses"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    name = Column(String)
    sta_approve_status_to_station = relationship("Sta_station",back_populates="sta_station_to_approve_status")


class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = {'schema' : 'system'}
    id = Column(Integer,primary_key=True,nullable=True)
    system_id = Column(Integer)
    username = Column(String)
    password = Column(Text)
    avatar_name = Column(String)
    avatar_img = Column(Text)
    email = Column(String)
    birth_date = Column(Date)
    display_name = Column(String)
    is_deleted = Column(Boolean)
    created = Column(DateTime)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    type = Column(String)
    unique_link = Column(String)
    expire_time = Column(DateTime)
    unique_link_activated = Column(String)
    expire_time_activated = Column(DateTime)
    object_key = Column(String)
    is_activated = Column(Boolean)
    first_name = Column(String)
    last_name = Column(String)

class Stat_customer(Base):
    __tablename__ = "stat_customers"
    __table_args__ = {'schema' : 'stat'}
    id = Column(Integer,primary_key=True,nullable=True)
    sum_status_online = Column(Integer)
    sum_online_date = Column(DateTime)
    sum_view = Column(Integer)
    sum_view_date = Column(DateTime)
    is_deleted = Column(Boolean)
    created = Column(DateTime)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)


class Sta_channel(Base):
    __tablename__ = "sta_channels"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    name = Column(String)
    description = Column(String)
    icon_path = Column(String)
    url_channel = Column(String)
    category_id = Column(Integer)
    country_id = Column(Integer)
    code = Column(String)
    is_enabled = Column(Boolean)
    channel_status_id = Column(Integer)
    is_hide_statistics = Column(Boolean)
    channel_public_id = Column(Integer)
    channel_comment_id = Column(Integer)
    can_download = Column(Boolean)
    can_like = Column(Boolean)
    canceled_date = Column(DateTime)
    deleted_date = Column(DateTime)
    count_like = Column(Integer)
    count_share = Column(Integer)
    count_listen = Column(Integer)
    count_comment = Column(Integer)
    object_key = Column(String)

class Sta_station_member_waitings(Base):
    __tablename__ = "sta_station_member_waitings"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    station_id = Column(Integer)
    email = Column(String)
    station_role_id = Column(Integer)
    unique_link = Column(String)
    expire_time = Column(DateTime)

class Sta_channel_member_waitings(Base):
    __tablename__ = "sta_channel_member_waitings"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    channel_id = Column(Integer)
    email = Column(String)
    channel_role_id = Column(Integer)
    unique_link = Column(String)
    expire_time = Column(DateTime)

class Sta_station_channel(Base):
    __tablename__ = "sta_station_channels"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    station_id = Column(Integer)
    channel_id = Column(Integer)
    contract_name = Column(String)
    contract_number = Column(String)
    station_channel_invite_status_id = Column(Integer)
    invite_date = Column(DateTime)
    contract_date_start = Column(Date)
    contract_date_end = Column(Date)
    accept_date = Column(DateTime)

class Stat_customer_detail(Base):
    __tablename__ = "stat_customer_details"
    __table_args__ = {'schema' : 'stat'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    stat_customer_id = Column(Integer)
    customer_id = Column(Integer)
    status_online = Column(Integer)
    activity = Column(Integer)

class Stat_customer_action_detail(Base):
    __tablename__ = "stat_customer_action_details"
    __table_args__ = {'schema' : 'stat'}
    id = Column(Integer,primary_key=True,nullable=True)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    station_id = Column(Integer)
    schedule_id = Column(Integer)
    period_id = Column(Integer)
    customer_id = Column(Integer)
    action_type_id = Column(Integer)
    action_date = Column(DateTime)
    action_time = Column(Time)
    is_active = Column(Boolean)
    uuid = Column(String)




class Sta_message_groups(Base):
    __tablename__ = "sta_message_groups"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,Sequence('sta_message_groups_id_seq'),primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    station_id = Column(Integer)
    channel_id = Column(Integer)
    name = Column(String)
    description = Column(String)
    form_member_id = Column(Integer)
    receive_member_id = Column(Integer)
    message_type_id = Column(Integer)
    message_status_id = Column(Integer)
    object = Column(String)
    reference_id = Column(Integer)
    message_mode = Column(String)
    is_attach_file = Column(Boolean)
    form_customer_id = Column(Integer)
    ticket_id = Column(String)
    request_id = Column(Integer)
    is_read = Column(Boolean)



class Sta_message_files(Base):
    __tablename__ = "sta_message_files"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    message_id = Column(Integer)
    file_name = Column(String)
    file_path = Column(String)
    file_type = Column(String)
    file_size = Column(String)
    object_key  = Column(String)


class Sta_message_statuses(Base):
    __tablename__ = "sta_message_statuses"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    name = Column(String)


class Sta_message_type(Base):
    __tablename__ = "sta_message_types"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    name = Column(String)
    description = Column(String)
    tag_color = Column(String)

class Stat_customer_interest(Base):
    __tablename__ = "stat_customer_interests"
    __table_args__ = {'schema' : 'stat'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_active = Column(Boolean)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    station_id = Column(Integer)
    schedule_id = Column(Integer)
    customer_id = Column(Integer)
    period_id = Column(Integer)


class Sta_period_categories(Base):
    __tablename__ = "sta_period_categories"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean)
    name = Column(String)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    description = Column(String)
    sort = Column(Integer)
    name_th = Column(String)
    name_en = Column(String)
    name_lo = Column(String)


class Sta_broadcast_type(Base):
    __tablename__ = "sta_broadcast_types"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean)
    name = Column(String)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)

class Sta_playlist(Base):
    __tablename__ = "sta_playlists"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean)
    name = Column(String)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    description = Column(String)
    time_duration = Column(String)
    count_file = Column(Integer)
    station_id = Column(Integer)
    channel_id = Column(Integer)
    icon_path = Column(String)
    artist = Column(String)
    album = Column(String)
    object_key = Column(String)


class Sta_package_detail(Base):
    __tablename__ = "sta_package_details"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean)
    name_th = Column(String)
    name_en = Column(String)
    name_lo = Column(String)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    package_group_id = Column(Integer)
    sort = Column(Integer)


class Sta_package_group(Base):
    __tablename__ = "sta_package_groups"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean)
    name = Column(String)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    detail_th = Column(String)
    detail_en = Column(String)
    detail_lo = Column(String)
    detail_footer_th = Column(String)
    detail_footer_en = Column(String)
    detail_footer_lo = Column(String)


class Sta_partner(Base):
    __tablename__ = "sta_partners"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean)
    name = Column(String)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    icon_path = Column(String)
    object_key = Column(String)
    sort = Column(Integer)


class Sta_help_type(Base):
    __tablename__ = "sta_help_types"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean)
    name = Column(String)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)


class Sta_report_type(Base):
    __tablename__ = "sta_report_types"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean)
    name = Column(String)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    name_th = Column(String)
    name_en = Column(String)
    name_lo = Column(String)


class Sta_request(Base):
    __tablename__ = "sta_requests"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,Sequence('sta_requests_id_seq'),primary_key=True,nullable=True)
    is_deleted = Column(Boolean)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    ticket_id = Column(Integer)
    help_type_id = Column(Integer)
    report_type_id = Column(Integer)
    country_id = Column(Integer)
    email = Column(String)
    link = Column(String)
    description = Column(Text)
    file_name = Column(String)
    file_path = Column(String)
    file_type = Column(String)  
    file_size = Column(String)
    object_key = Column(String)


class Sta_support_groups(Base):
    __tablename__ = "sta_support_groups"
    __table_args__ = {'schema': 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    topic_th = Column(String)
    topic_en = Column(String)
    topic_lo = Column(String)
    description_th = Column(String)
    description_en = Column(String)
    description_lo = Column(String)
    sort = Column(Integer)

class Sta_support_detail(Base):
    __tablename__ = "sta_support_details"
    __table_args__ = {'schema': 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    topic_th = Column(String)
    topic_en = Column(String)
    topic_lo = Column(String)
    description_th = Column(String)
    description_en = Column(String)
    description_lo = Column(String)
    parent_id = Column(Integer)
    support_group_id = Column(Integer)
    link = Column(String)


class Sta_channel_playlists(Base):
    __tablename__ = "sta_channel_playlists"
    __table_args__ = {'schema': 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    channel_period_id = Column(Integer)
    channel_playlist_history_id = Column(Integer)
    file_name = Column(String)
    file_path = Column(Text)
    file_type = Column(Text)
    file_size = Column(Text)
    time_duration = Column(String)
    order = Column(Integer)
    audit_status_id = Column(Integer)
    object_key = Column(String)
    source_ref = Column(String)
    bpm = Column(Numeric)


class Sta_channel_periods(Base):
    __tablename__ = "sta_channel_periods"
    __table_args__ = {'schema' : 'nrc'}
    id = Column(Integer,primary_key=True,nullable=True)
    is_deleted = Column(Boolean,default=False)
    created = Column(DateTime,nullable=True)
    created_by = Column(Integer)
    modified = Column(DateTime)
    modified_by = Column(Integer)
    channel_schedule_id = Column(Integer)
    name = Column(String)
    icon_path = Column(String)
    period_type_id = Column(Integer)
    period_time_id = Column(Integer)
    period_time_start = Column(Time)
    period_time_end = Column(Time)
    run_date = Column(Date)
    run_time = Column(Time)
    audit_status_id = Column(Integer)
    channel_id = Column(Integer)
    icon_object_key = Column(String)
    time_duration = Column(String)
    period_category_id = Column(Integer)
    is_copy = Column(Boolean)

# model คือตัวแทน Table
