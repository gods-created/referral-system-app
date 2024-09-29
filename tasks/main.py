import os
from celery import Celery
from typing import Callable
from loguru import logger
import sqlalchemy
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from models.users import user_referral, Users

app = Celery(
    'main',
    broker=os.environ.get('REDIS_HOST')
)

app.conf.task_queues = {
    'high_priority': {
        'exchange': 'high_priority',
        'routing_key': 'high.#',
    },
    'loq_priority': {
        'exchange': 'loq_priority',
        'routing_key': 'low.#',
    }
}

@app.task
def add_bonuse(ref: str, *args) -> dict:
    response_json = {
        'status': 'error',
        'err_description': ''
    }
    
    try:
        session = Session(
            create_engine(
                os.environ.get('DB_HOST'),
                echo=False
            )
        )
        
        stmt = select(Users).join(user_referral)
        for user in session.scalars(stmt):
            if user.referral.value == ref:
                user.bonuse += 1
                session.commit()
                break
        
        response_json['status'] = 'success'
        
    except Exception as e:
        session.rollback()
        response_json['err_description'] = str(e)
        
    finally:
        session.close()
        logger.info(response_json)
        return response_json
