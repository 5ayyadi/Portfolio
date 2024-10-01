from pydantic import BaseModel, field_validator
from enum import IntEnum
from enum import StrEnum


class SkillLevel(IntEnum):
    BEGINNER = 1
    NOVICE = 2
    INTERMEDIATE = 3
    ADVANCED = 4
    EXPERT = 5
    MASTER = 6
    

class Tag(StrEnum):
    LANGUAGE = "Language"
    FRAMEWORK = "Framework"
    CODE = "Code"
    TECHNOLOGY = "Technology"
    DATABASE = "Database"

class Skill(BaseModel):
    _id: str | None = None
    name : str
    level : SkillLevel
    level_name: str  
    tag: Tag

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level_name = self.level.name
