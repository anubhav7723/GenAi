from sqlalchemy import Column, Integer, String
from database import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    employee_id = Column(String, unique=True)
    leave_balance = Column(Integer)
    
class LeaveHistory(Base):
    __tablename__ = "leave_history"
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(String)
    leave_date = Column(String)