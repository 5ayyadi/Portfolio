from pydantic import BaseModel, field_validator, ValidationInfo
from datetime import datetime
from errors.error_handler import WrongInput
class Education(BaseModel):
    institution : str
    degree : str
    start : str
    end : str | None = None
    desc : str
    
    @field_validator('start', 'end', mode="before")
    def validate_dates(cls, v, info: ValidationInfo):
        if v is None and info.field_name == "end":
            return v
        
        if v:
            try:
                datetime.strptime(v, '%Y-%m') 
            except ValueError:
                raise WrongInput
        
        return v
