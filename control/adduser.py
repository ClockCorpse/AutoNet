import os
import subprocess
import random
import string

# dc: domain controller
# cn: computer name
# ou: organitional unit

# dsadd user "cn=test3,ou=PhongTI,ou=PhongIT, dc=qtm, dc=com" -pwd 1 -profile \\WINSV2019\profile\%username% -hmdir \\WINSV2019\homedir\%username%
# dsmod user "cn=test3,ou=phongTI,ou=phongIT, dc=qtm, dc=com" -pwd 2
# dsrm -noprompt "cn=test3, ou=PhongIT, dc=qtm, dc=com"

# if return code = 0, command executed successfully

def addUser(name,ou,dc,password):
    ou=ou.split('.')
    dc = dc.split('.')
    ouString = ''
    dcString = ''
    serverName = os.getenv('COMPUTERNAME')
    for item in ou:
        ouString = ouString + ',ou='+str(item.strip())
    for item in dc:
        dcString = dcString + ',dc='+str(item.strip())
    com = 'dsadd user "cn=' + str(name) + ouString + dcString + '" -pwd ' + str(password) + f''' -profile \\\\{serverName}\\profile\\{name}''' + f''' -hmdrv z: -hmdir \\\\{serverName}\\Home_folders\\{name}'''
    os.system('mkdir ' + f'''\\\\{serverName}\\Home_folders\\{name}''')
    print(com)
    result = subprocess.run(com)
    os.system(f'''icacls "\\\\{serverName}\\Home_folders\\{name}" /grant {name}:(OI)(CI)F /T''')
    return result.returncode

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def deleteUser(cn,ou,dc):
    ou=ou.split('.')
    dc = dc.split('.')
    ouString = ''
    dcString = ''
    serverName = os.getenv('COMPUTERNAME')
    for item in ou:
        ouString = ouString + ',ou='+str(item.strip())
    for item in dc:
        dcString = dcString + ',dc='+str(item.strip())
    com = 'dsrm -noprompt "cn=' + cn + ouString + dcString + '"'
    os.system(f'rmdir /S /Q \\\\{serverName}\\Home_folders\\{cn}')
    print(com)
    result = subprocess.run(com)
    return result.returncode

def modUser(name,ou,dc,password,enabled):
    disabled = '-disabled no'
    if enabled =='True':
        disabled = ' -disabled no'
    else:
        disabled = ' -disabled yes'
    ou=ou.split('.')
    dc = dc.split('.')
    ouString = ''
    dcString = ''
    for item in ou:
        ouString = ouString + ',ou='+str(item.strip())
    for item in dc:
        dcString = dcString + ',dc='+str(item.strip())
    com = 'dsmod user "cn=' + str(name) + ouString + dcString + '" -pwd ' + str(password) + disabled
    # print(com)
    result = subprocess.run(com)
    return result.returncode

def addOU(ou,dc):
    ous = ou.split('.')
    dcPara = ''
    ouPara = ''
    for item in ous:
        ouPara = ouPara + 'ou='+item+','
    for item in dc.split('.'):
        dcPara = dcPara + 'dc='+item+','
    
    ou = str(ouPara.strip(','))
    dc = str(dcPara.strip(','))
    com = f'dsadd ou ou={ou[3:]},{dc}'
    print(com)
    os.system(com)
    
def getOU():
    result = subprocess.check_output('dsquery ou')
    ous = result.decode('utf-8').split('\n')
    OU = []
    ouList=[]
    del ous[0]
    for line in ous:
        line = line.strip('"').split(',')
        del line[-2:]
        OU.append(line)
        for ou in line:
            ou = ou[3:]
    for item in OU:
        item = '.'.join(item).replace('OU=','')
        ouList.append(item)
    del ouList[-1]
    return ouList

def getDomain():
    result = subprocess.check_output('wmic.exe ComputerSystem get Domain')
    domain = result.decode('utf-8').split('\n')[1]
    return domain

if __name__ == "__main__":
    print(modUser('test3','phongTI,phongIT',2))