import random
import datetime
from filelock import Timeout, FileLock
import shutil

import copy
import os
import glob
import subprocess
import threading
import zlib
from contextlib import closing
from functools import partial

from docopt import docopt
from lxml.etree import XMLSyntaxError

import hwp_convert_code.excute.file_converting.config as cf

from hwp5.hwp5html import HTMLTransform, wrap_for_css, wrap_for_xml, open_dir
from hwp5.proc import rest_to_docopt, version, init_logger
from hwp5.utils import make_open_dest_file
from hwp5.xmlmodel import Hwp5File

from hwp_convert_code.excute.error_manage.hwp_convert_error import RegistryRegistrationError

now = datetime.datetime.now()

'''
* HWP 문서를 Html 문서로 변환하는 프로그램
'''


class HWPConvert(threading.Thread):
    def __init__(self, slash, target_file_name, save_location, replace_extension="html", password=""):
        self.CODEC = "utf-8"
        self.PASSWORD = password
        self.SLASH = slash
        self.TARGET_FILE_NAME = target_file_name
        self.REPLACE_FILE_NAME = target_file_name.split(slash)[-1].split(".hwp")[0] + "." + replace_extension
        self.SAVE_LOCATION = save_location  # if save_location[-1] in ["\\", "/"] else save_location + "/"
        self.EXTENSION = replace_extension
        self.HWP_SECURE_REGISTRY_NAME = "FilePathCheckerModule"

        threading.Thread.__init__(self)

    # 현재 실행중인 프로세스의 정보를 가져옴
    def __get_execute_process_list(self):
        process_dict = {}
        all_process_list = [line.split() for line in
                            subprocess.check_output(["tasklist", "/V"], encoding="cp949").splitlines()]

        for i in all_process_list[3:]:
            process_dict.setdefault(i[0], [])
            in_list = process_dict.get(i[0])

            name_index = 0
            origin_info = copy.deepcopy(i)
            for j_index, j in enumerate(reversed(origin_info)):
                if j.find(":") != -1:
                    name_index = len(origin_info) - j_index
                    break

            process_name = " ".join(i[name_index:])

            for j in origin_info[name_index:]:
                del i[name_index]
            i.append(process_name)

            in_list.append(i)

        return process_dict

    def __get_process_name(self):
        filename = self.TARGET_FILE_NAME.split("/")[-1]
        file_location = self.TARGET_FILE_NAME.replace(filename, "").replace("/", "\\")
        return f"{filename} [{file_location}] - 한글"

    def hwp_to_html(self):
        log_path = cf.path.log_path

        __doc__ = '''HWPv5 to HTML converter

        Usage::

            hwp5html [options] <hwp5file>
            hwp5html [options] <hwp5file> --html
            hwp5html [options] <hwp5file> --css
            hwp5html -h | --help
            hwp5html --version

        Options::

            -h --help           Show this screen
            --version           Show version
            --loglevel=<level>  Set log level.
            --logfile=<file>    Set log file.

            --output=<output>   Output file / directory'''

        doc = rest_to_docopt(__doc__)
        args = docopt(doc, argv=[self.TARGET_FILE_NAME], version=version)
        init_logger(args)

        hwp5path = args['<hwp5file>']

        html_transform = HTMLTransform()

        open_dest = make_open_dest_file(args['--output'])
        if args['--css']:
            transform = html_transform.transform_hwp5_to_css
            open_dest = wrap_for_css(open_dest)

        elif args['--html']:
            transform = html_transform.transform_hwp5_to_xhtml
            open_dest = wrap_for_xml(open_dest)

        else:
            transform = html_transform.transform_hwp5_to_dir
            dest_path = self.SAVE_LOCATION + self.REPLACE_FILE_NAME

            if not (os.path.isdir(dest_path)):
                os.makedirs(os.path.join(dest_path))

            if not dest_path:
                dest_path = os.path.splitext(os.path.basename(hwp5path))[0]
            open_dest = partial(open_dir, dest_path)

        with closing(Hwp5File(hwp5path)) as hwp5file:
            with open_dest() as dest:
                try:
                    transform(hwp5file, dest)
                except XMLSyntaxError as syntax_error:
                    print(syntax_error)
                    log = open(log_path + 'log.txt', 'a')
                    log.write('SYNTAX_ERROR!:' + str(dest_path) + '\n')
                    log.close()
                    pass

    def run(self):
        self.hwp_to_html()


def path_list(o_path, iswin):
    if iswin == 'test':
        slash = '\\'
    elif iswin == 'linux':
        slash = '/'
    elif iswin == 'home':
        slash = '\\'
    else:
        print('os 입력이 잘못되었습니다.')

    first_path = os.listdir(o_path)

    second_path = []

    for i in range(len(first_path)):
        path_temp = str(o_path + first_path[i] + slash)
        second_path.append(path_temp)

        third_path = []
        for pth in second_path:
            if len(os.listdir(pth)) > 1:
                path_temp = sorted(os.listdir(pth))
                third_path.append(pth + path_temp[-1] + slash + '한글' + slash + '*.hwp')
            elif len(os.listdir(pth)) == 1:
                path_temp = sorted(os.listdir(pth))
                third_path.append(pth + path_temp[0] + slash + '한글' + slash + '*.hwp')
            else:
                continue

    final_path = []
    for i in range(len(third_path)):
        final_path_tmp = sorted(glob.glob(third_path[i]))
        final_path.extend(final_path_tmp)

    return final_path, slash


def run_list(i_process, path):
    # 경로 지정
    if path == 'test':
        test_path = cf.test_path
        input_path = test_path.targetPattern
        print('input_path : ' + input_path)
        output_path = test_path.output_path
        print('output_path : ' + output_path)
        log_path = test_path.log_path  # todo 로그 경로 추가
        lock_path = test_path.lock_path

    elif path == 'linux':
        linux_path = cf.path
        input_path = linux_path.targetPattern
        print('input_path : ' + input_path)
        output_path = linux_path.output_path
        print('output_path : ' + output_path)
        log_path = linux_path.log_path  # todo 로그 경로 추가
        lock_path = linux_path.lock_path

    elif path == 'home':
        home_path = cf.home_path
        input_path = home_path.targetPattern
        # print('input_path : ' + input_path)
        output_path = home_path.output_path
        # print('output_path : ' + output_path)
        log_path = home_path.log_path

    else:
        print('run_list : path error')

    result, slsh = path_list(input_path, path)
    # print('total hwp : ' + str(len(result)))


    if not (os.path.isdir(log_path)):
        try:
            os.makedirs(os.path.join(log_path))
        except FileExistsError:
            print('create log.txt error')

    # log.txt에 발견한 hwp 갯수 생성
    with open(log_path + 'log.txt', 'a') as log:
        log.write('total hwp : ' + str(len(result)) + '\n')
        log.write(now.strftime('%Y-%m-%d %H:%M:%S') + '\n')

    # 해당 경로에 존재하는 모든 hwp파일을 불러와 html 변환
    # for res in result:
    for i in range(len(result)):
        css_path = output_path + result[i].split(slsh)[-1].split('.hwp')[0] + '.html' + slsh + 'styles.css'
        bin_path = output_path + result[i].split(slsh)[-1].split('.hwp')[0] + '.html' + slsh + 'bindata'

        if os.path.isfile(css_path):
            try:
                os.remove(css_path)
            except FileNotFoundError as ff:
                print(ff)
                pass

        if os.path.isdir(bin_path):
            try:
                shutil.rmtree(bin_path)
            except FileNotFoundError as ff:
                print(ff)
                pass

        message = '#### prcs_id : ' + str(i_process) + ' #### ' + result[i]
        # txt_path = result[i].split(".hwp")[0] + '.txt'
        txt_path = output_path + 'txt' + slsh + result[i].split(slsh)[-1].split('.hwp')[0] + '.txt'
        output_txt_path = output_path + 'txt' + slsh

        if not (os.path.isdir(output_txt_path)):
            try:
                os.makedirs(os.path.join(output_txt_path))
            except FileExistsError:
                print('')
                pass

        if os.path.isfile(txt_path):
            continue

        elif not os.path.isfile(txt_path):
            # print(str(i_process) + '@@ ' + txt_path, flush=True)
            if not (os.path.isdir(lock_path)):
                try:
                    os.makedirs(os.path.join(lock_path))
                except FileExistsError:
                    pass


            lock_file_path = lock_path + result[i].split(slsh)[-1].split('.hwp')[0] + '.lock'
            lock = FileLock(lock_file_path)

            with lock:
                if os.path.isfile(txt_path):
                    continue
                f = open(txt_path, 'w')
                f.close()

                print(message + '\n', flush=True)

                try:
                    html_path = output_path + result[i].split(slsh)[-1].split('.hwp')[0] + '.html'
                    if os.path.isdir(html_path):
                        continue
                    else:
                        hwp_convert = HWPConvert(slash=slsh,
                                                 target_file_name=result[i],
                                                 save_location=output_path,
                                                 replace_extension="html")
                        hwp_convert.run()

                except zlib.error as e:
                    print(e)

                except XMLSyntaxError as syntax_error:
                    print(syntax_error)
                    log = open(log_path + 'log.txt', 'a')
                    log.write('SYNTAX_ERROR2!:' + str(html_path) + '\n')
                    log.write(str(syntax_error) + '\n')
                    log.close()
                    continue

                try:
                    log = open(log_path + 'log.txt', 'a')
                    log.write(message + '\n')
                finally:
                    log.close()

                # time.sleep(0.1)

            # todo .html 폴더 내부 css파일 bin 폴더 등 필요없는 것 삭제

            css_path = output_path + result[i].split(slsh)[-1].split('.hwp')[0] + '.html' + slsh + 'styles.css'
            bin_path = output_path + result[i].split(slsh)[-1].split('.hwp')[0] + '.html' + slsh + 'bindata'

            try:
                os.remove(css_path)
            except FileNotFoundError as ff:
                print(ff)
                pass

            try:
                shutil.rmtree(bin_path)
                lock_file_path = lock_path + result[i].split(slsh)[-1].split('.hwp')[0] + '.lock'
                os.remove(lock_file_path)

            except FileNotFoundError as ff:
                print(ff)
                pass

    # for root, dirs, files in os.walk(output_path):
    #     rootpath = os.path.join(os.path.abspath(output_path), root)
    #
    #     for file in files:
    #         filepath = os.path.join(rootpath, file)
    #         res.append(filepath)
    #
    #     for result in res:
    #         print(result)
    #         file_name = result.split("/")[-1]
    #         file_path = os.path.join()


def test_path(i_process, path):
    if path == 'test':
        test_path = cf.test_path
        input_path = test_path.targetPattern
        print('input_path : ' + input_path)
        output_path = test_path.output_path
        print('output_path : ' + output_path)
        # log_path = test_path.log_path #todo 로그 경로 추가
        # lock_path = cf.home_path.lock_path

    elif path == 'linux':
        linux_path = cf.path
        input_path = linux_path.targetPattern
        print('input_path : ' + input_path)
        output_path = linux_path.output_path
        print('output_path : ' + output_path)
        # log_path = linux_path.log_path #todo 로그 경로 추가
        # lock_path = cf.home_path.lock_path

    elif path == 'home':
        home_path = cf.home_path
        input_path = home_path.targetPattern
        # print('input_path : ' + input_path)
        output_path = home_path.output_path
        # print('output_path : ' + output_path)
        log_path = home_path.log_path

    else:
        print('test_path : path error')

    result, slsh = path_list(input_path, path)
    print('total hwp : ' + str(len(result)))

    with open(log_path, 'a') as log:
        log.write('total hwp : ' + str(len(result)) + '\n')

    for i in range(len(result)):
        txt_path = result[i].split(".hwp")[0] + '.txt'

        if os.path.isfile(txt_path):
            continue

        elif not os.path.isfile(txt_path):
            # print(str(i_process) + '@@ ' + txt_path, flush=True)
            # lock = FileLock(lock_path)

            with lock:
                print(str(i_process) + '<- ' + result[i], flush=True)
                if os.path.isfile(txt_path):
                    continue

                f = open(txt_path, 'w')
                f.close()

                message = '#### prcs_id : ' + str(i_process) + ' #### ' + result[i]

                try:
                    log = open(log_path, 'a')
                    log.write(message + '\n')
                finally:
                    log.close()

                # time.sleep(0.1)


def rm_txt(path):
    if path == 'test':
        test_path = cf.test_path
        input_path = test_path.targetPattern
        print('input_path : ' + input_path)
        output_path = test_path.output_path
        print('output_path : ' + output_path)
        # log_path = test_path.log_path #todo 로그 경로 추가
        lock_path = cf.home_path.lock_path

    elif path == 'linux':
        linux_path = cf.path
        input_path = linux_path.targetPattern
        print('input_path : ' + input_path)
        output_path = linux_path.output_path
        print('output_path : ' + output_path)
        # log_path = linux_path.log_path #todo 로그 경로 추가
        lock_path = cf.home_path.lock_path

    elif path == 'home':
        home_path = cf.home_path
        input_path = home_path.targetPattern
        # print('input_path : ' + input_path)
        output_path = home_path.output_path
        # print('output_path : ' + output_path)
        log_path = home_path.log_path

    else:
        print('rm_txt : path error')

    result, slsh = path_list(input_path, path)
    # 임시 텍스트함수 제거
    for i in range(len(result)):
        txt_path = output_path + 'txt' + slsh + result[i].split(slsh)[-1].split('.hwp')[0] + '.txt'
        # css_path = output_path + result[i].split(slsh)[-1].split('.hwp')[0] + '.html' + slsh + 'styles.css'
        # bin_path = output_path + result[i].split(slsh)[-1].split('.hwp')[0] + '.html' + slsh + 'bindata'

        if os.path.isfile(txt_path):
            os.remove(txt_path)
        # os.remove(css_path)
        # os.rmdir(bin_path)

    print('block 텍스트파일 제거완료')
