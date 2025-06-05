# LinkedIn Applied Jobs Scraper

A Python script to scrape and track your applied jobs from LinkedIn. This tool helps you maintain a record of all the jobs you've applied to on LinkedIn, including application dates, job titles, companies, and statuses.

## Author

[sk3pp3r](https://github.com/sk3pp3r)

## Features

- Scrapes your applied jobs from LinkedIn
- Saves job data in JSON format
- Tracks application dates and statuses
- Easy to use command-line interface
- Automatic Chrome driver management
- Beautiful data formatting

## Prerequisites

- Python 3.8 or higher
- LinkedIn account
- Chrome browser installed

## Installation

1. Clone this repository:

```bash
git clone https://github.com/sk3pp3r/linkedin-applied-jobs-scraper.git
cd linkedin-applied-jobs-scraper
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Make sure you're logged into LinkedIn in your Chrome browser
2. Run the script:

```bash
python applied_jobs_scraper.py
```

The script will:

- Open your LinkedIn applied jobs page
- Scrape all your applied jobs
- Save the data in `data/merged_jobs_YYYY-MM-DD.json`

## Example Output

![Screenshot of script output](@image.png)

## Data Structure

The scraped data is saved in JSON format with the following structure:

```json
{
    "job_title": "string",
    "company": "string",
    "application_date": "YYYY-MM-DD",
    "status": "string",
    "job_url": "string"
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for personal use only. Please respect LinkedIn's terms of service and use this tool responsibly
