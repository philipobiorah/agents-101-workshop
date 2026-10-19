from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from google.adk.agents.llm_agent import Agent


def get_current_time(timezone: str = 'UTC') -> dict:
    """Returns the current date and time for a given IANA timezone.

    Args:
        timezone (str): The IANA timezone name (e.g., 'Africa/Lagos',
            'Africa/Johannesburg', 'Africa/Nairobi', 'Europe/London', or 'UTC').
            Defaults to 'UTC'.

    Returns:
        dict: A dictionary containing the status and the current time report.
    """
    try:
        tz = ZoneInfo(timezone)
        now = datetime.now(tz)
        return {
            'status': 'success',
            'timezone': timezone,
            'current_time': now.strftime('%Y-%m-%d %H:%M:%S %Z'),
        }
    except ZoneInfoNotFoundError:
        return {
            'status': 'error',
            'error_message': f"Unknown timezone '{timezone}'. Please provide a valid IANA timezone like 'Africa/Lagos' or 'UTC'.",
        }

root_agent = Agent(
    model='gemini-3.8-flash',  # or 'gemini-3.8-flash' if configured in your environment
    name='general_assistant_agent',
    description='A helpful assistant that answers user questions and can check the current time.',
    instruction=(
        'Answer user questions to the best of your knowledge. '
        'When asked for the current time, always use the `get_current_time` tool '
        'and convert the city or region into a valid IANA timezone (e.g., '
        'Port Harcourt -> Africa/Lagos, Pretoria -> Africa/Johannesburg, Kisii -> Africa/Nairobi).'
    ),
    tools=[get_current_time],
)