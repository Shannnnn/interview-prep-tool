from fastapi import FastAPI
import numpy as np

app = FastAPI()

@app.get("/generate/math")
def generate_math():
    # Use Numpy to create a random matrix
    # This demonstrates proficiency in Python numerical libraries
    matrix = np.random.randint(1, 10, size=(2, 2))
    det = int(np.linalg.det(matrix))
    
    return {
        "title": "Linear Algebra Challenge",
        "category": "MA",
        "body": f"Calculate the determinant of this 2x2 matrix: {matrix.tolist()}",
        "answer": str(det)
    }