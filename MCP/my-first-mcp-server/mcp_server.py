from mcp.server.fastmcp import FastMCP
from services import get_leave_balance

mcp = FastMCP()

@mcp.tool()
def leave_balance(employee_id: str) -> str:
    """Get Employe Leave Balance"""
    balance = get_leave_balance(employee_id)
    
    return f"{employee_id} has {balance} day left."

if __name__ == "__main__":
    mcp.run()
    