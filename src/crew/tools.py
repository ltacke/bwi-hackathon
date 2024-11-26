from crewai.tools import BaseTool
from crewai_tools import SeleniumScrapingTool


class PolicySearchTool(BaseTool):
    name: str = "Policy Search Tool"
    description: str = "Search for relevant context matching the question about life insurance policies."

    def _run(self, query: str) -> str:
        return "Response from Tool"


class ScrapeBWI(BaseTool):
    name: str = "Scrape Website Tool"
    description: str = "Scrape a website_url from BWI to get the relevant information for a job posting."

    def _run(self, website_url: str) -> str:
        result = SeleniumScrapingTool(
            website_url, css_element=".jobDetailContent"
        ).run()
        return result
