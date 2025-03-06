from pydantic import BaseModel, field_validator, EmailStr
from datetime import datetime
import re
from errors.error_handler import WrongInput

class Contact(BaseModel):
    email: EmailStr
    phone: str
    linkedin: str | None = None
    github: str | None = None
    
    @field_validator('phone')
    def validate_phone(cls, v):
        if v and not re.match(r'^\+?\d{10,15}$', v):
            raise WrongInput
        return v
    
    @field_validator('linkedin')
    def validate_linkedin(cls, v):
        if v and not re.match(r'^https://www.linkedin.com/in/.+$', v):
            raise WrongInput
        return v

class Person(BaseModel):
    name: str
    birthday: str
    position: str
    contact: Contact
    description: str
    
    @field_validator('birthday')
    def validate_birthday(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')  # Adjust format as needed
        except ValueError:
            raise WrongInput
        return v
