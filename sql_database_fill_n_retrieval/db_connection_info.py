# just a place to store db credentials
# Connect to the MySQL instance
db_host = 'localhost'
db_user = 'sec_user'

db_name = 'securities_master'

WIN_OR_MAC = -1

# I use a Windows and Mac machine. db creds are different
# ----
import sys
import os

# these items differn base don the operating system.
op_platform = sys.platform
op_sys_keys = list(os.environ.keys())

# In Windows or MacOS the patforom (for me) will be one of the following.
mac_by_sys = "darwin"
win_by_sys = "win32"

# In Windows or MacOS, the sys.keys() will contain one of the following
mac_by_os = "TERM_PROGRAM"
win_by_os = "WINDIR"

if mac_by_sys == op_platform: WIN_OR_MAC = "MAC"
if win_by_sys == op_platform: WIN_OR_MAC = "WIN"

if mac_by_os in op_sys_keys: WIN_OR_MAC = "MAC"
if win_by_os in op_sys_keys: WIN_OR_MAC = "WIN"

which_pass = {"MAC":'password', "WIN":'secpassword'}

db_pass = which_pass.get(WIN_OR_MAC)
