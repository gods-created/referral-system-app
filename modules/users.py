import copy
import os
import string
import random
from loguru import logger
from abc import ABC, abstractmethod
import sqlalchemy
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from models.users import Users as Users_Model
from models.users import Referrals, user_referral

from tasks.main import add_bonuse

class Base(ABC):
    @abstractmethod
    def select_user(self):
        pass
        
    @abstractmethod
    def insert_user(self):
        pass

class Users(Base):
    def __init__(self):
        self.st_response_json = {
            'status': 'error',
            'err_description': ''
        }
        
    def __enter__(self, *args, **kwargs):
        self.session = Session(
            create_engine(
                os.environ.get('DB_HOST'),
                echo=False
            )
        )
        
        return self
            
    def __generate_refferal(self) -> str:
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
            
    def select_user(self, email: str) -> dict:
        response_json = copy.deepcopy(self.st_response_json)
        
        try:
            stmt = select(Users_Model).where(Users_Model.email == email).join(user_referral)
            for row in self.session.scalars(stmt):
                user = row.to_json()
                response_json['user'] = user
                
            response_json['status'] = 'success'
            
        except Exception as e:
            response_json['err_description'] = str(e)
            
        finally:
            logger.info(response_json)
            return response_json
            
    def insert_user(self, ref: str, email: str) -> dict:
        response_json = copy.deepcopy(self.st_response_json)
        
        try:
            refferal = self.__generate_refferal()
            
            add_new_referral = Referrals(
                value=refferal
            )
            
            add_new_user = Users_Model(
                email=email,
            )
            
            self.session.add(add_new_user)
            self.session.commit()
            
            add_new_referral.user_id = add_new_user.id
            self.session.add(add_new_referral)
            self.session.commit()
            
            add_new_user.referral = add_new_referral
            add_new_referral.user = add_new_user
            self.session.commit()
            
            select_user_response = self.select_user(email)
            response_json['user'] = select_user_response.get('user', {})
            response_json['status'] = 'success'
            
        except sqlalchemy.exc.IntegrityError as e:
            self.session.rollback()
            message = 'This email already exists!' if 'duplicate' in str(e).lower() else str(e)
            response_json['err_description'] = message
            
        except Exception as e:
            self.session.rollback()
            response_json['err_description'] = str(e)
            
        finally:
            if ref != 'NONE' and response_json['status'] == 'success':
                add_bonuse.apply_async(
                    (ref, ),
                    queue='high_priority'
                )
                
            logger.info(response_json)
            return response_json
            
    def __exit__(self, *args, **kwargs):
        self.session.close()
