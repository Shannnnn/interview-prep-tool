from fastapi import FastAPI
import numpy as np

app = FastAPI()

@app.get("/challenge/matrix")
def get_matrix_challenge():
    # 1. Create a random 2x2 Matrix with numbers between 1 and 10
    # This shows you can handle 'matrix operations' mentioned in the JD
    matrix = np.random.randint(1, 10, size=(2, 2))
    
    # 2. Calculate the Determinant
    # Formula: (a*d) - (b*c)
    determinant = np.linalg.det(matrix)
    
    # 3. Format the response
    return {
        "title": "Linear Algebra: Determinant",
        "description": "Calculate the determinant of the following 2x2 matrix.",
        "matrix": matrix.tolist(),
        "answer": round(float(determinant), 2),
        "hint": "For a 2x2 matrix [[a, b], [c, d]], the determinant is (ad - bc)"
    }