from pydantic import BaseModel, field_validator, EmailStr
from datetime import datetime
import re

class Contact(BaseModel):
    email: EmailStr
    phone: str
    linkedin: str | None = None
    
    @field_validator('phone')
    def validate_phone(cls, v):
        if v and not re.match(r'^\+?\d{10,15}$', v):
            raise ValueError('Invalid phone number format')
        return v
    
    
    @field_validator('linkedin')
    def validate_linkedin(cls, v):
        if v and not re.match(r'^https://www.linkedin.com/in/.+$', v):
            raise ValueError('Invalid LinkedIn URL')
        return v

class Person(BaseModel):
    _id: str | None = None
    name : str
    birthday : str
    position : str
    contact : Contact
    description : str
    
    @field_validator('birthday')
    def validate_birthday(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')  # Adjust format as needed
        except ValueError:
            raise ValueError("birthday must be in the format YYYY-MM-DD")
        return v
    
