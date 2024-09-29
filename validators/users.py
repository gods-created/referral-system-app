from pydantic import BaseModel, Field, EmailStr

class Data(BaseModel):
    ref: str = Field(default='NONE')
    email: EmailStr = Field(default='example@gmail.com')
    
    def to_json(self):
        return {
            'ref': self.ref,
            'email': self.email
        }
