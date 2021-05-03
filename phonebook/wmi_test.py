import wmi
import re


conn = wmi.WMI('dc2')
# for os in conn.Win32_OperatingSystem():  # Win32_Processor
#     print(os)

user = 'filippov'
sessions = conn.query('Select * from Win32_LogonSession')
logons = conn.query('Select * from Win32_LoggedOnUser')
# wql2 = 'Select * from Win32_LogonSession Where LogonType = 2 OR LogonType = 10'

for logon in logons:
    result = re.search(user, logon.antecedent)
    if result is not None:
        logon_id = logon.dependent.split('"')[1]
        for session in sessions:
            result2 = re.search(logon_id, session.logonid)
            if result2 is not None:
                print(result2)

# for disk in conn.Win32_LogicalDisk(DriveType=3):
#     print(disk)

# print(conn.Win32_ComputerSystem.methods.keys())
