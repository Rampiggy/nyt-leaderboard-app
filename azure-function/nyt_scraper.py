from datetime import datetime, timedelta
from pytz import timezone
import re
import requests
from score import Score

# The URL that scores will be fetched from
LEADERBOARD_URL = "https://www.nytimes.com/puzzles/leaderboards"

# Headers to mimic a real browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.nytimes.com/",
}


class NytScraper:
    def __init__(self, session: requests.Session):
        self.session = session

    def scrape_leaderboard(self) -> list[Score]:
        """Scrapes the NYT leaderboard and returns a list of scores."""
        html = self._fetch_leaderboard()
        scores = _parse_html(html)
        return scores

    def _fetch_leaderboard(self) -> str:
        """Fetches the raw HTML from the NYT leaderboard using authentication cookies."""
        response = self.session.get(LEADERBOARD_URL, headers=HEADERS)
        html = response.text
        return html


def create_requests_session(nyt_s_cookie: str) -> requests.Session:
    """Creates a requests session with the NYT authentication cookie."""
    session = requests.Session()
    session.cookies.update({"NYT-S": nyt_s_cookie})
    return session


def _parse_html(html: str) -> list[Score]:
    """Parses the raw HTML to retrieve a list of scores."""
    pattern = r'"name":"([^"]+)".*?"solveTime":(?:"([^"]+)"|null)'
    matches = re.findall(pattern, html)
    scores = _convert_regex_matches_to_scores(matches)
    return scores


def _convert_regex_matches_to_scores(matches: list[tuple[str, str]]) -> list[Score]:
    """Converts the regex matches to a list of scores."""
    scores = []

    current_date = _get_current_crossword_date()
    for match in matches:
        username = match[0]

        time = match[1]
        if time == "":
            continue
        time_in_seconds = _convert_time_to_seconds(time)

        score = Score(username, current_date, time_in_seconds)
        scores.append(score)

    return scores


def _get_current_crossword_date() -> datetime.date:
    """Returns the current crosswword date."""
    eastern_timezone = timezone("US/Eastern")
    curr_datetime = datetime.now(eastern_timezone)

    saturday = 5
    sunday = 6
    six_pm = 18
    ten_pm = 22

    curr_date = curr_datetime.date()
    curr_weekday = curr_datetime.weekday()
    curr_weekday_is_a_weekend = curr_weekday == saturday or curr_weekday == sunday
    curr_hour = curr_datetime.hour

    if (curr_weekday_is_a_weekend and curr_hour >= six_pm) or (curr_hour >= ten_pm):
        return curr_date + timedelta(days=1)
    return curr_date


def _convert_time_to_seconds(time: str) -> int:
    """Converts a string time formatted in hh:mm:ss to an int of seconds."""
    time = time.split(":")
    if len(time) == 2:  # Minues:Seconds
        time_in_seconds = int(time[0]) * 60 + int(time[1])
    else:  # Hours:Minutes:Seconds
        time_in_seconds = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
    return time_in_seconds
