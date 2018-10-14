import os
import sqlite3
import csv
import cStringIO


def cmp_select_output_with_csv(csv_file_name, sqlite3_db_file, select_query_file_name, sort=True,
                               header=False, sql_parameters=()):
    # We have to read the csv file, run the query and compare the results. Returns true if equal false otherwise.

    # Read csv file.
    csv_file_header, csv_file_contents = read_from_csv_file(csv_file_name)

    # Run query and convert it to csv representation, so that we can directly compare.
    csv_file_like = cStringIO.StringIO()
    save_to_csv_file_like(sqlite3_db_file, csv_file_like, read_from_file(select_query_file_name), sql_parameters)
    # Following line is kind of a hack. Ideally csv module should be able to read from StringIO object treating it like
    # any other file but this version of csv doesn't work that way. We are explicitly reading the entire data in StringIO
    # and sending to csv reader
    # Ideal call should be:
    # select_csv_schema, select_csv_contents = read_from_csv_file_like(csv_file_like) # Not working as explained above.
    select_csv_schema, select_csv_contents = read_from_csv_file_like(csv_file_like.getvalue().splitlines())

    # Compare
    if sort:
        contents_match = cmp(sorted(csv_file_contents), sorted(select_csv_contents)) == 0
    else:
        contents_match = cmp(csv_file_contents, select_csv_contents) == 0

    if header:
        headers_match = cmp(csv_file_header, select_csv_schema) == 0
        return contents_match and headers_match
    else:
        return contents_match


def read_from_file(file_name):
    with open(file_name, 'rb') as file_contents:
        return file_contents.read()


def read_from_csv_file(csv_file_name):
    with open(csv_file_name, 'rb') as csvfile:
        return read_from_csv_file_like(csvfile)


def read_from_csv_file_like(csv_file_like):
    csv_reader = csv.reader(csv_file_like)
    header = []
    data = []
    for row in csv_reader:
        if len(row) != 0:  # check to ignore empty lines in csv file.
            if len(header) == 0:
                header = row
            else:
                data.append(row)
    return header, data


def save_to_csv_file_like(sqlite3_db_file, csv_file_like, select_query, sql_parameters=()):
    schema, all_rows = get_schema_and_all_rows(sqlite3_db_file, select_query, sql_parameters)
    writer = csv.writer(csv_file_like)
    writer.writerow(schema)
    writer.writerows(all_rows)


def save_to_csv_file(sqlite3_db_file, csv_file_name, select_query, sql_parameters=()):
    with open(csv_file_name, 'wb') as csvfile:
        save_to_csv_file_like(sqlite3_db_file, csvfile, select_query, sql_parameters)


def get_schema_and_all_rows(sqlite3_db_file, select_query, sql_parameters=()):
    # Check that database exists, otherwise sqlite3 API will create new database.
    if not valid_db(sqlite3_db_file):
        raise ValueError("Database doesn't exist.")
    # Query should be select query
    # Some students are also using CTE instead of select query. Therefore, removing the following check for now.
    # Right way to stop students from cheating would be to have different test cases on Coursera server.
    '''
    if not is_select_query(select_query):
        raise ValueError("Query should be one select query.")
    '''
    conn = None
    try:
        # Create connection.
        conn = sqlite3.connect(sqlite3_db_file)
        # Execute query.
        cur = conn.execute(select_query, sql_parameters)
        # Get data.
        all_rows = cur.fetchall()
        # Get schema.
        schema = tuple(x[0] for x in cur.description)
        return schema, all_rows
    finally:
        if conn is not None:
            conn.close()


def valid_db(sqlite3_db_file):
    return os.path.isfile(sqlite3_db_file)


def is_select_query(query):
    starts_with_select = query.strip().lower().startswith('select')
    single_query = is_single_query(query)
    return starts_with_select and single_query


def is_single_query(query):
    # We need to execute query against a dummy database and catch the warning that multiple queries are executed. Later
    return True
