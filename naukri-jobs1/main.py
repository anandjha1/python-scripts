import requests
import pandas as pd
import html2text
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# File path for the existing CSV
CSV_FILE = 'job_data_delhi_ncr.csv'

# Function to fetch job data
def fetch_job_data():
    url = (
        "https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc"
        "&searchType=adv&location=delhi%20%2F%20ncr&keyword=data%20entry%20operator"
        "&pageNo=1&k=data%20entry%20operator&l=delhi%20%2F%20ncr"
        "&seoKey=data-entry-operator-jobs-in-delhi-ncr&src=jobsearchDesk&latLong="
    )

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

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        return None

# Function to process job data
def process_job_data(data):
    jobs = data.get('jobDetails', [])
    job_data = []

    for job in jobs:
        title = job.get('title', 'N/A')
        job_id = job.get('jobId', 'N/A')
        company = job.get('companyName', 'N/A')
        skills = job.get('tagsAndSkills', 'N/A')
        placeholders = job.get('placeholders', [])

        experience = placeholders[0]['label'] if len(placeholders) > 0 else 'N/A'
        salary = placeholders[1]['label'] if len(placeholders) > 1 else 'N/A'
        locations = placeholders[2]['label'] if len(placeholders) > 2 else 'N/A'

        company_id = job.get('companyId', 'N/A')
        job_url = f"https://www.naukri.com{job.get('jdURL', '')}"
        jd = html2text.html2text(job.get('jobDescription', 'N/A'))

        ambitionBox = job.get('ambitionBoxData', {})
        ab_url = ambitionBox.get('Url', 'N/A')
        ab_reviews = ambitionBox.get('ReviewsCount', 'N/A')
        ab_rating = ambitionBox.get('AggregateRating', 'N/A')

        job_data.append([job_id, company, title, skills, experience, salary, locations, company_id, job_url, jd, ab_url, ab_reviews, ab_rating])

    return job_data

# Function to update the existing CSV file
def update_csv(job_data, file_path):
    if os.path.exists(file_path):
        # Load existing data
        existing_data = pd.read_csv(file_path)
        existing_ids = set(existing_data['job_id'])
        # Filter new jobs
        new_jobs = [job for job in job_data if job[0] not in existing_ids]
        if new_jobs:
            new_jobs_df = pd.DataFrame(new_jobs, columns=existing_data.columns)
            updated_data = pd.concat([existing_data, new_jobs_df], ignore_index=True)
            updated_data.to_csv(file_path, index=False)
            logging.info(f"Added {len(new_jobs)} new jobs to {file_path}")
        else:
            logging.info("No new jobs to add.")
    else:
        # Create new file if it doesn't exist
        columns = ['job_id', 'company', 'title', 'skills', 'experience', 'salary', 
                   'locations', 'company_id', 'job_url', 'jd', 'ab_url', 'ab_reviews', 'ab_rating']
        df = pd.DataFrame(job_data, columns=columns)
        df.to_csv(file_path, index=False)
        logging.info(f"File created: {file_path} with {len(job_data)} jobs.")

# Main script execution
def main():
    data = fetch_job_data()
    if data:
        job_data = process_job_data(data)
        update_csv(job_data, CSV_FILE)
    else:
        logging.error("No data to process.")

if __name__ == "__main__":
    main()
