from pydantic import BaseModel, Field


class Address(BaseModel):
    city: str
    state: str
    zip_code: str

class Patient(BaseModel):
    name: str
    address: Address


address_dict = {
    "city": "New York",
    "state": "NY",
    "zip_code": "10001"
}

address1 = Address(**address_dict)  # type coercion happens here
patient_info = {
    "name": "John Doe",
    "address": address1
}

patient1 = Patient(**patient_info)  # type coercion happens here

print(patient1)