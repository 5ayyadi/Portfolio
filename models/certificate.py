from pydantic import BaseModel, field_validator
from datetime import datetime
from errors.error_handler import WrongInput

class Certificate(BaseModel):
    id: str | None = None
    name: str
    date: str
    desc: str
    
    @field_validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m') 
        except ValueError:
            raise WrongInput
        return v
