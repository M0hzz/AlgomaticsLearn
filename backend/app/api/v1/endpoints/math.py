from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from backend.app.core.security import get_current_user
from backend.app.models.user import User

from backend.app.topics.math.algebra.quadratic import (
    solve_quadratic, get_quadratic_points, get_quadratic_properties
)

router = APIRouter()

class QuadraticEquation(BaseModel):
    a: float
    b: float
    c: float
    x_min: Optional[float] = -10
    x_max: Optional[float] = 10
    num_points: Optional[int] = 100

@router.post("/algebra/quadratic/solve")
async def solve_quadratic_equation(equation: QuadraticEquation):
    """Solve a quadratic equation"""
    try:
        return solve_quadratic(equation.a, equation.b, equation.c)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/algebra/quadratic/plot")
async def get_quadratic_plot_points(equation: QuadraticEquation):
    """Get points for plotting a quadratic function"""
    try:
        return {
            "points": get_quadratic_points(
                equation.a, equation.b, equation.c,
                equation.x_min, equation.x_max, equation.num_points
            )
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/algebra/quadratic/properties")
async def get_quadratic_function_properties(equation: QuadraticEquation):
    """Get properties of a quadratic function"""
    try:
        return get_quadratic_properties(equation.a, equation.b, equation.c)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class LinearSystem(BaseModel):
    coefficients: List[List[float]]
    constants: List[float]

@router.post("/algebra/linear-system")
async def solve_linear_system(system: LinearSystem, current_user: User = Depends(get_current_user)):
    """Solve a system of linear equations"""
    try:
        import numpy as np

        # Convert to numpy arrays
        A = np.array(system.coefficients)
        b = np.array(system.constants)

        # Check if system is solvable
        rank_A = np.linalg.matrix_rank(A)
        rank_Ab = np.linalg.matrix_rank(np.column_stack((A, b)))

        if rank_A != rank_Ab:
            return {
                "type": "inconsistent",
                "message": "The system has no solutions",
                "solution": None
            }

        if rank_A < min(A.shape):
            # Underdetermined system
            return {
                "type": "underdetermined",
                "message": "The system has infinitely many solutions",
                "solution": "Infinitely many solutions",
                "particular_solution": np.linalg.lstsq(A, b, rcond=None)[0].tolist()
            }

        # Try to solve
        solution = np.linalg.solve(A, b)

        return {
            "type": "unique",
            "message": "The system has a unique solution",
            "solution": solution.tolist()
        }
    except np.linalg.LinAlgError as e:
        return {
            "type": "error",
            "message": f"Error solving system: {str(e)}",
            "solution": None
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class SimpleExpression(BaseModel):
    expression: str
    variable: Optional[str] = "x"
    value: Optional[float] = None

@router.post("/evaluate")
async def evaluate_expression(data: SimpleExpression):
    """Evaluate a mathematical expression"""
    try:
        # A simple and safe way to evaluate basic expressions
        # For more complex expressions, consider using sympy
        import math

        # Define safe functions and constants
        safe_dict = {
            'abs': abs,
            'max': max,
            'min': min,
            'sum': sum,
            'len': len,
            'round': round,
            'pow': pow,
            'math': math
        }

        # Add all math module functions and constants
        for key in dir(math):
            safe_dict[key] = getattr(math, key)

        # Replace variable with value if provided
        expression = data.expression
        if data.value is not None:
            expression = expression.replace(data.variable, str(data.value))

        # Calculate result
        result = eval(expression, {"__builtins__": {}}, safe_dict)

        return {
            "expression": data.expression,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error evaluating expression: {str(e)}")