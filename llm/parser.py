from llm.parse_schema import ParseSchema
from models.meal_plan_request import MealPlanRequest
from pydantic import ValidationError
from models.parsing_error import ParsingError



def build_request_from_parse(parse: ParseSchema):
    boundaries = [(parse.calories_boundary, 'min_calories', 'max_calories'),
                (parse.protein_boundary, 'min_protein', 'max_protein'),
                (parse.carbs_boundary, 'min_carbs', 'max_carbs'),
                (parse.fat_boundary, 'min_fat', 'max_fat')]
    boundary_dict = {}
    for boundary, nutrient_min, nutrient_max in boundaries:
        nutr_min = None
        nutr_max = None
        if boundary is not None:
            if boundary.approx_value is not None:
                nutr_min = boundary.approx_value * 0.9
                nutr_max = boundary.approx_value * 1.1
            else:
                nutr_min = boundary.stated_min
                nutr_max = boundary.stated_max
        boundary_dict[nutrient_min] = nutr_min
        boundary_dict[nutrient_max] = nutr_max
    try:
        return MealPlanRequest(**boundary_dict,
                        max_price = parse.max_price,
                        calorie_percent_max = parse.calorie_percent_max,
                        excluded_ingredients = parse.excluded_ingredients)
    except ValidationError as e:
        return ParsingError(message=str(e))