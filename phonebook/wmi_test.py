import wmi
import getpass


# conn = wmi.WMI('dc2')
# for os in conn.Win32_OperatingSystem():  # Win32_Processor
#     print(os)

# user = 'filippov'
# sessions = conn.query('Select * from Win32_LogonSession')
# logons = conn.query('Select * from Win32_LoggedOnUser')
# wql2 = 'Select * from Win32_LogonSession Where LogonType = 2 OR LogonType = 10'

password = getpass.getpass()

print(password)
