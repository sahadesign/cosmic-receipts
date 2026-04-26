import os, json
import requests
from .state import AgentState
from dotenv import load_dotenv


class NasaTool:
    def __init__(self, nasa_api_key: str):
        self.nasa_api_key = nasa_api_key

    def fetch_nasa_apod(self, date: str) -> str:
        """Fetches the Astronomy Picture of the Day for a specific date."""
        url = "https://api.nasa.gov/planetary/apod"
        params = {"api_key": self.nasa_api_key, "date": date}

        try:
            response = requests.get(url, params)
            response.raise_for_status()
            data = response.json()
            return f"Date: {data.get('date')}\nTitle: {data.get('title')}\nDescription: {data.get('explanation')}"
        except Exception as e:
            print(f"Error fetching NASA data: {str(e)}")
            return ""

    def nasa_node(self, state: AgentState):
        try:
            plan_data = json.loads(state.plan[0])
            target_date = plan_data.get("nasa_date", "2021-12-25")
        except:
            target_date = "2021-12-25"
            
        results = self.fetch_nasa_apod(target_date)
        return {"nasa_results": results}


def nasa(state: AgentState):
    load_dotenv()
    n = NasaTool(nasa_api_key=os.getenv("NASA_TOKEN"))
    return n.nasa_node(state)