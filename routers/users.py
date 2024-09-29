from fastapi import APIRouter
from fastapi.responses import JSONResponse
from validators.users import Data

from modules.users import Users

app = APIRouter(
    prefix='/users',
    tags=['API']
)

@app.post('/insert_user', name='Insert user', status_code=200)
def insert_user(data: Data) -> dict:
    with Users() as module:
        data = data.to_json()
        
        response = module.insert_user(
            data.get('ref'),
            data.get('email')
        )
        
    return JSONResponse(content=response)
