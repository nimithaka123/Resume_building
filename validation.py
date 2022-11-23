from pydantic import BaseModel,validator, Field
from typing import Annotated
from datetime import date
import re

class Basic_Details(BaseModel):
    name:str
    email:str
    phone:str
    image:str
    summary:str

    class Config:
        orm_mode = True

    @validator('name')
    def is_valid_name(cls, val):
        if len(val) < 3:
            raise ValueError("Name should be atleast 3 characters")
        return val

    @validator("email")
    def check_email_format(cls, v):
        reg = r"^[A-Za-z0-9-.]+@([A-Za-z0-9-]+\.)+[\w-]{2,4}$"
        if not re.match(reg, v):
            raise ValueError("Invalid email id")
        return v


    @validator("phone")
    def check_phoneNumber_format(cls, v):
        regExs = r"^\(?(\d{3})\)?[- ]?(\d{3})[- ]?(\d{4})$"
        if not re.match(regExs, v):
            raise ValueError("Invalid phone no.")
        return v

   










