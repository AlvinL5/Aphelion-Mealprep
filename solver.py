import pandas as pd
from ortools.linear_solver import pywraplp
from models.meal_plan_request import MealPlanRequest
from models.solver_success import SolverSuccess
from models.solver_failure import SolverFailure
import logging



def solver_calc(request: MealPlanRequest, ingredients_df: pd.DataFrame = None, prices_df: pd.DataFrame = None):
    if ingredients_df is None:
        ingredients_df = pd.read_csv('data/ingredients.csv')
    if prices_df is None:
        prices_df = pd.read_csv('data/prices.csv')
    merged_df = pd.merge(ingredients_df, prices_df, on = 'name', how = 'inner')
    dropped = set(ingredients_df['name']) - set(merged_df['name'])
    if dropped:
        logging.warning(f'Ingredients dropped due to missing prices: {sorted(dropped)}')

    included_df = merged_df[~merged_df['name'].isin(request.excluded_ingredients)]

    solver = pywraplp.Solver.CreateSolver('GLOP')
    calories_eq = 0
    protein_eq = 0
    carbs_eq = 0
    fat_eq = 0
    price_eq = 0
    var_dict = {}
    nutrient_dict = {}

    for index, row in included_df.iterrows():
        ingredient = row['name']
        calories = row['calories_per_100g']
        protein = row['protein_g_per_100g']
        carbs = row['carbs_g_per_100g']
        fat = row['fat_g_per_100g']
        price_total = row['price_per_100g']

        x = solver.NumVar(0, solver.infinity(), f'{ingredient}')
        var_dict[ingredient] = x

        nutrient_dict[x] = {'calories': calories,
                            'protein': protein,
                            'carbs': carbs,
                            'fat':  fat,
                            'price': price_total}

        calories_eq += calories * x
        protein_eq += protein * x
        carbs_eq += carbs * x
        fat_eq += fat * x
        price_eq += price_total * x
    if request.calorie_percent_max is not None:
        for var, nutrients in nutrient_dict.items():
            solver.Add(var * nutrients['calories'] <= request.calorie_percent_max * calories_eq)

    boundaries = [
        (calories_eq, request.min_calories,request.max_calories),
        (protein_eq, request.min_protein, request.max_protein),
        (carbs_eq, request.min_carbs, request.max_carbs),
        (fat_eq, request.min_fat, request.max_fat)
    ]
    for nutr_sum, min_nutr, max_nutr in boundaries:
        solver.Add(nutr_sum >= min_nutr)
        if max_nutr is not None:
            solver.Add(nutr_sum <= max_nutr)

    if request.max_price is not None:
        solver.Add(price_eq <= request.max_price)
    
    solver.Minimize(price_eq)
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        plan = {}
        calories_total = 0
        protein_total = 0
        carbs_total = 0 
        fat_total = 0
        price_total = 0
        for ingredient, var in var_dict.items():
            if var.solution_value() != 0:
                value = var.solution_value()
                plan[ingredient] = value * 100
                calories_total += value * nutrient_dict[var]['calories']
                protein_total += value * nutrient_dict[var]['protein']
                carbs_total += value * nutrient_dict[var]['carbs']
                fat_total += value * nutrient_dict[var]['fat']
                price_total += value * nutrient_dict[var]['price']

        return SolverSuccess(ingredients_grams = plan, calories_total = calories_total, protein_total = protein_total, carbs_total = carbs_total, fat_total = fat_total, price_total = price_total)
    else:
        return SolverFailure(message = "Not possible with given constraints.")

if __name__ == "__main__":
    test_request = MealPlanRequest(
        min_calories=2500, max_calories=3000,
        min_protein=120,
        min_carbs=200,
        max_price=30,
        max_fat = 30,
        excluded_ingredients=['whey_protein_generic', 'lentils', 'chickpeas', 'bacon', 'black_beans'],
    )
    print(solver_calc(test_request))


