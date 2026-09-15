import pandas as pd

ingredients_df = pd.DataFrame({
    'name': ['pure_calories', 'pure_protein', 'pure_carbs', 'pure_fat'],
     "display_name": ["Pure Calories", "Pure Protein", "Pure Carbs", "Pure Fat"],
    'calories_per_100g': [100, 0, 0, 0],
    'protein_g_per_100g': [0, 100, 0, 0],
    'carbs_g_per_100g': [0, 0, 100, 0],
    'fat_g_per_100g': [0, 0, 0, 100]
})

prices_df = pd.DataFrame({
    'name': ['pure_calories', 'pure_protein', 'pure_carbs', 'pure_fat'],
    'price_per_100g': [1, 1, 1, 1]
})