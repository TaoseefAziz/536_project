import requests
from bs4 import BeautifulSoup

def get_job_description(url):
    """Scrapes the job description text from a given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # For this sample, we extract all text from the <body> tag.
        text = soup.body.get_text(separator="\n", strip=True)
        return f"JOB DESCRIPTION:\n{text}"
    except Exception as e:
        return f"Error retrieving job description: {str(e)}"

