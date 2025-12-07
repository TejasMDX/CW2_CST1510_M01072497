import pandas as pd
from pathlib import Path

#Create CSV Loading Function
def load_csv_to_table(conn, csv_path, table_name):
    #Check if CSV file exists

    csv_path = Path(csv_path)
    
    if csv_path.exists():
        print(f"{csv_path} exist")

    if not csv_path.exists():
        print(f"Error! {csv_path} does not exist")
        row_count = 0
    else:
        #Read CSV using pandas.read_csv()
        df = pd.read_csv(csv_path)

        

        #Use df.to_sql() to insert data
        df.to_sql(table_name, conn, if_exists= 'append', index=False)

        #Print success message and return row count
        row_count = len(df)
        print("Data has been sucessfully inserted")
    
    return row_count
    
def load_all_csv_data(conn):
    incidents_path = "DATA/cyber_incidents.csv"
    tickets_path = "DATA/it_tickets.csv"
    metadata_path = "DATA/datasets_metadata.csv"
    total_rows = 0

    print("Loading cyber_incidents...")
    rows = load_csv_to_table(conn, incidents_path, "cyber_incidents")
    total_rows += rows

    print("Loading it_tickets...")
    rows = load_csv_to_table(conn, tickets_path, "it_tickets")
    total_rows += rows

    print("Loading datasets_metadata...")
    rows = load_csv_to_table(conn, metadata_path, "datasets_metadata")
    total_rows += rows

    return total_rows


#CRUD FOR METADATA
def get_all_metadata(conn):
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY dataset_id DESC",
        conn
    )
    return df

def get_dataset_by_uploader_count(conn):

    query = """
    SELECT uploaded_by, COUNT(*) as count
    FROM datasets_metadata
    GROUP BY uploaded_by
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def insert_dataset(conn, name, rows, columns, uploaded_by, upload_date):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata 
        (name, rows, columns, uploaded_by, upload_date)
        VALUES (?, ?, ?, ?, ?)
    """, (name, rows, columns, uploaded_by, upload_date))
    conn.commit()

    return cursor.lastrowid

def update_dataset_rows(conn, dataset_id, new_rows):
    cursor = conn.cursor()

    sql = "UPDATE datasets_metadata SET rows = ? WHERE dataset_id = ?"

    cursor.execute(sql,(new_rows, dataset_id))
    conn.commit()
    return cursor.rowcount

def delete_dataset(conn, dataset_id):
    cursor = conn.cursor()
    
    sql = """
    DELETE FROM datasets_metadata
    WHERE dataset_id = ?
    """
    #Execute and commit
    cursor.execute(sql,(dataset_id,))
    conn.commit()
    #Return cursor.rowcount
    return cursor.rowcount