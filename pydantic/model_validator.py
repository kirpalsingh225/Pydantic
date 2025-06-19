from pydantic import BaseModel, Field, AnyUrl, EmailStr, model_validator
from typing import List, Optional, Annotated, Dict


class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    weight: float
    married: bool
    allergies: List[str]
    contact: Dict[str, str]
    
    @model_validator(mode="after")
    def emergency_contact(cls, model):
        if model.age > 60 and "emergency_contact" not in model.contact:
            raise ValueError("Emergency contact is required for patients over 60 years old.")
        return model
    
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