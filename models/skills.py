from pydantic import BaseModel, model_validator
from enum import IntEnum, StrEnum

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
    name: str
    level: SkillLevel
    tag: Tag
    level_name: str | None = None

    @model_validator(mode="before")
    def set_level_name(cls, values):
        level = values.get('level')
        if level is not None:
            values['level_name'] = SkillLevel(level).name
        return values
