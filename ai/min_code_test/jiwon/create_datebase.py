import sqlite3

# Function to initialize the database
def initialize_database():
    # Connect to the SQLite database
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Drop the table if it exists (this will reset the database)
    cursor.execute('DROP TABLE IF EXISTS 제품')

    # Create the table with an additional column for storing images
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS 제품 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datetime TEXT,            -- 날짜 및 시간 (ISO 형식으로 저장: "YYYY-MM-DD HH:MM:SS")
        uuid TEXT UNIQUE,         -- UUID (고유 식별자)
        is_defective INTEGER,     -- 제품 상태 (예: "양품" 또는 "불량품")
        defect_reason TEXT,       -- 불량 이유 (불량인 경우에만 이유 저장)
        image BLOB                -- 제품 이미지 (BLOB 타입으로 저장)
    )
    '''

    # Execute the query to create the table
    cursor.execute(create_table_query)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print("Database initialized and table created with image support.")

# Initialize the database
initialize_database()
