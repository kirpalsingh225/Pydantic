from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=50, description="Name of the patient", example="John Doe")]
    email: EmailStr
    age: int  
    weight: Annotated[float, Field(default=True, description="Weight of the person", strict=True, gt=0)]
    married: Annotated[bool, Field(default=False, description="Is the patient married?")]
    allergies: Optional[List[str]]  = None # if set optional have to pass None by default
    contact: Dict[str, str]

patient_info = {
    "name": "John Doe",
    "age": 30,
    "weight": True,
    "married": False,
    "allergies": ["pollen", "nuts"],
    "contact": {"email": "@.com", "phone": "123-456-7890"}}
patient1 = Patient(**patient_info)

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("insrted into database")

insert_patient_data(patient1)
