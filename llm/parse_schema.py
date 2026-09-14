from pydantic import BaseModel, Field, model_validator

class MacroField(BaseModel):
    stated_min: float | None = Field(gt = 0, default=None, description="Minimum macronutrient amount. Only populate if the user explicity states a minimum.")
    stated_max: float | None = Field(gt = 0, default=None, description="Maximum macronutrient amount. Only populate if the user explicity states a maximum")
    approx_value: float | None = Field(gt = 0, default=None, description="Approximate macronutrient amount. Only populate if the user explicity approximates a value.")

    @model_validator(mode = 'after')
    def validator(self):
        if (self.stated_min is not None or self.stated_max is not None) and self.approx_value is not None:
            raise ValueError('cannot have both stated and approximate values')
        return self

class ParseSchema(BaseModel):
    calories_boundary: MacroField | None = Field(default=None, description="Calorie constraints only. Only populate if the user explicitly mentions calories.")
    protein_boundary: MacroField | None = Field(default=None, description="Protein constraints only. Only populate if the user explicitly mentions protein.")
    carbs_boundary: MacroField | None = Field(default=None, description="Carbs constraints only. Only populate if the user explicitly mentions carbs or carbohydrates.")
    fat_boundary: MacroField | None = Field(default=None, description="Fat constraints only. Only populate if the user explicitly mentions fat.")
    max_price: float | None = Field(gt=0, default=None,)
    calorie_percent_max: float | None = Field(gt=0, lt=1, default=None)
    excluded_ingredients: list[str] = Field(default_factory=list)