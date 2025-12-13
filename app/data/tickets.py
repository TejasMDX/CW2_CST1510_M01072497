import pandas as pd
from app.data.db import connect_database

def insert_ticket(conn, priority, description, status, assigned_to, resolution_time_hours):
    #Inserts a new IT support ticket into the database.
    #Returns the ID of the newly created ticket.
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO it_tickets
    (priority, description, status, resolution_time_hours, assigned_to)
    VALUES (?, ?, ?, ?, ?)
    """, (priority, description, status, resolution_time_hours, assigned_to))

    conn.commit()

    return cursor.lastrowid
    
def get_all_tickets(conn):

    #Retrieves all IT tickets as a Pandas DataFrame,

    df = pd.read_sql_query(
        "SELECT * FROM it_tickets ORDER BY ticket_id DESC",
        conn
    )
    
    return df

def update_ticket_status(conn, ticket_id, new_status):
    #Updates the status of a specific IT ticket.
    #Returns the number of rows affected.
    cursor = conn.cursor()

    sql = "UPDATE it_tickets SET status = ? WHERE ticket_id = ?"

    cursor.execute(sql,(new_status, ticket_id))
    conn.commit()
    #Return cursor.rowcount
    return cursor.rowcount

def delete_ticket(conn, ticket_id):
    #Deletes an IT ticket using its ticket ID.
    #Returns the number of deleted rows.
    cursor = conn.cursor()
    
    sql = """
    DELETE FROM it_tickets
    WHERE ticket_id = ?
    """
    #Execute and commit
    cursor.execute(sql,(ticket_id,))
    conn.commit()
    #Return cursor.rowcount
    return cursor.rowcount
    
def get_tickets_by_assigned_to_count(conn):
    #Returns the number of tickets grouped by assigned technician.
    #Demonstrates GROUP BY and ORDER BY usage.
    query = """
    SELECT assigned_to, COUNT(*) as count
    FROM it_tickets
    GROUP BY assigned_to
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_high_piority_by_status(conn):
    #Returns counts of HIGH priority tickets grouped by status.
    #Demonstrates WHERE filtering with GROUP BY.
    
    query = """
    SELECT status, COUNT(*) as count
    FROM it_tickets
    WHERE priority = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_assigned_to_with_many_cases(conn, min_count=5):
    #Returns technicians assigned to more than a specified number of tickets.
    #Demonstrates HAVING clause usage.
    query = """
    SELECT assigned_to, COUNT(*) as count
    FROM it_tickets
    GROUP BY assigned_to
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df
