# csv_to_mysql
generate mysql database from csv

    1) have mysql installed and create a database called 'csv_test'
    2) create a .env file in sites/ to store the mysql credentials
        - or you can just write them in manually inside sites/env.py
    3) run '$ python3 csv_engine.py'
        - parses and pushes test_0.csv to local mysql database
        - csv must be 'comma delimited'
        
