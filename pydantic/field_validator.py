from pydantic import BaseModel, Field, AnyUrl, EmailStr, field_validator
from typing import List, Optional, Annotated, Dict


class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    weight: float
    married: bool
    allergies: List[str]
    contact: Dict[str, str]

    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        valid_domains = ['icici.com', 'hdfc.com']

        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError(f"Email domain must be one of {valid_domains}")
        
        return value
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, value):
        return value.upper()
    
def update_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact)

    print("Patient updated successfully!")

patient_info = {
    "name": "John Doe",
    "age": 30,
    "email": "abc@abc.com",
    "weight": 70.5,
    "married": True,
    "allergies": ["penicillin", "nuts"],
    "contact": {
        "phone": "1234567890",
        "address": "123 Main St, City, Country"
    }}

patient1 = Patient(**patient_info) # type coersion happens here
update_patient(patient1)