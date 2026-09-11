from pydantic import BaseModel, Field

class SolverSuccess(BaseModel):
    ingredients_grams: dict[str, float]
    calories_total: float
    protein_total: float
    carbs_total: float
    fat_total: float
    price_total: float
