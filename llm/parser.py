from llm.parse_schema import ParseSchema
from models.meal_plan_request import MealPlanRequest
from pydantic import ValidationError
from models.parsing_error import ParsingError
import anthropic

client = None

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

def get_api_key():
    global client
    if not client:
        client = anthropic.Anthropic()

def llm_call(user_input: str):
    get_api_key()
    response = client.messages.create(model = 'claude-haiku-4-5-20251001',
                        max_tokens = 1024,
                        messages = [{"role": "user", "content": user_input}],
                        tools = [{'name': 'extract_meal_plan_request', 'description': 'Extract meal plan constraints from a natural language request', 'input_schema': ParseSchema.model_json_schema()}],
                        tool_choice = {'type': 'any'})
    for block in response.content:
        if block.type == 'tool_use':
            try:
                return ParseSchema(**block.input)
            except ValidationError as e:
                return ParsingError(message=str(e))
    return ParsingError(message='llm failed to use tool')

def parse(user_input: str):
    response = llm_call(user_input)
    if isinstance(response, ParsingError):
        return response
    return build_request_from_parse(response)


