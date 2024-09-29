from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn

from middlewares.error404 import Error404Middleware

from routers.users import app as user_router

app = FastAPI(
    title='Referral system API',
    version='0.0.1',
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_headers=['*'],
    allow_methods=['*']
)

app.add_middleware(
    Error404Middleware
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({'detail': exc.errors()})
    )
    
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({'detail': exc.detail})
    )

@app.get('/', tags=['No API'], name='Root', status_code=302)
def root():
    return RedirectResponse('/docs')
    
@app.get('/error404', tags=['No API', 'Errors'], name='Error 404', status_code=200)
def root():
    return HTMLResponse(
        content='''
            <div style="width:100%;text-align:center;">
                <h3>Page not found!</h3>
            </div>
        '''
    )
    
app.include_router(user_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8001, reload=True)
