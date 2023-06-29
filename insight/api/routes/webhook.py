# webhook.py
# Relative Path: insight/api/routes/webhook.py
from fastapi import APIRouter, Request
import requests
import pandas as pd
import io

router = APIRouter()

# Global variable to store the rules
rules_dict = {}


# Function to load data from URL via pandas.
def load_rules():
    url = "https://docs.gova11y.io/files/a11y_rules"
    s = requests.get(url).content
    rules_data = pd.read_csv(io.StringIO(s.decode('utf-8')))

    # Convert the DataFrame to a list of dictionaries
    rules_list = rules_data.to_dict('records')

    # Convert the list to a dictionary with 'axe_id' as key
    return {row['axe_id']: row for row in rules_list}


# Load rules at startup
@router.on_event("startup")
async def startup_event():
    global rules_dict
    rules_dict = load_rules()


# Endpoint to receive webhook POSTs
# https://reports.gova11y.io/webhook/update/a11y_rules
@router.post("/update/a11y_rules")
async def update_rules(request: Request):
    # To or not to validate if it is a payload from the Githubs...
    data = await request.json()

    # Mock condition, replace with your own verification.
    if 'updated_file' in data:
        # If file updated, reload rules.
        global rules_dict
        rules_dict = load_rules()
    return {"status": "rules updated"}