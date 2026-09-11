import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FDC_API_KEY")
BASE_URL = "https://api.nal.usda.gov/fdc/v1/food"


def get_descriptions(fdc_ids):
    descriptions = {}
    for fdc_id in fdc_ids:
        response = requests.get(
            f"{BASE_URL}/{fdc_id}",
            params={"api_key": API_KEY}
        )
        response.raise_for_status()
        data = response.json()
        descriptions[fdc_id] = data["description"]
    return descriptions


if __name__ == "__main__":
    ids_to_check = [
    171474, 171077, 172385, 173627,
    172850, 171098,
    168312, 168286, 167843, 168277,
    174036, 169495, 168728,
    175167, 173709, 175176, 171955, 175179,
    171287,
    170894, 172182, 173180, 171265,
    172475, 174272, 172420, 173734, 173756,
    168877, 169703, 173904, 169736, 169738,
    174924, 172688, 170027, 168482, 168874, 173242,
]
    results = get_descriptions(ids_to_check)
    for fdc_id, desc in results.items():
        print(f"{fdc_id}: {desc}")