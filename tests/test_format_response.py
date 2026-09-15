from models.solver_success import SolverSuccess
from llm.format_response import format_response
import unittest

def test_format_response():
    mealplan = SolverSuccess(ingredients_grams = {'chicken_breast': 100.0001, 'white_rice': 200.6},
                                                calories_total = 1000,
                                                protein_total = 50,
                                                carbs_total = 100,
                                                fat_total = 0,
                                                price_total = 2.111)
    display_names = {'chicken_breast': 'Chicken Breast', 'brown_rice': 'Brown Rice', 'white_rice': 'White Rice'}
    output = format_response(mealplan, display_names)
    assert('100g of Chicken Breast' in output)
    assert('201g of White Rice' in output)
    assert('Total Price: $2.11' in output)
    assert('Protein Total: 50g' in output)
