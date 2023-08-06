from multiprocessing import Process
import warnings
import time

import hwp_convert_code.excute.file_converting.config as cf
import hwp_convert_code.excute.file_converting.hwp_to_html_convert as hth

# 경고문구 제거
warnings.filterwarnings(action='ignore')

i_cpu = cf.prcs.cpu_num
# print('core num : ' + str(i_cpu + 2))

# 멀티 쓰레딩 Process 사용
procs = []

# 시작시간
start_time = time.time()

if __name__ == '__main__':
    for i_process in range(i_cpu):
        # Process 객체 생성
        # proc = Process(target=hth.test_path, args=(i_process, 'test'))
        # proc = Process(target=hth.test_path, args=(i_process, 'home')) #todo 제거하기
        proc = Process(target=hth.run_list, args=(i_process, 'linux'))  # todo 제거하기
        procs.append(proc)
        proc.start()

    # 프로세스 종료 대기
    for proc in procs:
        proc.join()

    # hth.rm_txt('test')
    hth.rm_txt('linux') #todo 제거하기

# 종료시간
print("--- %s seconds ---" % (time.time() - start_time))