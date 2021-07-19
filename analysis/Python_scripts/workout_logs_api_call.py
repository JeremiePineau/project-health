import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('S:\9_Projects\Project_Health\google_drive_svc.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Gym workouts (Responses)").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()

########## PUSH DATA TO BIGQUERY ##########
credentials = service_account.Credentials.from_service_account_file('S:\9_Projects\Project_Health\svc_acc.json')

# Construct a BigQuery client object.
project_id = 'local-axis-317516'
client = bigquery.Client(credentials= credentials,project=project_id)

# convert the json to dataframe
records_df = pd.DataFrame.from_dict(list_of_hashes)

pd.DataFrame.to_gbq(records_df, "dbt_project_health.workout_logs", project_id, if_exists="replace")