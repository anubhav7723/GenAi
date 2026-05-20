from fastapi import FastAPI
from services import get_leave_balance

app = FastAPI()

@app.get("/leave/{employee_id}")
def leave_balance(employee_id:str):
    balance = get_leave_balance(employee_id)
    
    return {
        "employee_id" : employee_id,
        "balance" : balance
    }