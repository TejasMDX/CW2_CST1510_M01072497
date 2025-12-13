#create users table
def create_users_table(conn):

    """Create users table."""
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # SQL statement to create the users table if it does not already exist
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    # Execute the SQL statement
    cursor.execute(create_table_sql)
    # Save changes to the database
    conn.commit()
    print("✅ Users table created successfully!")

#create cyber incidents table
def create_cyber_incidents_table(conn):

    """Create cyber incidents table"""
    #Get a cursor from the connection
    cursor = conn.cursor()

    #create the cyber incidents table
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

#create datasets metadata table
def create_datasets_metadata_table(conn):

    cursor = conn.cursor()
    #creating datasets metadata table
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
    # Execute the SQL command
    cursor.execute(create_table_sql)
    # Commit database changes
    conn.commit()
    print("✅ Datasets metadata table created successfully!")

#create it tickets table
def create_it_tickets_table(conn):

    # Create a cursor for database operations
    cursor = conn.cursor()
    # SQL statement to create IT tickets table
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

    # Execute SQL statement
    cursor.execute(create_table_sql)
    # Save changes
    conn.commit()
    # Confirmation message
    print("✅ IT tickets table created successfully!")

#Creates all database tables required by the system
def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)