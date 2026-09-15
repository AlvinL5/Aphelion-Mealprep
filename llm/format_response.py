from models.solver_success import SolverSuccess
import pandas as pd


def build_display_lookup(df: pd.DataFrame = None) -> dict[str, str]:
    if df is None:
        df = pd.read_csv('data/ingredients.csv')
    return dict(zip(df["name"], df["display_name"]))

def format_response(mealplan: SolverSuccess, display_names: dict[str, str]) -> str:
    output = ''
    output += 'Your optimal mealplan is:\n'
    for ingredient, grams in mealplan.ingredients_grams.items():
        output += f'{grams:.0f}g of {display_names[ingredient]}\n'
    output += f'Calorie Total: {mealplan.calories_total:.0f}\n'
    output += f'Protein Total: {mealplan.protein_total:.0f}g\n'
    output += f'Carbs Total: {mealplan.carbs_total:.0f}g\n'
    output += f'Fat Total: {mealplan.fat_total:.0f}g\n'
    output += f'Total Price: ${mealplan.price_total:.2f}\n'
    return output