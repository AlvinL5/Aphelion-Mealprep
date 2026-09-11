from pydantic import BaseModel, Field

class NutrientRecord(BaseModel):
    name: str
    fdc_id: int
    calories_per_100g: float = Field(gt=0)
    protein_g_per_100g: float = Field(ge=0)
    fat_g_per_100g: float = Field(ge=0)
    carbs_g_per_100g: float = Field(ge=0)
    price_per_100g: float = Field(gt=0)