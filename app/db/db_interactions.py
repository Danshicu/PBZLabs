from .db import DBController
from .db import DBConnection
from psycopg2 import sql
import datetime
import uuid

dbController = DBController()

def get_all_values(tableName):
    with dbController.Cursor() as cursor:
        try:
            query = __select_all_query__(tableName)
            cursor.execute(query)
            values = cursor.fetchall()
            return values
        except Exception as e:
            print(e)

def get_column_values(columnName, tableName):
    with dbController.Cursor() as cursor:
        try:
            query = __select_column_query__(columnName, tableName)
            cursor.execute(query)
            values = cursor.fetchall()
            return values
        except Exception as e:
            print(e)

def __select_all_query__(tableName):
    return f"select * from {tableName}"

def __select_column_query__(columnName, tableName):
    return f"select {columnName} from {tableName}"

def insert_into(tableName, values):
    with dbController.Cursor() as cursor:
        try:
            query = f"INSERT INTO {tableName} VALUES {__build_insert_values__(values)}"
            deltaCount = get_rows_count(tableName)-len(values)
            if deltaCount>=1:
                for i in range(0,deltaCount):
                    defValue = 'DEFAULT'
                    values.insert(0, defValue)
            elif deltaCount<0:
                raise Exception('incorrect values count')
            cursor.execute(query, values)
            dbController.Save()
        except Exception as e:
            print(e)

def __build_insert_values__(values):
    length = len(values)
    if length > 0:
        finalSTR = "("
        for i in range(0, length):
            finalSTR +="%s, "
        finalSTR = finalSTR[:-2]+')'
        return finalSTR

def __build_insert_columns__(tableName):
    query = f"select column_name FROM information_schema.columns WHERE table_name = '{tableName}';"
    with dbController.Cursor() as cursor:
        try:
            cursor.execute(query)
            columnNames = [row[0] for row in cursor]
            return columnNames
        except Exception as e:
            print(e)

def get_post_id_to_name_dictionary():
    tuples = get_all_values(DBConnection.POSTS_TABLE)
    return create_dictionary_from_tuples(tuples)

def get_worker_uuid_name_post_tuples():
    workers = get_all_values(DBConnection.WORKERS_TABLE)
    post_name_to_id = get_post_id_to_name_dictionary()
    uuid_list = [workers[i][0] for i in range(0, len(workers))]
    worker_tuples = list()
    for i in range(0, len(workers)):
        tempTuple = (workers[i][1], post_name_to_id[workers[i][2]])
        worker_tuples.append(tempTuple)
    tuples = dict(zip(uuid_list, worker_tuples))
    return tuples

def get_edition_index_to_name_dictionary():
    tuples = get_all_values(DBConnection.EDITION_TABLE)
    edition_tuples = list()
    for i in range(0, len(tuples)):
        tempTuple = (tuples[i][0], tuples[i][1])
        edition_tuples.append(tempTuple)
    tupless = dict(edition_tuples)
    return tupless

def get_edition_cost_from_index(index:str):
    query = f"SELECT subscriptionPerCopyCost FROM {DBConnection.EDITION_TABLE} WHERE subscriptionIndex = '{index}'"
    with dbController.Cursor() as cursor:
        try:
            cursor.execute(query)
            return cursor.fetchone()[0]
        except Exception as e:
            print(e)

def get_rows_count(tableName):
    query = f"SELECT COUNT(column_name) FROM information_schema.columns WHERE table_name = '{tableName}';"
    with dbController.Cursor() as cursor:
        try:
            cursor.execute(query)
            return cursor.fetchone()[0]
        except Exception as e:
            print(e)

def create_dictionary_from_tuples(inputTuple):
    resultDictionary = dict((x,y) for x,y in inputTuple)
    return resultDictionary

def edit_subscription(values, uuid:str):
    update_query = sql.SQL("UPDATE subscriptions SET {} WHERE thisID = %s;").format(
        sql.SQL(', ').join(
            sql.Composed([sql.Identifier(col), sql.SQL(' = %s')]) for col in values
        )
    )
    with dbController.Cursor() as cursor:
        try:
            cursor.execute(update_query, list(values.values()) + [uuid])
            dbController.Save()
        except Exception as e:
            print(e)

def edit_worker(values, uuid:str):
    update_query = f"UPDATE workers SET fullname = '{values[1]}', postId ={values[2]}, isActive = {values[3]} WHERE thisID = '{uuid}';"
    with dbController.Cursor() as cursor:
        try:
            cursor.execute(update_query)
            dbController.Save()
        except Exception as e:
            print(e)

def receive_edition():
    pass

def delete_worker(uuid: str):
    query = f"DELETE FROM {DBConnection.WORKERS_TABLE} WHERE thisID = '{uuid}';"
    with dbController.Cursor() as cursor:
        try:
            cursor.execute(query)
            dbController.Save()
        except Exception as e:
            print(e)

def delete_subscription(uuid: str):
    query = f"DELETE FROM {DBConnection.SUBSCRIPTIONS_TABLE} WHERE thisID = '{uuid}';"
    with dbController.Cursor() as cursor:
        try:
            cursor.execute(query)
            dbController.Save()
        except Exception as e:
            print(e)

def get_editions_by_year():
    pass

def get_worker_received_edition():
    pass

def get_non_received_editions():
    pass

def find_key_by_value(dictionary, value):
    for key in dictionary.keys():
        if dictionary[key] == value:
            return key

'''def get_dictionary_strings_from(tableName):
    tuples = get_all_values(tableName)
    dictValues = []
    for row in tuples:
        dictValues.append(__build_dictionary_string(row[0], row[1]))
    return dictValues

def __build_dictionary_string(key, value):
    return f"{key}-{value}"

def get_key_from_string(string):
    return string.split('-')[0]'''


#print(get_edition_index_to_name_dictionary())

#print(get_column_values('thisID', db.POSTS_TABLE))
#print(__build_insert_columns__(DBConnection.FREQUENCY_OF_RELEASE_TABLE))

#with dbController.Cursor() as cursor:
#    query = "create table frequencyOfRelease(thisID serial primary key,frequency interval NOT NULL,CHECK(frequency > interval'1 day'));"
#    cursor.execute(query)
#build_insert_columns(db.WORKERS_TABLE)

#insert_into(db.WORKERS_TABLE, ['Victor Pavlowww', 1, True])

#print(get_rows_count(db.WORKERS_TABLE))
#rows = get_all_values(db.POSTS_TABLE)
#print(type(rows))
#for row in rows:
    #print(type(row))
    #print(row)
#print(uuid.uuid4())
#workers = get_all_values(db.WORKERS_TABLE)
#print(type(workers))
#print(workers)
#for row in workers:
#    print(type(row))
#    print(row)

#edit_worker(['1', '2', '3'], '4')