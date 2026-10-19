from datetime import datetime
from zoneinfo import ZoneInfo
from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool



# 1. Custom Python Function Tool
def get_current_time(timezone: str = 'UTC') -> dict:
    """Returns the current date and time for a given IANA timezone (e.g. 'Africa/Lagos')."""
    now = datetime.now(ZoneInfo(timezone))
    return {'status': 'success', 'current_time': now.strftime('%Y-%m-%d %H:%M:%S %Z')}


# 2. Dedicated Search Specialist Agent using built-in google_search
search_agent = Agent(
    model='gemini-3.8-flash',
    name='google_search_agent',
    description='Searches the web using Google Search for up-to-date information.',
    instruction='Use Google Search to find accurate, up-to-date answers to the query.',
    tools=[google_search],
)





# 3. Root Agent combining Custom Function Tool + Search AgentTool
root_agent = Agent(
    model='gemini-3.8-flash',
    name='general_assistant_agent',
    description='A helpful assistant for user questions.',
    instruction=(
        'Answer user questions to the best of your knowledge. '
        'Use `get_current_time` for time/date questions, and `google_search_agent` '
        'whenever you need live information from the web.'
    ),
    tools=[
        get_current_time,
        AgentTool(agent=search_agent),
    ],
)