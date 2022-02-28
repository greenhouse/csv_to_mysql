__filename = 'csv_engine.py'
__fname = 'csv_engine'
cStrDividerExcept = '***************************************************************'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

"""
    mysql database setup...
        $ mysql -u root -p password
        mysql> create dabase csv_test;
"""
import os
import csv
from pprint import pprint
import time
from db_controller import *

#========================================#
# Static Settings...
DB_DROP_CREATE_TBL = True
DB_TBL_NAME = 'csv_test_table'
CSV_TEST_FILE = 'test_0.csv'

# Dynamic vars...
LST_ROWS = []

# connect to database
DBC = db_controller()
is_conn = DBC.open_connection()
#========================================#

def create_csv_table(lst_col_names):
    # create new table w/ default cols (if exists, drop first)
    sql_stat = f"drop table if exists `{DB_TBL_NAME}`;"
    r = DBC.execute_statement(sql_stat)
    print(f'r={r}')
    sql_stat = (f"CREATE TABLE `{DB_TBL_NAME}` ("
                "`id` int(11) NOT NULL AUTO_INCREMENT, "
                "`dt_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, "
                "`dt_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, "
                "`dt_deleted` timestamp NULL DEFAULT NULL, "
                "UNIQUE KEY `ID` (`id`) USING BTREE"
                ") ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;")
    r = DBC.execute_statement(sql_stat)
    print(f'r={r}')
    for col_name in lst_col_names:
        sql_stat = (f"ALTER TABLE `{DB_TBL_NAME}` "
                    f"ADD `{col_name}` varchar(255) not null default '<nil>';")
        r = DBC.execute_statement(sql_stat)
        print(f'r={r}')
        
print(f" IMPORTs complete:- STARTING -> '{__filename}' file native run scripts...\n")

#ref: https://www.educba.com/python-read-csv-file/
with open(CSV_TEST_FILE, 'r') as file:
    print('opening csv file...')
    reader = csv.reader(file)
    LST_ROWS = list(reader)
    lst_tup_col_vals = []
    str_cols = None
    pprint(LST_ROWS)
    print('traversing csv rows...')
    for idx, each_row in enumerate(LST_ROWS):
        #print(idx, each_row)
        
        # if, currently in first row (parse column headers)
        if idx == 0:
            if DB_DROP_CREATE_TBL:
                print(f'  creating database table... (each_row={each_row})')
                status = DBC.begin_transaction() # begin trans before exe statements
                create_csv_table(each_row)
                status = DBC.commit_transaction() # commit trans after exe statements
            print(f'  parsing csv column names...   row[{idx}]')
            str_cols = str(tuple(each_row)).replace("'",'')
            
        # else, currently in data row (parse column values)
        else:
            if idx == 1: print(f'  parsing csv column values...   row[{idx}]', end='... ')
            else: print(f' row[{idx}]', end='... ')
            lst_tup_col_vals.append(tuple(each_row))
                
    print('\ninserting table column values...')
    status = DBC.begin_transaction() # begin trans before exe statements
    r = DBC.execute_insert_list(DB_TBL_NAME, str_cols, lst_tup_col_vals)
    status = DBC.commit_transaction() # commit trans after exe statements
    status = DBC.close_connection()
print(f"\n  DONE -> Executing additional '{__filename}' native run scripts ...")
print('#======================================================================#')

