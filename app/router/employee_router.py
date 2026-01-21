from fastapi import APIRouter, HTTPException
from app.db.mongo import get_collection
from app.db.models import Employee
from datetime import date, datetime

router = APIRouter(prefix="/api", tags=["Employees"])
employees = get_collection("employees")


@router.post("/employees")
def add_employee(emp: Employee):

    # Duplicate check
    if employees.find_one({"employee_id": emp.employee_id}):
        raise HTTPException(400, "Employee already exists")

    today = date.today()

    # Calculate company experience
    emp.company_experience_years = round(
        (today - emp.date_of_joining).days / 365, 2
    )

    # Fresher logic
    if emp.is_fresher:
        emp.previous_experience_years = 0

    # Total experience
    emp.total_experience_years = round(
        emp.previous_experience_years + emp.company_experience_years, 2
    )

    # Validation
    if emp.company_experience_years < 0:
        raise HTTPException(400, "Joining date cannot be in the future")

    data = emp.dict()

    # 🔥 MongoDB FIX
    data["date_of_joining"] = datetime.combine(emp.date_of_joining, datetime.min.time())

    employees.insert_one(data)

    return {
        "message": "Employee added successfully",
        "employee_id": emp.employee_id,
        "total_experience": emp.total_experience_years
    }
