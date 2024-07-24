from crewai_tools import tool
import requests
from bs4 import BeautifulSoup


class ScraperTool:
    @tool("Scraper Tool")
    def scrape(url: str):
        "Useful tool to scrap a website content, use to learn more about a given url."
        result = requests.get(url)
        src = result.content
        if result.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(src, 'html.parser')
            # print(soup)
            return soup
        else:
            print("Failed to retrieve the webpage")
