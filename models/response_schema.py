from pydantic import BaseModel
from models.certificate import Certificate
from models.education import Education
from models.person import Person
from models.skills import Skill
from models.work_experience import Work
from typing import Any

class BaseResponse(BaseModel):
    msg: str = "OK"
    status_code: int = 200
    result: Any = None
    
class PersonResponse(BaseResponse):
    result: Person
    
class WorkResponse(BaseResponse):
    result: list[Work]
    
class EducationResponse(BaseResponse):
    result: list[Education]
    
class CertificateResponse(BaseResponse):
    result: list[Certificate]

class SkillResponse(BaseResponse):
    result: list[Skill]