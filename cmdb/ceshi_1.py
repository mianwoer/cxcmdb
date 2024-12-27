import os
import sys

# from cmdb import views
import django
import paramiko

from mwer_utils import crud
from django.db import connection, transaction, DatabaseError

# 这两行很重要，用来寻找项目根目录，os.path.dirname要写多少个根据要运行的python文件到根目录的层数决定
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cxCMDB.settings')
django.setup()
from cmdb import views


def execute_query(sql, params=None):
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql, params)
            result = cursor.fetchall()
            return result
        except DatabaseError as e:
            print(f"Database error occurred: {e}")
            return None


def get_resource(host, user, passwd, fileSystem='/$', port=22):
    ssh_ = paramiko.SSHClient()
    ssh_.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_.connect(host, port, user, passwd)
        stdin1, cpu, stderr1 = \
            ssh_.exec_command(''' export LANG=en_US.UTF-8;lscpu |egrep '^CPU\(s\)'|awk 'BEGIN{ORS=""} {print $2}' ''')
        stdin2, memory, stderr2 = \
            ssh_.exec_command(''' export LANG=en_US.UTF-8;free -g | grep 'Mem' | awk 'BEGIN{ORS=""} {print $2}' ''')
        stdin3, disk, stderr3 = \
            ssh_.exec_command(
                ''' export LANG=en_US.UTF-8;lsblk -d | awk 'NR > 2,ORS="," {print prev1,prev2}{prev1=$1}{prev2=$4}END{printf"%s %s" ,$1,$4}' ''')
        stdin3, sn, stderr3 = \
            ssh_.exec_command(
                ''' export LANG=en_US.UTF-8;dmidecode -t system | grep Serial| awk -F": " 'BEGIN{ORS=""}{print $2}' ''')
        stdin3, cpu_model, stderr3 = \
            ssh_.exec_command(
                ''' export LANG=en_US.UTF-8;lscpu|grep "Model name"|awk '{ORS=""}{print substr($0, index($0, $3))}' ''')

        resource_dict = {'ip': host,
                         'cpus': str(cpu.read().decode('utf-8')),
                         'memory': str(int(memory.read().decode('utf-8'))) + 'g',
                         'disk': str(disk.read().decode('utf-8')),
                         'sn': str()}
    except Exception as e:
        return {"result": "1",  # 代表失败
                "data": e}
    finally:
        ssh_.close()
    print(resource_dict)
    return {"result": 0,  # 代表成功
            "data": resource_dict}


if __name__ == '__main__':
    _crud = crud.Exsql()
    sql = '''select * from cmdb_host where status = %s'''
    sql1 = ''' update cmdb_host set disk=%s where id=%s '''
    # params = [1]
    result = _crud.update(sql1, 'sda-20G', 1)
    # execute_transactional_update(sql1,'sda 20G', 1)
    print(result)
