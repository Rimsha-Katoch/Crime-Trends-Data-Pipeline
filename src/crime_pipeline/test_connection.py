
from sqlalchemy import text
from crime_pipeline.db import get_engine

def test_database_connection():

    engine = get_engine()

    try:
        with engine.begin() as connection:

            # Check database connection
            result = connection.execute(
                text("""
                    SELECT
                        current_database(),
                        current_user,
                        version();
                """)
            )

            database_info = result.fetchone()

            print("\nDatabase connected successfully!")
            print("Database:", database_info[0])
            print("User:", database_info[1])
            print("Version:", database_info[2])

            # Create a temporary testing table
            connection.execute(text("""
                CREATE TEMP TABLE connection_test (
                    id INTEGER PRIMARY KEY,
                    message TEXT
                );
            """))

            # Insert a test record
            connection.execute(
                text("""
                    INSERT INTO connection_test (id, message)
                    VALUES (1, 'Python connected successfully');
                """)
            )

            # Retrieve the inserted record
            test_result = connection.execute(
                text("SELECT * FROM connection_test;")
            )

            print("\nTesting database read and write:")

            for row in test_result:
                print(row)

            print("\nAll database tests passed!")

    finally:
        engine.dispose()


if __name__ == "__main__":
    test_database_connection()
