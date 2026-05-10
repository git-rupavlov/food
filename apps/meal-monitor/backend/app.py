from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx

app = FastAPI(title='Meal Monitor API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

FDC_API_KEY = os.getenv('FDC_API_KEY', '')

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.get('/foods/search')
async def search_foods(q: str):
    url = 'https://api.nal.usda.gov/fdc/v1/foods/search'

    payload = {
        'query': q,
        'pageSize': 10,
        'dataType': [
            'Foundation',
            'SR Legacy',
            'Survey (FNDDS)',
            'Branded'
        ]
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            url,
            params={'api_key': FDC_API_KEY},
            json=payload
        )

    response.raise_for_status()
    data = response.json()

    foods = []

    for item in data.get('foods', []):
        foods.append({
            'fdc_id': item.get('fdcId'),
            'description': item.get('description'),
            'data_type': item.get('dataType')
        })

    return foods
