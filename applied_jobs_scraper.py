import os
import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

class LinkedInJobsScraper:
    def __init__(self):
        self.setup_driver()
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)

    def setup_driver(self):
        """Set up the Chrome WebDriver with appropriate options."""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        # Uncomment the line below if you want to run in headless mode
        # chrome_options.add_argument("--headless")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def scrape_applied_jobs(self):
        """Scrape applied jobs from LinkedIn."""
        try:
            # Navigate to LinkedIn applied jobs page
            self.driver.get("https://www.linkedin.com/my-items/saved-jobs/")
            
            # Wait for the page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-saved-job-card"))
            )

            # Scroll to load all jobs
            self._scroll_to_bottom()

            # Get the page source and parse with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            jobs = []

            # Find all job cards
            job_cards = soup.find_all("div", class_="jobs-saved-job-card")
            
            for card in job_cards:
                job_data = self._extract_job_data(card)
                if job_data:
                    jobs.append(job_data)

            return jobs

        except Exception as e:
            print(f"Error scraping jobs: {str(e)}")
            return []

    def _scroll_to_bottom(self):
        """Scroll to the bottom of the page to load all jobs."""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def _extract_job_data(self, card):
        """Extract job data from a job card."""
        try:
            job_title = card.find("a", class_="job-card-list__title").text.strip()
            company = card.find("span", class_="job-card-container__company-name").text.strip()
            job_url = card.find("a", class_="job-card-list__title")["href"]
            
            # Extract application date if available
            application_date = None
            date_element = card.find("time")
            if date_element:
                application_date = date_element.text.strip()

            return {
                "job_title": job_title,
                "company": company,
                "application_date": application_date,
                "status": "Applied",
                "job_url": job_url
            }
        except Exception as e:
            print(f"Error extracting job data: {str(e)}")
            return None

    def save_jobs_to_json(self, jobs):
        """Save jobs data to a JSON file."""
        if not jobs:
            print("No jobs to save.")
            return

        # Create filename with current date
        filename = f"merged_jobs_{datetime.now().strftime('%Y-%m-%d')}.json"
        filepath = os.path.join(self.data_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=4, ensure_ascii=False)
        
        print(f"Saved {len(jobs)} jobs to {filepath}")

    def close(self):
        """Close the WebDriver."""
        self.driver.quit()

def main():
    scraper = LinkedInJobsScraper()
    try:
        print("Starting to scrape applied jobs...")
        jobs = scraper.scrape_applied_jobs()
        scraper.save_jobs_to_json(jobs)
        print("Scraping completed successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()