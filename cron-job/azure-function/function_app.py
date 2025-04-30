import azure.functions as func
from credential import nyt_s_cookie, sql_server, sql_database, sql_username, sql_password
from datetime import datetime
import logging
import nyt_database
import nyt_scraper

app = func.FunctionApp()


@app.timer_trigger(schedule="0 55 21,1 * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False)
def daily_upload(myTimer: func.TimerRequest) -> None:
    today = datetime.today()
    todays_date = today.date()
    todays_time = today.time()

    if myTimer.past_due:
        logging.critical(f"Timer is past due on {todays_date} at {todays_time}!")

    logging.info(f"Executing on {todays_date} at {todays_time}.")

    try:
        session = nyt_scraper.create_requests_session(nyt_s_cookie)
        scraper = nyt_scraper.NytScraper(session)
        scores = scraper.scrape_leaderboard()
        session.close()
    except Exception as e:
        logging.critical(f"Failed to scrape the NYT leaderboard: {e}")
        raise e

    try:
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
        db.insert_scores(scores)
        conn.close()
    except Exception as e:
        logging.critical(f"Failed to upload scores to the database: {e}")
        raise e
