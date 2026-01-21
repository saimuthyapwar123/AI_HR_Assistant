# app/db/models.py
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime, date


class Employee(BaseModel):
    employee_id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None

    company_name: str = "Acme Technologies Pvt Ltd"

    department: str
    role: str
    level: str  # Junior, Mid, Senior, Lead

    skills: List[str]

    date_of_joining: date

    is_fresher: bool = False

    # Experience BEFORE joining Acme
    previous_experience_years: float = 0

    # Experience in Acme (calculated)
    company_experience_years: Optional[float] = None

    # Total experience (auto calculated)
    total_experience_years: Optional[float] = None

    total_projects: int

    is_active: bool = True

    created_at: datetime = Field(default_factory=datetime.utcnow)

# class Resume(BaseModel):
#     resume_id: str
#     candidate_name: str
#     email: str
#     skills: List[str]
#     experience_years: float
#     projects: List[str]
#     education: Optional[str] = None
#     parsed_text: str
#     created_at: datetime = Field(default_factory=datetime.utcnow)

# class HRPolicy(BaseModel):
#     policy_id: str
#     title: str
#     category: str  # Leave, Payroll, Benefits
#     content: str
#     source: Optional[str] = None  # PDF name
#     created_at: datetime = Field(default_factory=datetime.utcnow)

# class ConversationMemory(BaseModel):
#     session_id: str
#     user_id: Optional[str] = None
#     messages: List[dict]  # {"role": "user"/"assistant", "content": "..."}
#     updated_at: datetime = Field(default_factory=datetime.utcnow)

# class GraphCheckpoint(BaseModel):
#     thread_id: str
#     graph_state: dict
#     step_name: str
#     created_at: datetime = Field(default_factory=datetime.utcnow)
