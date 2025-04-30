from datetime import datetime
from nyt_leaderboard_scraper import score
import pyodbc


class NytDatabase:
    def __init__(self, pyodbc_conn: pyodbc.Connection):
        self.conn = pyodbc_conn

    def insert_scores(self, score_collection: score.ScoreCollection) -> None:
        """Inserts a collection of scores to the database, ignoring any that already exist."""
        if len(score_collection.scores) == 0:
            return

        crossword_date = score_collection.scores[0].crossword_date
        completed_users_in_db = self._get_completed_users(crossword_date)

        SQL_INSERT = "INSERT INTO Score VALUES (?, ?, ?)"

        cursor = self.conn.cursor()
        for score in score_collection:
            if score.username in completed_users_in_db:
                continue

            if score.time_in_seconds is None:
                continue

            cursor.execute(
                SQL_INSERT,
                score.username,
                score.crossword_date,
                score.time_in_seconds,
            )
        self.conn.commit()
        cursor.close()

    def _get_completed_users(self, crossword_date: datetime.date) -> set[str]:
        """Gets the users that already completed the crossword from the database."""
        SQL_SELECT = "SELECT Username FROM Score WHERE CompletionDate = ?"

        cursor = self.conn.cursor()
        cursor.execute(SQL_SELECT, crossword_date)
        db_users = cursor.fetchall()
        cursor.close()

        users = {db_user[0] for db_user in db_users}
        return users


def create_pyodbc_conn(
    driver: int,
    server: str,
    database: str,
    username: str,
    password: str,
    encrypt: bool = True,
    trust_server_certificate: bool = False,
    conn_timeout: int = 30,
) -> pyodbc.Connection:
    conn_string = f"Driver={{ODBC Driver {driver} for SQL Server}};"
    conn_string += f"Server={server};"
    conn_string += f"Database={database};"
    conn_string += f"Uid={username};"
    conn_string += f"Pwd={password};"
    if encrypt:
        conn_string += "Encrypt=yes;"
    else:
        conn_string += "Encrypt=no;"
    if trust_server_certificate:
        conn_string += "TrustServerCertificate=yes;"
    else:
        conn_string += "TrustServerCertificate=no;"
    conn_string += f"Connection Timeout={conn_timeout};"
    return pyodbc.connect(conn_string)
