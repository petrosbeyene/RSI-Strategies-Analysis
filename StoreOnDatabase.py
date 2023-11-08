from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from retrieveData.RetrieveData import df  # Import the DataFrame created in the data retrieval step

# Create a SQLAlchemy engine to connect to your database
engine = create_engine('postgresql://postgres:1234%21%40%23%24@localhost/invsto_db')

# Create a session
Session = sessionmaker(bind=engine)

# Use a context manager for the session
with Session() as session:
    try:
        # If your DataFrame and database table have matching data types, you can use the "to_dict" method for efficiency
        data_list = df.to_dict(orient='records')
        
        # Create a text object for your SQL query
        sql_query = text("INSERT INTO stock_data (open, high, low, close, volume, instrument, datetime) "
                         "VALUES (:open, :high, :low, :close, :volume, :instrument, :datetime)")
        
        # Bulk insert data
        session.execute(sql_query, data_list)
        
        # Commit the changes
        session.commit()
    except Exception as e:
        session.rollback()  # Rollback changes if an exception occurs
        print(f"Error: {e}")

