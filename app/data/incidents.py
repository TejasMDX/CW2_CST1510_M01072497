import pandas as pd
from app.data.db import connect_database

def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    """Insert new incident."""
    #Get cursor
    cursor = conn.cursor()
    #Write INSERT SQL with parameterized query
    #Execute and commit
    cursor.execute("""
        INSERT INTO cyber_incidents 
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by))

    conn.commit()
    #Return cursor.lastrowid
    return cursor.lastrowid

def get_all_incidents(conn):
    """Get all incidents as DataFrame."""
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )
    return df

def update_incident_status(conn, incident_id, new_status):
    cursor = conn.cursor()
    #Write UPDATE SQL: UPDATE cyber_incidents SET status = ? WHERE id = ?
    sql = "UPDATE cyber_incidents SET status = ? WHERE id = ?"
    #Execute and commit
    cursor.execute(sql,(new_status, incident_id))
    conn.commit()
    #Return cursor.rowcount
    return cursor.rowcount

def delete_incident(conn, incident_id):
    cursor = conn.cursor()
    #Write DELETE SQL: DELETE FROM cyber_incidents WHERE id = ?
    sql = """
    DELETE FROM cyber_incidents
    WHERE id = ?
    """
    #Execute and commit
    cursor.execute(sql,(incident_id,))
    conn.commit()
    #Return cursor.rowcount
    return cursor.rowcount

def get_incidents_by_type_count(conn):
    """
    Count incidents by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_high_severity_by_status(conn):
    """
    Count high severity incidents by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_incident_types_with_many_cases(conn, min_count=5):
    """
    Find incident types with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df
