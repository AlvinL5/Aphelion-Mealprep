from dotenv import load_dotenv
import requests
from models.nutrient import NutrientRecord
import os
from data.fdc_mapping import INGREDIENT_FDC_IDS
import csv

#global variables for IDs associated with macronutrients
CALORIES_ID = 1008
PROTEIN_ID = 1003
CARBS_ID = 1005
FAT_ID = 1004

api_key = None

#set of IDs to lookup
NUTRIENT_IDS = {CALORIES_ID,PROTEIN_ID,FAT_ID,CARBS_ID}

#grabs API keys from .env file once
def get_api_key():
    global api_key
    if not api_key:
        load_dotenv()
        api_key = os.environ["FDC_API_KEY"]
    return api_key

def fetch_nutrient_data(name, fdc_id):
    nutrient_values = {}
    api_key = get_api_key()

    #grabs data from FDC database for given id using API key, errors if invalid key
    response = requests.get(f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}", params={"api_key": api_key})
    if response.status_code != 200: raise ValueError("INVALID ID")
    data = response.json()["foodNutrients"]

    #checks if each entry is the correct nutrient, adds nutrient data to nutrient_values dict
    for entry in data:
        if entry["nutrient"]["id"] in NUTRIENT_IDS:
            nutrient_values[entry["nutrient"]["id"]] = entry["amount"]

    #uses nutrient_values dict to build NutrientRecord
    return NutrientRecord(name = name, fdc_id = fdc_id, calories_per_100g = nutrient_values[CALORIES_ID], protein_g_per_100g = nutrient_values[PROTEIN_ID], carbs_g_per_100g = nutrient_values[CARBS_ID],fat_g_per_100g = nutrient_values[FAT_ID])

if __name__ == "__main__":
    nutrient_records = {}
    for name, fdc_id in INGREDIENT_FDC_IDS.items():
        nutrient_records[name] = fetch_nutrient_data(name, fdc_id)

    with open("data/ingredients.csv", "w", newline = "") as f:
        writer = csv.DictWriter(f, fieldnames= ["name", "fdc_id", "calories_per_100g", "protein_g_per_100g", "carbs_g_per_100g", "fat_g_per_100g"])
        writer.writeheader()
        for nutrient_record in nutrient_records.values():
            writer.writerow(nutrient_record.model_dump())