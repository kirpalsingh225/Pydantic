from pydantic import BaseModel, Field, AnyUrl, EmailStr, computed_field
from typing import List, Optional, Annotated, Dict


class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    weight: float
    height: float
    married: bool
    allergies: List[str]
    contact: Dict[str, str]

    @computed_field
    @property
    def calc_bmi(self) -> float:
        bmi = self.weight / (self.height ** 2)
        return bmi

    
    
    
def update_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print("bmi value", patient.calc_bmi)
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
    "height": 1.75,  # Assuming height is in meters
    "married": True,
    "allergies": ["penicillin", "nuts"],
    "contact": {
        "phone": "1234567890",
        "address": "123 Main St, City, Country"
    }}

patient1 = Patient(**patient_info) # type coersion happens here
update_patient(patient1)