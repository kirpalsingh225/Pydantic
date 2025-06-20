from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="The unique identifier for the patient", example="1")]
    name: Annotated[str, Field(..., description="The name of the patient", example="John Doe")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="The age of the patient", example=30)]
    gender: Annotated[Literal["male", "female"], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="The height of patient")]
    weight: Annotated[float, Field(..., gt=0, description="The weight of patient")]

    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate Body Mass Index (BMI)"""
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    gender: Annotated[Optional[Literal["male", "female"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None)]
    weight: Annotated[Optional[float], Field(default=None)]

def load_data():
    with open("patients.json", "r") as file:
        data = json.load(file)
    return data

def save_data(data):
    with open("patients.json", "w") as file:
        json.dump(data, file)

@app.get("/")
def hello():
    return {"message": "patient management system"}

@app.get("/about")
def about():
    return {"message": "a fully functional patient management system built with FastAPI"}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to view", example="1")):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by:str = Query(..., description="sort on the basis of height, weight, bmi "), order:str = Query("asc", description="sort in ascending or descending order")):
    
    valid_field = ["height", "weight", "bmi"]

    if sort_by not in valid_field:
        raise HTTPException(status_code=400, detail="Invalid sort field. Choose from height, weight, bmi.")
    
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Choose 'asc' or 'desc'.")
    
    data = load_data()

    sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse=(order == "desc"))

    return sorted_data
    
    
@app.post("/create")
def create_patient(patient: Patient):

    #load existing data
    data = load_data()

    #check if patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists.")
    
    # add new patient
    data[patient.id] = patient.model_dump(exclude=["id"])

    save_data(data)

    return JSONResponse(status_code=201, content={"message": "patient created successfully"})

@app.put("/edit/{patient_id}")
def update(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info["id"] = patient_id
    patient_pydantic_object = Patient(**existing_patient_info)  # Validate the updated data
    patient_pydantic_object.model_dump(exclude=["id"])  # Ensure the id is not included in the final data

    data[patient_id] = existing_patient_info  

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "patient updated successfully"})  

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "patient deleted successfully"})
