from unittest.mock import patch
from starlette.testclient import TestClient
from main import app
from models.parsing_error import ParsingError
from models.meal_plan_request import MealPlanRequest
from models.solver_failure import SolverFailure
from models.solver_success import SolverSuccess


@patch('main.parse')
def test_parse_error(mock_name):
    mock_name.return_value = ParsingError(message = '422')
    with TestClient(app) as client:
        response = client.post("/plan", json={"user_input": "anything"})
    assert response.status_code == 422
    assert response.json()['detail'] == '422'


@patch('main.parse')
@patch('main.solver_calc')
def test_solver_error(mock_solver, mock_parse):
    mock_parse.return_value = MealPlanRequest(min_calories = 100, max_calories = 200)
    mock_solver.return_value = SolverFailure(message = '422')
    with TestClient(app) as client:
        response = client.post("/plan", json={"user_input": "anything"})
    assert response.status_code == 422
    assert response.json()['detail'] == '422'


@patch('main.parse')
@patch('main.solver_calc')
def test_success(mock_solver, mock_parse):
    mock_parse.return_value = MealPlanRequest(min_calories = 100, max_calories = 200)
    mock_solver.return_value = SolverSuccess(ingredients_grams = {'chicken_thigh_skin_on' : 1}, calories_total = 150, protein_total = 0, carbs_total = 0, fat_total = 0, price_total = 1)
    with TestClient(app) as client:
        response = client.post("/plan", json={"user_input": "anything"})
    assert response.status_code == 200
    assert isinstance(response.json()['plan'], str)
