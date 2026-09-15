from unittest.mock import patch
from llm.parser import parse
from llm.parse_schema import ParseSchema, MacroField
from models.meal_plan_request import MealPlanRequest
from models.parsing_error import ParsingError
import pytest

@patch("llm.parser.llm_call")
def test_min_max(mock_name):
    mock_name.return_value = ParseSchema(calories_boundary = MacroField(stated_min = 2000, stated_max = 2800),
                                        protein_boundary = MacroField(stated_min = 150))
    result = parse("Give me a meal plan with calories ranging from 2000 to 2800 and at least 150 grams of protein.")
    assert isinstance(result, MealPlanRequest)
    assert (result.min_calories == pytest.approx(2000) and result.max_calories == pytest.approx(2800) and result.min_protein == pytest.approx(150))

@patch("llm.parser.llm_call")
def test_approx(mock_name):
    mock_name.return_value = ParseSchema(calories_boundary = MacroField(approx_value = 2500),
                                        carbs_boundary = MacroField(approx_value = 100))
    result = parse("Give me a meal plan with about 2500 calories and 100 grams of carbs.")
    assert isinstance(result, MealPlanRequest)
    assert (result.min_calories == pytest.approx(2250) and result.max_calories == pytest.approx(2750) and result.min_carbs == pytest.approx(90) and result.max_carbs == pytest.approx(110))

@patch("llm.parser.llm_call")
def test_failure(mock_name):
    mock_name.return_value = ParseSchema(calories_boundary = MacroField(stated_min = 2000, stated_max = 1800))
    result = parse("Give me a mealplan with at least 2000 calories and at most 1800 calories.")
    assert isinstance(result, ParsingError)