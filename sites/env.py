__filename = 'env.py'
__fname = 'env'
cStrDividerExcept = '***************************************************************'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

#============================================================================#
## log paths (should use same 'log' folder as access & error logs from nginx config)

GLOBAL_PATH_DEV_LOGS = "../logs/dev.log"
GLOBAL_PATH_ISE_LOGS = "../logs/ise.log"
#============================================================================#
## .env support
import os
from read_env import read_env

try:
    #ref: https://github.com/sloria/read_env
    #ref: https://github.com/sloria/read_env/blob/master/read_env.py
    read_env() # recursively traverses up dir tree looking for '.env' file
except:
    print("#==========================#")
    print(" ERROR: no .env files found ")
    print("#==========================#")

##
# db support (use for remote & local server)
#   use w/ .env
#       DB_HOST=localhost
#       DB_DATABASE=csv_test
#       DB_USERNAME=root
#       DB_PASSWORD=password
##
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_DATABASE']
DB_USER = os.environ['DB_USERNAME']
DB_PW = os.environ['DB_PASSWORD']

#============================================================================#
## mysql return keys

## '/tracks/schedule/get'
#LST_TRACKS_GET_SCHED_RET_KEYS = ['race_id', 'pdf_id', 'race_date', 'race_num', 'track_name', 'track_record', 'owner_id', 'off_at_time', 'start_status', 'fractional_times', 'split_times', 'run_up']
##	select r.id as , r.fk_pdf_id as , r., r.,
##		rt., rt., r.winner_fk_owner_id as ,
##		r., r., r.,
##		r., r.

#============================================================================#


