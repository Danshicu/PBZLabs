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
    EDITION_TYPES_TABLE = "editionTypes"
    EDITION_TABLE = "edition"
    RECEIVED_EDITIONS_TABLE = "receivedEditions"
    DELIVERY_TYPES_TABLE = "deliveryTypes"
    ISSUED_EDITIONS_TABLE = "issuedEditions"
    SUBSCRIPTIONS_TABLE = "subscriptions"
    FREQUENCY_OF_RELEASE_TABLE = "frequencyOfRelease"

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