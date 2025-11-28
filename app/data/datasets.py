import pandas as pd

#Create CSV Loading Function
def load_csv_to_table(conn, csv_path, table_name):
    #Check if CSV file exists
    
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
    


