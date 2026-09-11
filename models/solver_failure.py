from pydantic import BaseModel, Field

class SolverFailure(BaseModel):
    message: str