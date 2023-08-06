import multiprocessing


class test_path:
    output_path = '/opt/HEQMS/convert/output/'
    targetPattern = r"D:\\NCS\\hwp\\"
    # lock_path = 'C:\\Python\\NCS\\log\\lock.txt'
    # log_path = 'C:\\Python\\NCS\\log\\log.txt'


class path:
    output_path = '/opt/HEQMS/convert/'
    targetPattern = r"/opt/test/"
    lock_path = '/opt/HEQMS/convert/log/lock.txt'
    log_path = '/opt/HEQMS/convert/log/log.txt'

class home_path:
    output_path = 'C:\\Python\\NCS\\output\\'
    targetPattern = r"C:\\Python\\NCS_data\\"
    lock_path = 'C:\\Python\\NCS\\log\\lock.txt'
    log_path = 'C:\\Python\\NCS\\log\\log.txt'


class prcs:
    cpu_num = multiprocessing.cpu_count() - 2
