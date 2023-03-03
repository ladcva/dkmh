# run every 5 minutes
# check for changes in Id dot dang ky

import requests
from bs4 import BeautifulSoup
import hashlib

# URL of the website to monitor
url = "https://www.example.com"

# Hash of the initial state of the website
initial_hash = None

# Function to calculate the hash of the website content
def calculate_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

# Monitor the website for changes
while True:
    # Make a POST request to the website
    response = requests.post(url, data={'param1': 'value1', 'param2': 'value2'})
    soup = BeautifulSoup(response.content, 'html.parser')

    # Calculate the hash of the website content
    current_hash = calculate_hash(str(soup))

    # If the hash of the content has changed, save a snapshot and notify Crawler 2
    if current_hash != initial_hash:
        # Save a snapshot of the website content
        with open('snapshot.html', 'w') as f:
            f.write(str(soup))

        # Notify Crawler 2 to update its data
        requests.post('http://crawler2.example.com/update', data={'new_data': str(soup)})

        # Update the hash of the content to the current hash
        initial_hash = current_hash
