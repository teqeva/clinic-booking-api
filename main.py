from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine, Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clinic Booking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/patients", response_model=schemas.PatientOut)
def create_patient_endpoint(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    p = crud.create_patient(db, patient)
    return p

@app.get("/patients", response_model=list[schemas.PatientOut])
def list_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_patients(db, skip=skip, limit=limit)

@app.get("/patients/{patient_id}", response_model=schemas.PatientOut)
def get_patient_endpoint(patient_id: int, db: Session = Depends(get_db)):
    p = crud.get_patient(db, patient_id)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return p

@app.put("/patients/{patient_id}", response_model=schemas.PatientOut)
def update_patient_endpoint(patient_id: int, patient: schemas.PatientUpdate, db: Session = Depends(get_db)):
    p = crud.update_patient(db, patient_id, patient)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return p

@app.delete("/patients/{patient_id}")
def delete_patient_endpoint(patient_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_patient(db, patient_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"status": "deleted"}

@app.post("/appointments", response_model=schemas.AppointmentOut)
def create_appointment_endpoint(appt: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    res = crud.create_appointment(db, appt)
    if isinstance(res, dict) and res.get("error"):
        raise HTTPException(status_code=400, detail=res["error"])
    return res

@app.get("/appointments", response_model=list[schemas.AppointmentOut])
def list_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_appointments(db, skip=skip, limit=limit)

@app.get("/appointments/{appointment_id}", response_model=schemas.AppointmentOut)
def get_appointment_endpoint(appointment_id: int, db: Session = Depends(get_db)):
    a = crud.get_appointment(db, appointment_id)
    if not a:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return a

@app.put("/appointments/{appointment_id}", response_model=schemas.AppointmentOut)
def update_appointment_endpoint(appointment_id: int, appt: schemas.AppointmentUpdate, db: Session = Depends(get_db)):
    res = crud.update_appointment(db, appointment_id, appt)
    if res is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if isinstance(res, dict) and res.get("error"):
        raise HTTPException(status_code=400, detail=res["error"])
    return res

@app.delete("/appointments/{appointment_id}")
def delete_appointment_endpoint(appointment_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_appointment(db, appointment_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"status": "deleted"}
