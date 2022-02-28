#auther: eric greenhosue
__filename = 'db_engine.py'
__fname = 'db_engine'
cStrDividerExcept = '***************************************************************'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

from sites import * #required: sites/__init__.py

'''
# https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
# https://docs.sqlalchemy.org/en/13/dialects/mysql.html#module-sqlalchemy.dialects.mysql.pymysql
    mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
# https://pymysql.readthedocs.io/en/latest/user/examples.html
# https://pymysql.readthedocs.io/en/latest/modules/connections.html#pymysql.connections.Connection.ping
    #NOTE: '$ pip3' == '$ python3.6 -m pip'
        $ python3 -m pip install PyMySQL
        $ python3.7 -m pip install PyMySQL
    '''
import pymysql.cursors
from utilities import *
ENABLE_LOGGING = False

#print(__filename, f" IMPORTs complete:- STARTING -> file '{__filename}' . . . ")

dbHost = DB_HOST #read_env()
dbName = DB_NAME #read_env()
dbUser = DB_USER #read_env()
dbPw = DB_PW     #read_env()

#db = None
#cur = None

#strErrCursor = "global var cur == None, returning -1"
#strErrConn = "FAILED to connect to db"

#====================================================#
##              db connection support               ##
#====================================================#
class db_engine:
    __classname = 'db_engine'
    db = None
    cur = None
    lst_trans = []
    
    def __init__(self, open_conn=False):
        if open_conn:
            self.open_database_connection()

    def is_connected(self):
        if self.db == None: return False
        try:
            # Raises:	Error – If the connection is closed and reconnect=False
            self.db.ping(reconnect=False)
            return True
        except Exception as e:
            printException(e)
            return False

    def get_lst_trans(self, copy=False):
        return list(self.lst_trans) if copy else self.lst_trans

    def clear_lst_trans(self):
        self.lst_trans = []

    def exe_sql_statement(self, sql_stat):
        funcname = f'exe_sql_statement()'
        #print('GO _', funcname)
        #argsTup = (dictColVals, lstColSelect, bGetAll)
        argsTup = ()
        strProc = sql_stat
        strOutParam = None
        result = self.exe_database_task(argsTup, strProc, strOutParam, raw_state=True)
        if result[0] == -1:
            print(f"!! ERROR -> exe_database_task() returned -1")
            return result[0]
        return result
        
    def exe_sql_proc(self, proc_name, argsTup):
        funcname = f'exe_sql_proc()'
        log_info = 'call '+proc_name+str(argsTup) if False else 'call '+proc_name+'(...)'
        if ENABLE_LOGGING: print(log_info)
        strProc = proc_name
        strOutParam = None
        result = self.exe_database_task(argsTup, strProc, strOutParam, raw_state=False)
        if result[0] == -1:
            print(f"!! ERROR -> exe_database_task() returned -1")
            return result[0]
        return result
                
    def exe_sql_lst_trans_statements(self):
        for idx, sql_stat in enumerate(self.lst_trans):
            #if ENABLE_LOGGING: print(sql_stat)
            #argsTup = (dictColVals, lstColSelect, bGetAll)
            argsTup = ()
            strProc = sql_stat
            strOutParam = None
            result = self.exe_database_task(argsTup, strProc, strOutParam, raw_state=True)
            if result[0] == -1:
                print(f"!! ERROR -> self.lst_trans[{idx}] _ exe_database_task() returned -1")
                return result[0]
        self.lst_trans = []
        return 0

    """
        insert into `res_wps_win`
            (fk_race_id, fin_place, race_pgm_val, val)
        values
            (-37, 1, 4, 'val'),
            (-37, 2, 6, 'val');
    """
    # generate insert statement with values list
    def gen_insert_stat_list(self, tble, str_cols, lst_tup_col_vals, append_trans=False):
        q = f'INSERT INTO `{tble}` ' + str_cols + ' VALUES '
        str_vals = ''.join(str(lst_tup_col_vals)).strip('[]')
        q = q + str_vals + ';'
        q = q.encode('utf-8')
        if append_trans: self.lst_trans.append(q)
        return q

    # generate single values insert statement
    def gen_insert_stat(self, tble, dict_col_vals, append_trans=False):
        q = f'INSERT INTO `{tble}`'
        c = v = b'('
        for idx, key in enumerate(dict_col_vals):
            bKey = key.encode('utf-8')
            bVal = dict_col_vals[key] if isinstance(dict_col_vals[key], bytes) or isinstance(dict_col_vals[key], int) else dict_col_vals[key].encode('utf-8')
            
            # case: 'Breeder: Donna J. Burcham & M. H. "Jim" Burcham' (1999.zip _ idx:36 i think)
            bVal = bVal if isinstance(bVal, int) else bVal.replace(b'"', b'')
            if idx < len(dict_col_vals) -1:
                c = c + bKey + b','
                #v = v + b'"' +bVal+ b'"' + b','
                if isinstance(bVal, int): v = v + str(bVal).encode('utf-8') + b','
                else: v = v + b'"' +bVal+ b'"' + b','
            else:
                c = c + bKey + b')'
                #v = v + b'"' +bVal+ b'"' + b')'
                if isinstance(bVal, int): v = v + str(bVal).encode('utf-8') + b')'
                else: v = v + b'"' +bVal+ b'"' + b')'
                        
        q = q.encode('utf-8') + b' ' + c + b' VALUES ' + v + b';'
        if append_trans: self.lst_trans.append(q)
        return q

    def gen_update_stat(self, tble, row_id, col, val, append_trans=False):
        q = f'UPDATE `{tble}` set {col} = "{val}" where id = {row_id};'
        q = q.encode('utf-8')
        if append_trans: self.lst_trans.append(q)
        return q
        
    def gen_update_where_stat(self, tble, col, val, where_cols, where_vals, append_trans=False):
        #q = f'UPDATE `{tble}` set {col} = "{val}" where {where_cols} = {where_vals};'
        q = f'UPDATE `{tble}` set {col} = "{val}" where {where_cols[0]} = {where_vals[0]} and {where_cols[1]} = {where_vals[1]};'
        q = q.encode('utf-8')
        if append_trans: self.lst_trans.append(q)
        return q

    def open_database_connection(self):
        ''' NOTE: commenting this causes exception / crash (can't figure out why
            Traceback (most recent call last):
              File "/Users/greenhouse/devzndlabs/git/zndlabs/src/pdf_engine.py", line 1073, in <module>
                is_conn = DBC.open_connection()
              File "/Users/greenhouse/devzndlabs/git/zndlabs/src/db_controller.py", line 66, in open_connection
                if self.dbe.is_connected() or self.dbe.open_database_connection() == 0:
              File "/Users/greenhouse/devzndlabs/git/zndlabs/src/db_engine.py", line 104, in open_database_connection
                funcname = f'[{__filename}] open_database_connection'
            NameError: name '_db_engine__filename' is not defined
            greenhouses-MacBook-Pro:src greenhouse$
        '''
        #funcname = f'[{__filename}] open_database_connection'
        funcname = 'open_database_connection()'
        print('GO _', funcname)

        # Connect to DB #
        try:
            # legacy manual db connection #
            self.db = pymysql.connect(host=dbHost,
                                 user=dbUser,
                                 password=dbPw,
                                 db=dbName,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
            self.cur = self.db.cursor()
            if ENABLE_LOGGING: print(funcname, ' >> CONNECTED >> to db successfully!')
        except Exception as e:
            print('!! Exception hit...', e, type(e), e.args, sep=' | ')
            printException(e)
            print(funcname, ' >> FAILED >> to connect to db, return -1')
            return -1
        finally:
            return 0

    def rollback_database_transaction(self):
        funcname = f'rollback_database_transactio()'
        print('GO _', funcname, '...')
        if not self.valid_reqs(): return -1
        self.db.rollback()
        print('GO _', funcname, 'SUCCESS')
        return 0

    def begin_database_transaction(self):
        funcname = f'begin_database_transaction()'
        print('GO _', funcname, '...')
        if not self.valid_reqs(): return -1
        self.db.begin()
        print('GO _', funcname, 'SUCCESS')
        return 0
        
    def commit_database_transaction(self):
        funcname = f'commit_database_transaction()'
        print('GO _', funcname, '...')
        if not self.valid_reqs(): return -1
        self.db.commit()
        print('GO _', funcname, 'SUCCESS')
        return 0

    def close_database_connection(self):
        funcname = f'close_database_connection()'
        print('GO _', funcname)
        if not self.valid_reqs(): return -1
        self.db.close()
        self.db = self.cur = None
        print(funcname, ' >> CLOSED >> db successfully!')
        return 0
        
    def valid_reqs(self):
        funcname = f'valid_reqs()'
        #print('_ ENTER _', funcname)
        if self.db == None or self.cur == None:
            print(funcname, 'global var db | cur == None; returning False')
            return False
        return True

    # can execute raw statements (select, insert, etc.) or stored proc
    def exe_database_task(self, argsTup, strProc, strOutParam=None, raw_state=False, automate=False):
        debug_print = False
        strProc_p = strProc if debug_print else '<hide_strProc>'
        argsTup_p = argsTup if debug_print else '<hide_argsTup>'
        funcname = f'exe_database_task({argsTup_p}, {strProc_p}, {strOutParam}, raw_state={raw_state}, automate={automate})'
        #print('GO _', funcname)

        #============ open db connection ===============#
        if automate:
            if self.open_database_connection() < 0:
                return -1

        if not self.valid_reqs():
            print('!! ERROR -> self.valid_reqs() == False; return -1')
            return -1
        #============ perform db query ===============#
        procArgs = 'nil'
        rowCnt = 'nil'
        rows = 'nil'
        result = None
        _e = None
        try:
            # ... left of here ... not getting past this next print statement
            if raw_state:
                procArgs = argsTup
                rowCnt = self.cur.execute(strProc)
                rows = self.cur.fetchall()
            else:
                procArgs = self.cur.callproc(f'{strProc}', argsTup)
                rowCnt = self.cur.execute(f"select {strOutParam};") if strOutParam != None else -1
                rows = self.cur.fetchall()
            
            #print(f" >> RESULT 'call {strProc_p}' procArgs: {argsTup_p};")
            #print(f" >> RESULT 'call {strProc_p}' rowCnt: {rowCnt};")
            #print(funcname, f' >> Printing... rows', *rows)
            #getPrintListStr(lst=rows, strListTitle=' >> Printing... rows', useEnumerate=True, goIdxPrint=True, goPrint=True)
            #print(funcname, f' >> Printing... rows[0]:', rows[0])
            
            if strOutParam == None: # stored proc invoked w/o OUT param
                result = rows
            else: # stored proc invoked w/ OUT param
                result = rows[0][strOutParam]
                if isTypeInteger(rows[0][strOutParam]):
                    result = int(rows[0][strOutParam])
        except Exception as e: # ref: https://docs.python.org/2/tutorial/errors.html
            #============ handle db exceptions ===============#
            printException(e)
            print(funcname, '\n',  f"!! Exception hit... procArgs: {procArgs}; returning -1")
            print(f'!! ORIGINAL QUERY: {strProc}\n set result == -1; raising exception...')
            result = -1
            _e = e
        finally:
            #============ close db connection ===============#
            if automate:
                self.commit_database_transaction()
                self.close_database_connection()
            
            # note_020422: check for 'insert' statement above
            if raw_state:
                row_id = self.cur.lastrowid
                return result, row_id
            return result, _e

#===========================================================#
# db_controller support
#===========================================================#
def procValidatePIN(iUserID=-1):
    funcname = f'[{__filename}] procValidatePIN(iUserID(PIN)={iUserID})'
    print('_ ENTER _', funcname)

    iPIN = int(iUserID)
    argsTup = (iPIN, 'p_Result')
    strProc = 'ValidatePIN'
    strOutParam = '@_ValidatePIN_1'
    return exeStoredProcedure(argsTup, strProc, strOutParam)

def isTypeInteger(varCheck=None):
    if varCheck == None:
        return False
    return isinstance(varCheck, int)
    
#====================================================#
#====================================================#

