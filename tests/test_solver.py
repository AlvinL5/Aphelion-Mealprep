import pandas as pd
from solver import solver_calc
from tests.test_data import ingredients_df, prices_df
from models.meal_plan_request import MealPlanRequest
from models.solver_success import SolverSuccess
from models.solver_failure import SolverFailure

def test_feasible_calories():
    request = MealPlanRequest(min_calories = 1, max_calories = 100)
    result = solver_calc(request, ingredients_df, prices_df)
    assert isinstance(result, SolverSuccess)
    assert (result.calories_total <= 100 and result.calories_total >= 1)

def test_infeasible_budget():
    request = MealPlanRequest(min_calories = 1000, max_calories = 1001, max_price = 9)
    result = solver_calc(request, ingredients_df, prices_df)
    assert isinstance(result, SolverFailure)


def test_infeasible_protein():
    request = MealPlanRequest(min_calories = 1, max_calories = 100, max_price = 10, min_protein = 10, excluded_ingredients = ['pure_protein'])
    result = solver_calc(request, ingredients_df, prices_df)
    assert isinstance(result, SolverFailure)