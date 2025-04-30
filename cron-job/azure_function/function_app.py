import azure.functions as func
from credential import (
    nyt_s_cookie,
    sql_server,
    sql_database,
    sql_username,
    sql_password,
)
from datetime import datetime
import nyt_database
from nyt_leaderboard_scraper import scraper, score
import logging

app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 55 21,1 * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def daily_upload(myTimer: func.TimerRequest) -> None:
    today = datetime.today()
    todays_date = today.date()
    todays_time = today.time()

    if myTimer.past_due:
        logging.critical(f"Timer is past due on {todays_date} at {todays_time}!")

    logging.info(f"Executing on {todays_date} at {todays_time}.")

    get_and_upload_scores()


def get_and_upload_scores() -> None:
    try:
        score_collection = get_scores()
    except Exception as e:
        logging.critical(f"Failed to scrape the NYT leaderboard: {e}")
        raise e

    try:
        upload_scores(score_collection)
    except Exception as e:
        logging.critical(f"Failed to upload the scores to the database: {e}")
        raise e


def get_scores() -> score.ScoreCollection:
    session = scraper.create_requests_session(nyt_s_cookie)
    score_collection = scraper.scrape_leaderboard(session)
    session.close()
    _validate_scores(score_collection)
    return score_collection


def _validate_scores(score_collection: score.ScoreCollection) -> None:
    if len(score_collection.scores) == 0:
        ex_message = "Score collection is empty."
        raise ValueError(ex_message)

    crossword_date = score_collection.scores[0].crossword_date

    for score in score_collection:
        if score.crossword_date != crossword_date:
            ex_message = f"All scores must have the same completion date. "
            +"Expected: {completion_date}. Actual: {score.completion_date}."
            raise ValueError(ex_message)

        if score.time_in_seconds is None:
            continue

        if score.time_in_seconds < 0 or score.time_in_seconds > 32767:
            ex_message = f"Score of {score.time_in_seconds} seconds is invalid."
            raise ValueError(ex_message)


def upload_scores(score_collection: score.ScoreCollection) -> None:
    conn = nyt_database.create_pyodbc_conn(
        driver=18,
        server=sql_server,
        database=sql_database,
        username=sql_username,
        password=sql_password,
        encrypt=True,
        trust_server_certificate=False,
        conn_timeout=30,
    )
    db = nyt_database.NytDatabase(conn)
    db.insert_scores(score_collection)
    conn.close()
