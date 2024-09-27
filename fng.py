import requests
import csv
import os
from datetime import datetime
from github import Github  # You'll need to install PyGithub: pip install PyGithub

# Step 1: Fetch data from Alternative.me API
url = 'https://api.alternative.me/fng/?limit=1'
response = requests.get(url)
data = response.json()

# Step 2: Extract the relevant data
fear_greed_value = data['data'][0]['value']
current_date = datetime.now().strftime('%Y-%m-%d')

# Step 3: Load existing CSV data (or create if it doesn't exist)
csv_file = 'fear_and_greed.csv'

if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['date', 'fear_greed_value'])  # Header row

# Append the new data
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([current_date, fear_greed_value])

# Step 4: Push the updated CSV file to GitHub
# You need a GitHub token with repo permissions to use PyGithub.
g = Github('your_github_access_token')

repo = g.get_user().get_repo('your_repository_name')
file_path = 'fear_and_greed.csv'
with open(csv_file, 'r') as file:
    content = file.read()

# Check if file exists in the repo
try:
    contents = repo.get_contents(file_path)
    repo.update_file(contents.path, f"Update Fear and Greed Index for {current_date}", content, contents.sha)
except:
    repo.create_file(file_path, "Create Fear and Greed Index CSV", content)
