def create_users_table(conn):

    """Create users table."""
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ Users table created successfully!")

def create_cyber_incidents_table(conn):

    """Create cyber incidents table"""
    #Get a cursor from the connection
    cursor = conn.cursor()

    #Write CREATE TABLE IF NOT EXISTS SQL statement
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        category TEXT,
        severity TEXT,
        status TEXT,
        description TEXT,
        reported_by TEXT
    )
    """

    #Execute the SQL statement
    cursor.execute(create_table_sql)

    #Commit the changes
    conn.commit()

    #Print success message
    print("✅ Cyber incidents table created successfully!")

def create_datasets_metadata_table(conn):

    cursor = conn.cursor()
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        dataset_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        rows INTEGER,
        columns INTEGER,
        uploaded_by TEXT,
        upload_date TEXT
    )
    """

    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ Datasets metadata table created successfully!")

def create_it_tickets_table(conn):

    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS it_tickets(
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        priority TEXT,
        status TEXT,
        description TEXT,
        resolution_time_hours INTEGER,
        assigned_to TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ IT tickets table created successfully!")

def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)