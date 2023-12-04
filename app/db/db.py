import psycopg2
from typing import Optional


class DBConnection:
    dbname = "systemdb"
    user = "postgres"
    password = "12345678"
    host = "localhost"
    port = "5432"
    isActive = False

    conn = psycopg2.connect(database=dbname, user=user, password=password, host=host, port=port)

    POSTS_TABLE = "posts"
    WORKERS_TABLE = "workers"
    EDITION_TYPES_TABLE = "editiontypes"
    EDITION_TABLE = "edition"
    RECEIVED_EDITIONS_TABLE = "receivededitions"
    DELIVERY_TYPES_TABLE = "deliverytypes"
    ISSUED_EDITIONS_TABLE = "issuededitions"
    SUBSCRIPTIONS_TABLE = "subscriptions"
    FREQUENCY_OF_RELEASE_TABLE = "frequencyofrelease"

    def __init__(self):
        self.isActive=True

    def Cursor(self):
        return self.conn.cursor()

    def Connection(self):
        return self.conn

class DBController:
    connection:DBConnection

    def __init__(self):
        self.connection=DBConnection()

    def Cursor(self):
        return self.connection.Cursor()

    def Save(self):
        if self.connection.isActive:
            self.connection.Connection().commit()

    def Reset(self):
        if self.connection.isActive:
            self.connection.Connection().rollback()