from fastmcp import FastMCP

mcp = FastMCP("Async Math Calculator")


@mcp.tool
async def add(a: float, b: float):
    """
    Add two numbers.
    """
    return {
        "operation": "addition",
        "expression": f"{a} + {b}",
        "result": a + b
    }


@mcp.tool
async def subtract(a: float, b: float):
    """
    Subtract the second number from the first.
    """
    return {
        "operation": "subtraction",
        "expression": f"{a} - {b}",
        "result": a - b
    }


@mcp.tool
async def multiply(a: float, b: float):
    """
    Multiply two numbers.
    """
    return {
        "operation": "multiplication",
        "expression": f"{a} × {b}",
        "result": a * b
    }


@mcp.tool
async def divide(a: float, b: float):
    """
    Divide the first number by the second.
    """
    if b == 0:
        return {
            "error": "Division by zero is not allowed."
        }

    return {
        "operation": "division",
        "expression": f"{a} ÷ {b}",
        "result": a / b
    }


if __name__ == "__main__":
    mcp.run()