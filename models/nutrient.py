from pydantic import BaseModel, Field

class NutrientRecord(BaseModel):
    name: str
    display_name: str = Field(min_length=1)
    fdc_id: int
    calories_per_100g: float = Field(gt=0)
    protein_g_per_100g: float = Field(ge=0)
    fat_g_per_100g: float = Field(ge=0)
    carbs_g_per_100g: float = Field(ge=0)