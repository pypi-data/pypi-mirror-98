# -*- coding = UTF-8 -*-
# Author   :buxiubuzhi
# File     : cli.py
# project  : UIAutoProject
# time     : 2020/12/14 16:39
# Describe : 
# ---------------------------------------

import argparse
import os, sys
from lazyTest import __version__, __description__

PY3 = sys.version_info[0] == 3


def main():
    """
    API test: parse command line options and run commands.
    """

    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        '-v', '--version', dest='version', action='store_true',
        help="show version")

    parser.add_argument(
        '--project',
        help="Create an lazyTest automation test project.")

    parser.add_argument(
        '-r',
        help="run test case")

    args = parser.parse_args()

    # 获取版本
    if args.version:
        print("version {}".format(__version__))
        return 0

    # 创建项目
    project_name = args.project
    if project_name:
        create_scaffold(project_name)
        return 0

    # 运行用例
    run_file = args.r
    if run_file:
        if PY3:
            ret = os.system("python -V")
            if ret != 0:
                os.system("python3 -V")
                command = "python3 " + run_file
            else:
                command = "python " + run_file
        else:
            raise NameError("Does not support python2")
        os.system(command)
        return 0


from lazyTest.template import TEMP


def create_scaffold(project_name):
    """
    create scaffold with specified project name.
    """
    if os.path.isdir(project_name):
        print("{}:Not a directory".format(project_name))
        return

    def create_folder(path):
        print("create dir:{}".format(path))
        os.makedirs(path)

    def create_file(path, file_content=""):
        print("create file:{}".format(path))
        with open(path, 'w', encoding='utf-8') as f:
            f.write(file_content)

    create_folder(project_name)  # 创建项目目录
    # 创建目录结构
    create_folder(os.path.join(project_name, "pages"))
    create_folder(os.path.join(project_name, "service"))
    create_folder(os.path.join(project_name, "case"))
    create_folder(os.path.join(project_name, "main"))
    create_folder(os.path.join(project_name, "result"))
    create_folder(os.path.join(project_name, "result", "log"))
    create_folder(os.path.join(project_name, "result", "report"))
    create_folder(os.path.join(project_name, "result", "screenshot"))
    create_folder(os.path.join(project_name, "resources"))
    create_folder(os.path.join(project_name, "resources", "element"))
    # 创建核心文件
    create_file(os.path.join(project_name, "__init__.py"))
    create_file(os.path.join(project_name, "case", "conftest.py"), TEMP["conftest"])
    create_file(os.path.join(project_name, "pytest.ini"), TEMP["pytest"])
    create_file(os.path.join(project_name, "main", "main.py"), TEMP["main"])
    # 创建demo文件
    create_file(os.path.join(project_name, "case", "test_RegisterCase.py"), TEMP["RegisterCase"])
    create_file(os.path.join(project_name, "service", "RegisterService.py"), TEMP["RegisterService"])
    create_file(os.path.join(project_name, "service", "LoginService.py"), TEMP["LoginService"])
    create_file(os.path.join(project_name, "pages", "RegisterPage.py"), TEMP["RegisterPage"])
    create_file(os.path.join(project_name, "pages", "LoginPage.py"), TEMP["LoginPage"])
    create_file(os.path.join(project_name, "resources", "element", "RegisterPage.yaml"), TEMP["RegisterPageyaml"])
    create_file(os.path.join(project_name, "resources", "element", "LoginPage.yaml"), TEMP["LoginPageYaml"])


if __name__ == '__main__':
    main()
