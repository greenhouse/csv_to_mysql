#auther: eric greenhouse
__filename = 'db_controller.py'
__fname = 'db_controller'
cStrDividerExcept = '***************************************************************'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

from pprint import *
from db_engine import *
from utilities import *
ENABLE_LOGGING = False

class db_controller:
    dbe = None

    def execute_insert_list(self, tble, str_cols, lst_tup_col_vals):
        if self.dbe.is_connected():
            sql_stat = self.dbe.gen_insert_stat_list(tble, str_cols, lst_tup_col_vals, append_trans=False)
            #return self.execute_statement(sql_stat)
            return self.execute_statement(sql_stat.decode('utf-8'))
        return False
        
    def execute_statement(self, sql_stat):
        if self.dbe.is_connected():
            result = self.dbe.exe_sql_statement(sql_stat)
            if result != -1:
                return result
        return False
            
    def close_connection(self):
        if not self.dbe.is_connected() or self.dbe.close_database_connection() == 0:
            return True
        return False

    def rollback_transaction(self):
        if self.dbe.is_connected():
            return self.dbe.rollback_database_transaction() == 0
        return False
        
    def begin_transaction(self):
        if self.dbe.is_connected():
            return self.dbe.begin_database_transaction() == 0
        return False
    
    def commit_transaction(self):
        if self.dbe.is_connected():
            return self.dbe.commit_database_transaction() == 0
        return False
        
    def open_connection(self):
        if self.dbe.is_connected() or self.dbe.open_database_connection() == 0:
            return True
        return False
    
    def clear_transactions(self):
        self.dbe.clear_lst_trans()
        return True
        
    def __init__(self):
        self.dbe = db_engine(open_conn=False)
