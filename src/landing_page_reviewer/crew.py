from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI

from landing_page_reviewer.tools.FetchHTMLTool import FetchHTMLTool


@CrewBase
class LandingPageReviewerCrew():
    """LandingPageReviewer crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self) -> None:
        self.llm = ChatOpenAI()
        self.scrape_tool = FetchHTMLTool()

    @agent
    def web_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['web_scraper'],
            tools=[self.scrape_tool],
            verbose=True,
        )

    @agent
    def content_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_analyzer'],
            verbose=True
        )

    @task
    def scraping_task(self) -> Task:
        return Task(
            config=self.tasks_config['scraping_task'],
            agent=self.web_scraper(),
            output_file='landing_page.html',
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysis_task'],
            agent=self.content_analyzer(),
            output_file='landing_page_review.md',

        )

    @crew
    def crew(self) -> Crew:
        """Creates the LandingPageReviewer crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.hierarchical,
            verbose=2,
            manager_llm=self.llm,
        )
