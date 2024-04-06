#!/usr/bin/env python
from landing_page_reviewer.crew import LandingPageReviewerCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'landing_page_url': 'https://www.crewai.io/'
    }
    LandingPageReviewerCrew().crew().kickoff(inputs=inputs)