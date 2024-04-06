import os
import requests
from typing import Optional, Type, Any
from crewai_tools import BaseTool
from pydantic.v1 import BaseModel, Field


class FixedFetchHTMLToolSchema(BaseModel):
    """Base input schema for FetchHTMLTool."""
    pass


class FetchHTMLToolSchema(FixedFetchHTMLToolSchema):
    """Input schema for FetchHTMLTool."""
    website_url: str = Field(
        ..., description="Mandatory website URL to fetch the HTML content from.")


class FetchHTMLTool(BaseTool):
    name: str = "Fetch HTML Content"
    description: str = "A tool for fetching raw HTML content from a given URL."
    args_schema: Type[BaseModel] = FetchHTMLToolSchema
    website_url: Optional[str] = None
    cookies: Optional[dict] = None
    headers: Optional[dict] = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    def __init__(self, website_url: Optional[str] = None, cookies: Optional[dict] = None, **kwargs):
        super().__init__(**kwargs)
        if website_url is not None:
            self.website_url = website_url
            self.description += f" Specifically, it fetches content from {
                website_url}."
            self.args_schema = FixedFetchHTMLToolSchema
        if cookies is not None:
            self.cookies = {cookies["name"]: os.getenv(cookies["value"])}

    def _run(self, **kwargs: Any) -> Any:
        website_url = kwargs.get('website_url', self.website_url)
        response = requests.get(
            website_url, headers=self.headers, cookies=self.cookies if self.cookies else {})
        return response.text
