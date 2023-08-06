import multiprocessing


class test_path:
    output_path = '/opt/HEQMS/convert/output/'
    targetPattern = r"D:\\NCS\\hwp\\"
    # lock_path = 'C:\\Python\\NCS\\log\\lock.txt'
    # log_path = 'C:\\Python\\NCS\\log\\log.txt'


class path:
    output_path = '/opt/test/output/'
    targetPattern = r"/opt/test/"
    lock_path = '/opt/HEQMS/lock/'
    log_path = '/opt/test/output/log/'

class home_path:
    output_path = 'C:\\Python\\NCS\\output\\'
    targetPattern = r"C:\\Python\\NCS_data\\"
    lock_path = 'C:\\Python\\NCS\\log\\lock.txt'
    log_path = 'C:\\Python\\NCS\\log\\log.txt'

class other_server:
    output_path = '/data/NCS/LM/output/'
    targetPattern = r"/data/NCS/LM/"
    lock_path = '/usr/local/python/PythonProject/hthconverter/lock/'
    log_path = '/data/NCS/LM/output/log/'



class prcs:
    cpu_num = multiprocessing.cpu_count()
