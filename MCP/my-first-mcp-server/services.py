from database import SessionLocal
from model import Employee

def create_employee(employee_id: str, balance: int):

    db = SessionLocal()

    employee = Employee(
        employee_id=employee_id,
        leave_balance=balance
    )

    db.add(employee)
    db.commit()

    db.close()
    
def get_leave_balance(employee_id: str):

    db = SessionLocal()
    
    employee = db.query(Employee).filter(
        Employee.employee_id == employee_id
    ).first()
    
    db.close()
    
    if employee:
        return employee.leave_balance
    return None

def apply_leave(employee_id:str, days:int):
    db = SessionLocal()
    
    employee = db.query(Employee).filter(
        Employee.employee_id == employee_id
    ).first()
    
    if employee:
        employee.leave_balance -= days
        db.commit()
        
    db.close()
        
        