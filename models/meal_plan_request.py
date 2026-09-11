from pydantic import BaseModel, Field, model_validator

class MealPlanRequest(BaseModel):
    min_calories: float = Field(gt=0)
    max_calories: float = Field(gt=0)
    min_protein: float = Field(ge=0, default = 0)
    max_protein: float | None = Field(ge=0, default=None)
    min_carbs: float = Field(ge=0, default = 0)
    max_carbs: float | None = Field(ge=0, default=None)
    min_fat: float = Field(ge=0, default = 0)
    max_fat: float | None = Field(ge=0, default=None)
    max_price: float | None = Field(gt=0, default=None)
    calorie_percent_max: float | None = Field(gt=0, lt=1, default=None)
    excluded_ingredients: list[str] = Field(default=[])

    def min_max_conflict(self, nutrient):
        if getattr(self, f'max_{nutrient}') is not None and getattr(self, f'max_{nutrient}') < getattr(self, f'min_{nutrient}'):
            raise ValueError(f"{nutrient} max cannot be less than {nutrient} min")

    @model_validator(mode = 'after')
    def validator(self):
        self.min_max_conflict('calories')
        self.min_max_conflict('protein')
        self.min_max_conflict('carbs')
        self.min_max_conflict('fat')
        return self
