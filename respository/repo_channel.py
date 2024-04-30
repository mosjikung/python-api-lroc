from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, null,or_ ,func , cast ,Date ,asc ,case


from datetime import datetime, timedelta ,date
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM


from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from model import (Sta_station,
                   Sta_station_channel,
                   Sta_channel,
                   Member,
                   Sta_channel_playlists,
                   Sta_channel_periods,
                   Countries
                   )

import pdb



T = TypeVar("T")
class BaseRepo:
              @staticmethod
              def get_data_station_channels(db:Session,
                                   station_channel:Sta_station_channel,
                                   station:Sta_station,
                                   member:Member,
                                   channel:Sta_channel,
                                   offset:int,
                                   limit:int,
                                   keyword:str,
                                   ):
                            first_name = None
                            last_name = None
                            if keyword is not None:
                                         
                                          search = "%{}%".format(keyword)
                            
                            if keyword is None:
                                          sql = (db.query(station_channel,station,member,channel)
                                          .join(station, station_channel.station_id == station.id)
                                          .join(channel, station_channel.channel_id == channel.id)
                                          .join(member, station_channel.created_by == member.id)
                                          .filter(station_channel.is_deleted == 'f')
                                          .filter(station_channel.station_channel_invite_status_id == 2)
                                          .filter(station.approve_status_id == 1)
                                          .filter(channel.channel_status_id == 1)
                                          .filter(station.is_deleted == 'f')
                                          .filter(channel.is_deleted == 'f')
                                          .filter(member.is_deleted == 'f')
                                          .group_by(member.id,
                                                        member.username,
                                                        member.first_name,
                                                        member.last_name,
                                                        member.email_verify,
                                                        member.display_name,
                                                        channel.id,
                                                        channel.name,
                                                        channel.icon_path,
                                                        channel.url_channel,
                                                        station.id,
                                                        station.name,
                                                        station.icon_path,
                                                        station_channel.accept_date,
                                                        member.member_type_id,
                                                        station_channel.id)
                                          .order_by(asc(station.id),asc(channel.id))
                                          .offset(offset)
                                          .limit(limit)
                                          .all()
                                          )
                                          
                                          return sql
                            elif keyword is not None:
                                          
                                          sql = (db.query(station_channel,station,member,channel)
                                                        .join(station, station_channel.station_id == station.id)
                                                        .join(channel, station_channel.channel_id == channel.id)
                                                        .join(member, station_channel.created_by == member.id)
                                                        .filter(station_channel.is_deleted == 'f')
                                                        .filter(station_channel.station_channel_invite_status_id == 2)
                                                        .filter(station.approve_status_id == 1)
                                                        .filter(channel.channel_status_id == 1)
                                                        .filter(station.is_deleted == 'f')
                                                        .filter(channel.is_deleted == 'f')
                                                        .filter(member.is_deleted == 'f')
                                                        .filter(or_(
                                                        channel.name.ilike(search),
                                                        station.name.ilike(search),
                                                        member.first_name.ilike(search),
                                                        member.last_name.ilike(search),
                                                        func.concat(member.first_name, " ", member.last_name).ilike(search),
                                                        func.concat(member.first_name, "  ", member.last_name).ilike(search)
                                                        ))
                                                        .group_by(member.id,
                                                                      member.username,
                                                                      member.first_name,
                                                                      member.last_name,
                                                                      member.email_verify,
                                                                      member.display_name,
                                                                      channel.id,
                                                                      channel.name,
                                                                      channel.icon_path,
                                                                      channel.url_channel,
                                                                      station.id,
                                                                      station.name,
                                                                      station.icon_path,
                                                                      station_channel.accept_date,
                                                                      member.member_type_id,
                                                                      station_channel.id)
                                                        .order_by(asc(station.id),asc(channel.id))
                                                        .offset(offset)
                                                        .limit(limit)
                                                        .all()
                                                        )
                            

                            return sql
              
              @staticmethod
              def get_count_data_station_channel(db:Session,
                                   station_channel:Sta_station_channel,
                                   station:Sta_station,
                                   member:Member,
                                   channel:Sta_channel,
                                   keyword:str,
                                   ):
                            first_name = None
                            last_name = None
                            if keyword is not None:
                                         
                                          search = "%{}%".format(keyword)
                            
                            if keyword is None:
                                          sql = (db.query(station_channel,station,member,channel)
                                          .join(station, station_channel.station_id == station.id)
                                          .join(channel, station_channel.channel_id == channel.id)
                                          .join(member, station_channel.created_by == member.id)
                                          .filter(station_channel.is_deleted == 'f')
                                          .filter(station_channel.station_channel_invite_status_id == 2)
                                          .filter(station.approve_status_id == 1)
                                          .filter(channel.channel_status_id == 1)
                                          .filter(station.is_deleted == 'f')
                                          .filter(channel.is_deleted == 'f')
                                          .filter(member.is_deleted == 'f')
                                          .group_by(member.id,
                                                        member.username,
                                                        member.first_name,
                                                        member.last_name,
                                                        member.email_verify,
                                                        member.display_name,
                                                        channel.id,
                                                        channel.name,
                                                        channel.icon_path,
                                                        channel.url_channel,
                                                        station.id,
                                                        station.name,
                                                        station.icon_path,
                                                        station_channel.accept_date,
                                                        member.member_type_id,
                                                        station_channel.id)
                                          .order_by(asc(station.id),asc(channel.id))
                                          .count()
                                          )
                                          
                                          return sql
                            elif keyword is not None:
                                          
                                          sql = (db.query(station_channel,station,member,channel)
                                                        .join(station, station_channel.station_id == station.id)
                                                        .join(channel, station_channel.channel_id == channel.id)
                                                        .join(member, station_channel.created_by == member.id)
                                                        .filter(station.approve_status_id == 1)
                                                        .filter(station.is_deleted == 'f')
                                                        .filter(channel.is_deleted == 'f')
                                                        .filter(channel.channel_status_id == 1)
                                                        .filter(member.is_deleted == 'f')
                                                        .filter(station_channel.station_channel_invite_status_id == 1)
                                                        .filter(or_(
                                                        channel.name.ilike(search),
                                                        station.name.ilike(search),
                                                        member.first_name.ilike(search),
                                                        member.last_name.ilike(search),
                                                        func.concat(member.first_name, " ", member.last_name).ilike(search),
                                                        func.concat(member.first_name, "  ", member.last_name).ilike(search)
                                                        ))
                                                        .group_by(member.id,
                                                                      member.username,
                                                                      member.first_name,
                                                                      member.last_name,
                                                                      member.email_verify,
                                                                      member.display_name,
                                                                      channel.id,
                                                                      channel.name,
                                                                      channel.icon_path,
                                                                      channel.url_channel,
                                                                      station.id,
                                                                      station.name,
                                                                      station.icon_path,
                                                                      station_channel.accept_date,
                                                                      member.member_type_id,
                                                                      station_channel.id)
                                                        .order_by(asc(station.id),asc(channel.id))
                                                        .count()
                                                        )
                              
                            
                            return sql
              
              @staticmethod
              def get_count_data_station_channel_none_keyword(db:Session,
                                   station_channel:Sta_station_channel,
                                   station:Sta_station,
                                   member:Member,
                                   channel:Sta_channel,
                                   ):
                           
                            
                            sql = (db.query(station_channel,station,member,channel)
                            .join(station, station_channel.station_id == station.id)
                            .join(channel, station_channel.channel_id == channel.id)
                            .join(member, station_channel.created_by == member.id)
                            .filter(station_channel.is_deleted == 'f')
                            .filter(station_channel.station_channel_invite_status_id == 2)
                            .filter(station.approve_status_id == 1)
                            .filter(channel.channel_status_id == 1)
                            .filter(station.is_deleted == 'f')
                            .filter(channel.is_deleted == 'f')
                            .filter(member.is_deleted == 'f')
                            .group_by(member.id,
                                          member.username,
                                          member.first_name,
                                          member.last_name,
                                          member.email_verify,
                                          member.display_name,
                                          channel.id,
                                          channel.name,
                                          channel.icon_path,
                                          channel.url_channel,
                                          station.id,
                                          station.name,
                                          station.icon_path,
                                          station_channel.accept_date,
                                          member.member_type_id,
                                          station_channel.id)
                            .order_by(asc(station.id),asc(channel.id))
                            .count()
                            )
                            
                            return sql
              


              @staticmethod
              def get_data_station_channels_delete(db:Session,
                                   station_channel:Sta_station_channel,
                                   station:Sta_station,
                                   member:Member,
                                   channel:Sta_channel,
                                   offset:int,
                                   limit:int,
                                   keyword:str,
                                   ):
                            first_name = None
                            last_name = None
                            if keyword is not None:
                                         
                                          search = "%{}%".format(keyword)
                            
                            if keyword is None:
                                          sql = (db.query(station_channel,station,member,channel)
                                          .join(station, station_channel.station_id == station.id)
                                          .join(channel, station_channel.channel_id == channel.id)
                                          .join(member, station_channel.created_by == member.id)
                                          .filter(station_channel.is_deleted == 'f')
                                          .filter(station_channel.station_channel_invite_status_id == 2)
                                          .filter(station.approve_status_id == 1)
                                          .filter(channel.channel_status_id == 3)
                                          .filter(station.is_deleted == 'f')
                                          .filter(channel.is_deleted == 't')
                                          .filter(member.is_deleted == 'f')
                                          .group_by(member.id,
                                                        member.username,
                                                        member.first_name,
                                                        member.last_name,
                                                        member.email_verify,
                                                        member.display_name,
                                                        channel.id,
                                                        channel.name,
                                                        channel.icon_path,
                                                        channel.url_channel,
                                                        station.id,
                                                        station.name,
                                                        station.icon_path,
                                                        station_channel.accept_date,
                                                        member.member_type_id,
                                                        station_channel.id)
                                          .order_by(asc(station.id),asc(channel.id))
                                          .offset(offset)
                                          .limit(limit)
                                          .all()
                                          )
                                          
                                          return sql
                            elif keyword is not None:
                                          
                                          sql = (db.query(station_channel,station,member,channel)
                                                        .join(station, station_channel.station_id == station.id)
                                                        .join(channel, station_channel.channel_id == channel.id)
                                                        .join(member, station_channel.created_by == member.id)
                                                        .filter(station_channel.is_deleted == 'f')
                                                        .filter(station_channel.station_channel_invite_status_id == 2)
                                                        .filter(station.approve_status_id == 1)
                                                        .filter(channel.channel_status_id == 3)
                                                        .filter(station.is_deleted == 'f')
                                                        .filter(channel.is_deleted == 't')
                                                        .filter(member.is_deleted == 'f')
                                                        .filter(or_(
                                                        channel.name.ilike(search),
                                                        station.name.ilike(search),
                                                        member.first_name.ilike(search),
                                                        member.last_name.ilike(search),
                                                        func.concat(member.first_name, " ", member.last_name).ilike(search),
                                                        func.concat(member.first_name, "  ", member.last_name).ilike(search)
                                                        ))
                                                        .group_by(member.id,
                                                                      member.username,
                                                                      member.first_name,
                                                                      member.last_name,
                                                                      member.email_verify,
                                                                      member.display_name,
                                                                      channel.id,
                                                                      channel.name,
                                                                      channel.icon_path,
                                                                      channel.url_channel,
                                                                      station.id,
                                                                      station.name,
                                                                      station.icon_path,
                                                                      station_channel.accept_date,
                                                                      member.member_type_id,
                                                                      station_channel.id)
                                                        .order_by(asc(station.id),asc(channel.id))
                                                        .offset(offset)
                                                        .limit(limit)
                                                        .all()
                                                        )
                                          
                           
                            return sql
              
              @staticmethod
              def get_count_data_station_channel_delete(db:Session,
                                   station_channel:Sta_station_channel,
                                   station:Sta_station,
                                   member:Member,
                                   channel:Sta_channel,
                                   keyword:str,
                                   ):
                            first_name = None
                            last_name = None
                            if keyword is not None:
                                         
                                          search = "%{}%".format(keyword)
                            
                            if keyword is None:
                                          sql = (db.query(station_channel,station,member,channel)
                                          .join(station, station_channel.station_id == station.id)
                                          .join(channel, station_channel.channel_id == channel.id)
                                          .join(member, station_channel.created_by == member.id)
                                          .filter(station_channel.is_deleted == 'f')
                                          .filter(station_channel.station_channel_invite_status_id == 2)
                                          .filter(station.approve_status_id == 1)
                                          .filter(channel.channel_status_id == 3)
                                          .filter(station.is_deleted == 'f')
                                          .filter(channel.is_deleted == 'f')
                                          .filter(member.is_deleted == 'f')
                                          .group_by(member.id,
                                                        member.username,
                                                        member.first_name,
                                                        member.last_name,
                                                        member.email_verify,
                                                        member.display_name,
                                                        channel.id,
                                                        channel.name,
                                                        channel.icon_path,
                                                        channel.url_channel,
                                                        station.id,
                                                        station.name,
                                                        station.icon_path,
                                                        station_channel.accept_date,
                                                        member.member_type_id,
                                                        station_channel.id)
                                          .order_by(asc(station.id),asc(channel.id))
                                          .count()
                                          )
                                          
                                          return sql
                            elif keyword is not None:
                                          
                                          sql = (db.query(station_channel,station,member,channel)
                                                        .join(station, station_channel.station_id == station.id)
                                                        .join(channel, station_channel.channel_id == channel.id)
                                                        .join(member, station_channel.created_by == member.id)
                                                        .filter(station.approve_status_id == 1)
                                                        .filter(station.is_deleted == 'f')
                                                        .filter(channel.is_deleted == 'f')
                                                        .filter(channel.channel_status_id == 1)
                                                        .filter(member.is_deleted == 'f')
                                                        .filter(station_channel.station_channel_invite_status_id == 3)
                                                        .filter(or_(
                                                        channel.name.ilike(search),
                                                        station.name.ilike(search),
                                                        member.first_name.ilike(search),
                                                        member.last_name.ilike(search),
                                                        func.concat(member.first_name, " ", member.last_name).ilike(search),
                                                        func.concat(member.first_name, "  ", member.last_name).ilike(search)
                                                        ))
                                                        .group_by(member.id,
                                                                      member.username,
                                                                      member.first_name,
                                                                      member.last_name,
                                                                      member.email_verify,
                                                                      member.display_name,
                                                                      channel.id,
                                                                      channel.name,
                                                                      channel.icon_path,
                                                                      channel.url_channel,
                                                                      station.id,
                                                                      station.name,
                                                                      station.icon_path,
                                                                      station_channel.accept_date,
                                                                      member.member_type_id,
                                                                      station_channel.id)
                                                        .order_by(asc(station.id),asc(channel.id))
                                                        .count()
                                                        )
                                          
                           
                            return sql
              
              @staticmethod
              def get_count_data_station_channel_delete_none_keyword(db:Session,
                                   station_channel:Sta_station_channel,
                                   station:Sta_station,
                                   member:Member,
                                   channel:Sta_channel,
                                   ):
                           
                            
                            sql = (db.query(station_channel,station,member,channel)
                            .join(station, station_channel.station_id == station.id)
                            .join(channel, station_channel.channel_id == channel.id)
                            .join(member, station_channel.created_by == member.id)
                            .filter(station_channel.is_deleted == 'f')
                            .filter(station_channel.station_channel_invite_status_id == 2)
                            .filter(station.approve_status_id == 1)
                            .filter(channel.channel_status_id == 3)
                            .filter(station.is_deleted == 'f')
                            .filter(channel.is_deleted == 'f')
                            .filter(member.is_deleted == 'f')
                            .group_by(member.id,
                                          member.username,
                                          member.first_name,
                                          member.last_name,
                                          member.email_verify,
                                          member.display_name,
                                          channel.id,
                                          channel.name,
                                          channel.icon_path,
                                          channel.url_channel,
                                          station.id,
                                          station.name,
                                          station.icon_path,
                                          station_channel.accept_date,
                                          member.member_type_id,
                                          station_channel.id)
                            .order_by(asc(station.id),asc(channel.id))
                            .count()
                            )
                            
                            return sql
              

              @staticmethod
              def get_data_station_channels_cancle(db:Session,
                                   station_channel:Sta_station_channel,
                                   station:Sta_station,
                                   member:Member,
                                   channel:Sta_channel,
                                   offset:int,
                                   limit:int,
                                   keyword:str,
                                   ):
                            first_name = None
                            last_name = None
                            if keyword is not None:
                                         
                                          search = "%{}%".format(keyword)
                            
                            if keyword is None:
                                          sql = (db.query(station_channel,station,member,channel)
                                          .join(station, station_channel.station_id == station.id)
                                          .join(channel, station_channel.channel_id == channel.id)
                                          .join(member, station_channel.created_by == member.id)
                                          .filter(station_channel.is_deleted == 'f')
                                          .filter(station_channel.station_channel_invite_status_id == 2)
                                          .filter(station.approve_status_id == 1)
                                          .filter(channel.channel_status_id == 2)
                                          .filter(station.is_deleted == 'f')
                                          .filter(channel.is_deleted == 'f')
                                          .filter(member.is_deleted == 'f')
                                          .group_by(member.id,
                                                        member.username,
                                                        member.first_name,
                                                        member.last_name,
                                                        member.email_verify,
                                                        member.display_name,
                                                        channel.id,
                                                        channel.name,
                                                        channel.icon_path,
                                                        channel.url_channel,
                                                        station.id,
                                                        station.name,
                                                        station.icon_path,
                                                        station_channel.accept_date,
                                                        member.member_type_id,
                                                        station_channel.id)
                                          .order_by(asc(station.id),asc(channel.id))
                                          .offset(offset)
                                          .limit(limit)
                                          .all()
                                          )
                                          
                                          return sql
                            elif keyword is not None:
                                          
                                          sql = (db.query(station_channel,station,member,channel)
                                                        .join(station, station_channel.station_id == station.id)
                                                        .join(channel, station_channel.channel_id == channel.id)
                                                        .join(member, station_channel.created_by == member.id)
                                                        .filter(station_channel.is_deleted == 'f')
                                                        .filter(station_channel.station_channel_invite_status_id == 2)
                                                        .filter(station.approve_status_id == 1)
                                                        .filter(channel.channel_status_id == 2)
                                                        .filter(station.is_deleted == 'f')
                                                        .filter(channel.is_deleted == 'f')
                                                        .filter(member.is_deleted == 'f')
                                                        .filter(or_(
                                                        channel.name.ilike(search),
                                                        station.name.ilike(search),
                                                        member.first_name.ilike(search),
                                                        member.last_name.ilike(search),
                                                        func.concat(member.first_name, " ", member.last_name).ilike(search),
                                                        func.concat(member.first_name, "  ", member.last_name).ilike(search)
                                                        ))
                                                        .group_by(member.id,
                                                                      member.username,
                                                                      member.first_name,
                                                                      member.last_name,
                                                                      member.email_verify,
                                                                      member.display_name,
                                                                      channel.id,
                                                                      channel.name,
                                                                      channel.icon_path,
                                                                      channel.url_channel,
                                                                      station.id,
                                                                      station.name,
                                                                      station.icon_path,
                                                                      station_channel.accept_date,
                                                                      member.member_type_id,
                                                                      station_channel.id)
                                                        .order_by(asc(station.id),asc(channel.id))
                                                        .offset(offset)
                                                        .limit(limit)
                                                        .all()
                                                        )
                                          
                           
                            return sql
              
              @staticmethod
              def get_count_data_station_channel_cancle(db:Session,
                                   station_channel:Sta_station_channel,
                                   station:Sta_station,
                                   member:Member,
                                   channel:Sta_channel,
                                   keyword:str,
                                   ):
                            first_name = None
                            last_name = None
                            if keyword is not None:
                                         
                                          search = "%{}%".format(keyword)
                            
                            if keyword is None:
                                          sql = (db.query(station_channel,station,member,channel)
                                          .join(station, station_channel.station_id == station.id)
                                          .join(channel, station_channel.channel_id == channel.id)
                                          .join(member, station_channel.created_by == member.id)
                                          .filter(station_channel.is_deleted == 'f')
                                          .filter(station_channel.station_channel_invite_status_id == 2)
                                          .filter(station.approve_status_id == 1)
                                          .filter(channel.channel_status_id == 2)
                                          .filter(station.is_deleted == 'f')
                                          .filter(channel.is_deleted == 'f')
                                          .filter(member.is_deleted == 'f')
                                          .group_by(member.id,
                                                        member.username,
                                                        member.first_name,
                                                        member.last_name,
                                                        member.email_verify,
                                                        member.display_name,
                                                        channel.id,
                                                        channel.name,
                                                        channel.icon_path,
                                                        channel.url_channel,
                                                        station.id,
                                                        station.name,
                                                        station.icon_path,
                                                        station_channel.accept_date,
                                                        member.member_type_id,
                                                        station_channel.id)
                                          .order_by(asc(station.id),asc(channel.id))
                                          .count()
                                          )
                                          
                                          return sql
                            elif keyword is not None:
                                          
                                          sql = (db.query(station_channel,station,member,channel)
                                                        .join(station, station_channel.station_id == station.id)
                                                        .join(channel, station_channel.channel_id == channel.id)
                                                        .join(member, station_channel.created_by == member.id)
                                                        .filter(station_channel.is_deleted == 'f')
                                                        .filter(station_channel.station_channel_invite_status_id == 2)
                                                        .filter(station.approve_status_id == 1)
                                                        .filter(channel.channel_status_id == 2)
                                                        .filter(station.is_deleted == 'f')
                                                        .filter(channel.is_deleted == 'f')
                                                        .filter(member.is_deleted == 'f')
                                                        .filter(or_(
                                                        channel.name.ilike(search),
                                                        station.name.ilike(search),
                                                        member.first_name.ilike(search),
                                                        member.last_name.ilike(search),
                                                        func.concat(member.first_name, " ", member.last_name).ilike(search),
                                                        func.concat(member.first_name, "  ", member.last_name).ilike(search)
                                                        ))
                                                        .group_by(member.id,
                                                                      member.username,
                                                                      member.first_name,
                                                                      member.last_name,
                                                                      member.email_verify,
                                                                      member.display_name,
                                                                      channel.id,
                                                                      channel.name,
                                                                      channel.icon_path,
                                                                      channel.url_channel,
                                                                      station.id,
                                                                      station.name,
                                                                      station.icon_path,
                                                                      station_channel.accept_date,
                                                                      member.member_type_id,
                                                                      station_channel.id)
                                                        .order_by(asc(station.id),asc(channel.id))
                                                        .count()
                                                        )
                                          
                           
                            return sql
              
              @staticmethod
              def get_count_data_station_channel_cancle_none_keyword(db:Session,
                                   station_channel:Sta_station_channel,
                                   station:Sta_station,
                                   member:Member,
                                   channel:Sta_channel,
                                   ):
                           
                            
                            sql = (db.query(station_channel,station,member,channel)
                            .join(station, station_channel.station_id == station.id)
                            .join(channel, station_channel.channel_id == channel.id)
                            .join(member, station_channel.created_by == member.id)
                            .filter(station_channel.is_deleted == 'f')
                            .filter(station_channel.station_channel_invite_status_id == 2)
                            .filter(station.approve_status_id == 1)
                            .filter(channel.channel_status_id == 2)
                            .filter(station.is_deleted == 'f')
                            .filter(channel.is_deleted == 'f')
                            .filter(member.is_deleted == 'f')
                            .group_by(member.id,
                                          member.username,
                                          member.first_name,
                                          member.last_name,
                                          member.email_verify,
                                          member.display_name,
                                          channel.id,
                                          channel.name,
                                          channel.icon_path,
                                          channel.url_channel,
                                          station.id,
                                          station.name,
                                          station.icon_path,
                                          station_channel.accept_date,
                                          member.member_type_id,
                                          station_channel.id)
                            .order_by(asc(station.id),asc(channel.id))
                            .count()
                            )
                            
                            return sql
              
              @staticmethod
              def get_data_prepair_update_cancel(db:Session,
                                          model:Generic[T],
                                          id:int,
                                          user_id:int,
                                          update_time:datetime
                                          ):
                      
                            sql = (db.query(model)
                                   .filter(model.id == id)
                                   .first()
                                   )
                            if sql is not None:
                                    sql.channel_status_id = 2
                                    sql.modified = update_time
                                    sql.modified_by = user_id

                            return sql
              

              @staticmethod
              def get_data_prepair_update_delete(db:Session,
                                          model:Generic[T],
                                          id:int,
                                          user_id:int,
                                          update_time:datetime
                                          ):
                      
                            sql = (db.query(model)
                                   .filter(model.id == id)
                                   .first()
                                   )
                            if sql is not None:
                                    sql.channel_status_id = 3
                                    sql.modified = update_time
                                    sql.modified_by = user_id
                                    sql.is_deleted = True

                            return sql
              
              
              @staticmethod
              def get_data_channel_by_id(db:Session,
                                         station_channel:Sta_station_channel,
                                         channel:Sta_channel,
                                         country:Countries,
                                         channel_id:int
                                         ):
                     
                     sql = (db.query(station_channel,channel,country)
                            .join(channel, station_channel.channel_id == channel.id)
                            .join(country, channel.country_id == country.id)
                            .filter(station_channel.is_deleted == 'f')
                            .filter(channel.is_deleted == 'f')
                            .filter(Sta_station_channel.channel_id == channel_id)
                            .all()
                            )
                     return sql
              
       
              @staticmethod
              def get_data_station(db:Session,
                                   model:Generic[T],
                                   id:int):
                     
                     sql = (db.query(model)
                            .filter(model.id == id)
                            .filter(model.is_deleted == 'f')
                            .all()
                            )
                     return sql
              
              @staticmethod
              def get_data_period(db:Session,
                                  channel_period:Sta_channel_periods,
                                  id:int):
                      
                     sql = (db.query(channel_period)
                            .filter(channel_period.channel_id == id)
                            .filter(channel_period.is_deleted == 'f')
                            .all()
                            )
                     return sql
              

              @staticmethod
              def get_data_playlist(db:Session,
                                  channel_playlist:Sta_channel_playlists,
                                  id:int):
                      
                     sql = (db.query(channel_playlist)
                            .filter(channel_playlist.channel_period_id == id)
                            .filter(channel_playlist.is_deleted == 'f')
                            .all()
                            )
                     return sql
              
              

              @staticmethod
              def insert(db: Session, model: Generic[T]):
                            db.add(model)
                            db.commit()
                            db.refresh(model)
                            return True


              @staticmethod
              def update(db: Session, model: Generic[T]):
                            db.commit()
                            db.refresh(model)
                            return True

              @staticmethod
              def delete(db: Session, model: Generic[T]):
                            db.delete(model)
                            db.commit()
                            return True

              @staticmethod
              def rollback(db: Session, model: Generic[T]):
                            db.rollback(model)
                            db.refresh(model)
                            return False
              

              