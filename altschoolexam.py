from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Patient(BaseModel):
    id: int
    name: str
    age: int
    sex: str
    weight: float
    height: float
    phone: str

class Doctor(BaseModel):
    id: int
    name: str
    specialization: str
    phone: str
    is_available: bool = True

class Appointment(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    date: str

patients = []
doctors = []
appointments = []

@app.post("/patients", response_model=Patient)
def create_patient(patient: Patient):
    patients.append(patient)
    return patient

@app.get("/patients")
def get_patients():
    return patients

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    for patient in patients:
        if patient.id == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

@app.put("/patients/{patient_id}", response_model=Patient)
def update_patient(patient_id: int, patient: Patient):
    for idx, p in enumerate(patients):
        if p.id == patient_id:
            patients[idx] = patient
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    for idx, patient in enumerate(patients):
        if patient.id == patient_id:
            del patients[idx]
            return {"message": "Patient deleted successfully"}
    raise HTTPException(status_code=404, detail="Patient not found")

@app.post("/doctors", response_model=Doctor)
def create_doctor(doctor: Doctor):
    doctors.append(doctor)
    return doctor

@app.get("/doctors")
def get_doctors():
    return doctors

@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    for doctor in doctors:
        if doctor.id == doctor_id:
            return doctor
    raise HTTPException(status_code=404, detail="Doctor not found")

@app.put("/doctors/{doctor_id}", response_model=Doctor)
def update_doctor(doctor_id: int, doctor: Doctor):
    for idx, d in enumerate(doctors):
        if d.id == doctor_id:
            doctors[idx] = doctor
            return doctor
    raise HTTPException(status_code=404, detail="Doctor not found")

@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    for idx, doctor in enumerate(doctors):
        if doctor.id == doctor_id:
            del doctors[idx]
            return {"message": "Doctor deleted successfully"}
    raise HTTPException(status_code=404, detail="Doctor not found")

@app.post("/appointments", response_model=Appointment)
def create_appointment(appointment: Appointment):
    available_doctors = [doctor for doctor in doctors if doctor.is_available]
    if not available_doctors:
        raise HTTPException(status_code=400, detail="No available doctors")
    appointment.doctor_id = available_doctors[0].id
    appointments.append(appointment)
    return appointment

@app.put("/appointments/{appointment_id}/complete")
def complete_appointment(appointment_id: int):
    for appointment in appointments:
        if appointment.id == appointment_id:
            for doctor in doctors:
                if doctor.id == appointment.doctor_id:
                    doctor.is_available = True
            return {"message": "Appointment completed successfully"}
    raise HTTPException(status_code=404, detail="Appointment not found")

@app.delete("/appointments/{appointment_id}")
def cancel_appointment(appointment_id: int):
    for idx, appointment in enumerate(appointments):
        if appointment.id == appointment_id:
            del appointments[idx]
            for doctor in doctors:
                if doctor.id == appointment.doctor_id:
                    doctor.is_available = True
            return {"message": "Appointment canceled successfully"}
    raise HTTPException(status_code=404, detail="Appointment not found")

@app.put("/doctors/{doctor_id}/set_availability")
def set_availability(doctor_id: int, is_available: bool):
    for doctor in doctors:
        if doctor.id == doctor_id:
            doctor.is_available = is_available
            return {"message": "Availability status updated successfully"}
    raise HTTPException(status_code=404, detail="Doctor not found")
