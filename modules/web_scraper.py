from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import time

def get_job_description(url):
    """Scrapes the job description text from a given URL using Selenium with headless Chrome."""
    try:
        # Create a random user agent
        ua = UserAgent()
        user_agent = ua.random
        
        # Set up Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')  # Use the new headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--allow-running-insecure-content')
        
        # Disable automation flags to be less detectable
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Set up the WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Add a page load timeout
        driver.set_page_load_timeout(30)
        
        # Modify navigator properties to make headless Chrome less detectable
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        })
        
        # Navigate to the URL
        driver.get(url)
        
        # Wait for dynamic content to load
        time.sleep(3)
        
        # Get the page source and extract text from body
        page_text = driver.find_element(By.TAG_NAME, 'body').text
        
        # Clean up
        driver.quit()
        
        return page_text
    except Exception as e:
        return f"Error retrieving job description: {str(e)}"
