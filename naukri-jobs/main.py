import requests
import pandas as pd

# Define the URL and headers for the API request
url = "https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&location=delhi%20%2F%20ncr&keyword=data%20entry%20operator&pageNo=1&k=data%20entry%20operator&l=delhi%20%2F%20ncr&seoKey=data-entry-operator-jobs-in-delhi-ncr&src=jobsearchDesk&latLong="

headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
    'appid': '109',
    'clientid': 'd3skt0p',
    'content-type': 'application/json',
    'gid': 'LOCATION,INDUSTRY,EDUCATION,FAREA_ROLE',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'systemid': 'Naukri',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

# Send the GET request to the API
response = requests.get(url, headers=headers)

# Check if the response is successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Assuming the actual job listings are inside 'jobDetails' in the JSON response
    job_listings = data.get('jobDetails', [])

    # Convert the job listings into a DataFrame
    df = pd.DataFrame(job_listings)

    # Optionally, print or process the DataFrame
    print(df.head())
    df.to_csv('abc1.csv')
else:
    print(f"Failed to retrieve data: {response.status_code}")
