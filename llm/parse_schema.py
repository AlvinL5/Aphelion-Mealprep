from pydantic import BaseModel, Field, model_validator

class MacroField(BaseModel):
    stated_min: float | None = Field(gt = 0, default=None)
    stated_max: float | None = Field(gt = 0, default=None)
    approx_value: float | None = Field(gt = 0, default=None)

    @model_validator(mode = 'after')
    def validator(self):
        if (self.stated_min is not None or self.stated_max is not None) and self.approx_value is not None:
            raise ValueError('cannot have both stated and approximate values')
        return self

class ParseSchema(BaseModel):
    calorie_boundary: MacroField | None = Field(default=None)
    protein_boundary: MacroField | None = Field(default=None)
    carbs_boundary: MacroField | None = Field(default=None)
    fat_boundary: MacroField | None = Field(default=None)
    max_price: float | None = Field(gt=0, default=None)
    calorie_percent_max: float | None = Field(gt=0, lt=1, default=None)
    excluded_ingredients: list[str] = Field(default_factory=list)