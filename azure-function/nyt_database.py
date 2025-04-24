from datetime import datetime
import pyodbc
from score import Score


class NytDatabase:
    def __init__(self, pyodbc_conn: pyodbc.Connection):
        self.conn = pyodbc_conn

    def insert_scores(self, scores: list[Score]) -> None:
        """Uploads a list of scores to the database, ignoring any that already exist."""
        if len(scores) == 0:
            return

        completion_date = scores[0].completion_date

        for score in scores:
            if score.completion_date != completion_date:
                ex_message = f"All scores must have the same completion date. Expected: {completion_date}. Actual: {score.completion_date}."
                raise ValueError(ex_message)

            if score.time_in_seconds < 0 or score.time_in_seconds > 32767:
                ex_message = f"Score of {score.time_in_seconds} seconds is invalid."
                raise ValueError(ex_message)

        db_completed_users = self._get_completed_users(completion_date)

        cursor = self.conn.cursor()
        sql_insert = "INSERT INTO Score VALUES (?, ?, ?)"
        for score in scores:
            if score.username not in db_completed_users:
                cursor.execute(sql_insert, score.username, score.completion_date, score.time_in_seconds)
        self.conn.commit()
        cursor.close()

    def _get_completed_users(self, completion_date: datetime.date) -> set[str]:
        """Retrieves the users that completed the crossword on the given date."""
        cursor = self.conn.cursor()
        sql_select = "SELECT Username FROM Score WHERE CompletionDate = ?"
        cursor.execute(sql_select, completion_date)
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
