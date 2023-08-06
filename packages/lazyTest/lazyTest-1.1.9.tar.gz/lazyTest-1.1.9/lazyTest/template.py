# project  :lazyTest
# -*- coding = UTF-8 -*-
# Author    : buxiubuzhi
# File     :template.py
# time     :2021/3/14  9:42
# Describe : 框架结构模板文件
# ---------------------------------------


# conftest.py文件模板
CONFTEST = """
# -*- coding = UTF-8 -*-
# Author   :
# File     : conftest.py
# time     : 
# Describe :
# ---------------------------------------
import os
import sys
import time
import allure
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from service.LoginService import LoginService
import lazyTest

globals()["driver"] = None


def pytest_addoption(parser):
    # pytest.ini文件自定义参数配置，想要在pytest.ini存放自定义参数，必须再此定义
    parser.addini('Terminal', help='访问浏览器参数')
    parser.addini('URL', help='添加 url 访问地址参数')
    parser.addini('setUp', help='添加 登录时前置输入的参数')
    parser.addini('username', help='添加 登录时用户名参数')
    parser.addini('password', help='添加 登录时密码参数')
    parser.addini('teardown', help='添加 登录时后置输入的参数')
    parser.addini('filepath', help='添加 截图路径')
    parser.addini('logpath', help='添加 日志路径')


@pytest.fixture(scope='session')
def getdriver(pytestconfig):
    '''
    全局的夹具配置，所有用例执行之前，和所有用例执行之后
    :param pytestconfig: 用于获取pytest.ini 中的参数
    :yield: 上面代码为前置，下面代码为后置
    '''
    Terminal = pytestconfig.getini("Terminal")
    URL = pytestconfig.getini("URL")
    driver = lazyTest.browser_Config(Terminal, URL)
    globals()["driver"] = driver.base_driver
    yield driver
    driver.browser_close()


@pytest.fixture(scope='session', autouse=True)
def login(getdriver, pytestconfig):
    '''
    登录业务，再此配置可在运行所有用例时只登录一次
    如果不想使用将：装饰器的autouser改为False即可
    :param getdriver: 获得驱动器
    :param pytestconfig: 从pytest.ini中获得参数
    :return: 
    '''
    lo = LoginService(getdriver)
    username = pytestconfig.getini("username")
    password = pytestconfig.getini("password")
    lo.loginService_1(username, password)


@pytest.fixture(scope="function", autouse=True)
def flush_browser(getdriver):
    '''
    每个用例执行之后刷新页面
    可通过控制装饰器的scope指定影响的级别
    可通过装饰器的autouser决定是否启用
    :param getdriver: 获取驱动器
    :return: 
    '''
    yield
    getdriver.flush_browser()
    getdriver.sleep(1)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    '''
    用例失败截图
    :param item: 每个用例的信息 
    :return: 
    '''
    config = item.config
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call':
        xfail = hasattr(report, 'wasxfail')
        if report.failed and not xfail:
            project = str(config.rootpath)
            filepath = config.getini("filepath")
            picture_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
            filename = project + filepath + picture_time + ".png"
            globals()["driver"].save_screenshot(filename)
            with open(filename, "rb") as f:
                file = f.read()
                allure.attach(file, "失败截图", allure.attachment_type.PNG)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_setup(item):
    '''配置日志输入到文件的位置'''
    config = item.config
    project = str(config.rootpath)
    logpath = config.getini("logpath")
    logging_plugin = config.pluginmanager.get_plugin("logging-plugin")
    logging_plugin.set_log_path(project + logpath)
    yield
"""
# pytest.ini文件模板
PYTEST = """
[pytest]
# 控制台输出日志配置
log_cli = true
log_cli_level = INFO
log_format = %(levelname)s %(asctime)s [%(filename)s:%(lineno)-s] %(message)s
log_date_format = %Y-%M-%D %H:%M:%S
# 文件输出日志控制
log_file_level = INFO
log_file_format = %(levelname)s %(asctime)s [%(filename)s:%(lineno)-s] %(message)s
log_file_date_format = %Y-%M-%D %H:%M:%S
# 自定义参数
#---------------------------------------------------
# 配置浏览器，支持： Chrome、Firefox、Ie、Edge、PhantomJs（无头浏览器）、ChromeOptions（谷歌提供无头）、h5（支持iPhone X）
Terminal = Chrome
# 填写需要访问页面的url，此处不需要指定路由，路由在pages层指定
URL = http://buxiubuzhi:7799
# 截图存放路径，可修改，截图文件名在conftest.py文件中定义
filepath = /result/screenshot/
# 日志存放路径，可修改
logpath = /result/log/log.log
# 自定义登录参数，可根据conftest.py文件中定义的添加，如果需要其他参数，需要先在conftest.py文件中定义
username = 
password = 
"""
# main.py文件模板
MAIN = """
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lazyTest import ClearTestResult


def getPorjectPath():
    '''
    获取项目路径
    '''
    return os.path.dirname(os.path.dirname(__file__))


def clearLogAndReport():
    print("----------清空上次测试结果----------")
    path = getPorjectPath() + "/result"
    ClearTestResult(path)
    time.sleep(2)
    print("----------测试结果清空成功----------")


def runlastFailed():
    print("启动失败用例重跑")
    cmd = "pytest -s --lf {}/case --alluredir {}/result/report".format(getPorjectPath(), getPorjectPath())
    print(os.system(cmd))


def startReport():
    print("-------------启动测试报告--------------")
    cmd = "allure serve {}/result/report".format(getPorjectPath())
    print(os.system(cmd))


def startCase(cases):
    print("------------开始执行测试------------")
    cmd = "pytest -s {}/case/{} --alluredir {}/result/report".format(getPorjectPath(), cases, getPorjectPath())
    print(os.system(cmd))


def run(cases=" "):
    clearLogAndReport()
    startCase(cases)
    s = input("请选择要启用的服务:1:启动失败用例重跑;\t2：启动测试报告;")
    if s == "1":
        runlastFailed()
        s = input("是否启动测试报告:y/n")
    if s == "2" or s == "y":
        startReport()
run()
"""
# 注册用例cases层demo
RegisterCase = """
# -*- coding = UTF-8 -*-
# Author   :
# File     :test_RegisterCase.py
# time     :
# Describe : 注册的测试用例
# ---------------------------------------
import allure
import pytest

import lazyTest
from service.RegisterService import RegisterService


class TestRegister(lazyTest.TestCase):

    @pytest.fixture(scope="function")
    def setUp(self, getdriver, flush_browser):
        self.reg = RegisterService(getdriver)
    
    @allure.title("用户注册")
    def testRegister(self, setUp):
        account = lazyTest.createData("account{}")
        result = self.reg.userRegister(account, account, "123456", "123456", "问题", "答案")
        assert result == "注册成功,快去登录吧！"
"""
# 注册用例service层demo
RegisterService = """
# -*- coding = UTF-8 -*-
# Autohr   :
# File     :RegisterService.py
# time     :
# Describe : 注册流程
# ---------------------------------------
import allure

from pages.RegisterPage import RegisterPage


@allure.feature("注册业务")
class RegisterService:

def __init__(self, driver):
    self.r = RegisterPage(driver)

@allure.story("用户注册")
def userRegister(self, account, username, password, repassword, issue, answer):
    self.r.getRegisterPage()
    self.r.inputAccount(account)
    self.r.inputUsername(username)
    self.r.inputPassword(password)
    self.r.inputRepassword(repassword)
    self.r.inputIssue(issue)
    self.r.inputAnswer(answer)
    self.r.clickSubmit()
    return self.reg.getalertText()
"""
# 注册用例page层demo
RegisterPage = """
# -*- coding = UTF-8 -*-
# Autohr   :
# File     :RegisterPage.py
# time     :
# Describe : 注册页面
# ---------------------------------------
import os

import allure
import lazyTest



class RegisterPage(lazyTest.Page):

def getProjectPath(self) -> str:
    return os.path.dirname(os.path.dirname(__file__))

@lazyTest.Sleep()
@allure.step("进入注册页面")
def getRegisterPage(self):
    self.log.info("进入注册页面")
    self.base_driver.get(self.selector["REGISTER"])

@lazyTest.Sleep()
@allure.step("输入账号:{account}")
def inputAccount(self, account):
    self.log.info("输入账号：%s" % account)
    self.base_driver.element_clear_input(self.selector["ACCOUNT"], account)

@lazyTest.Sleep()
@allure.step("输入用户名:{username}")
def inputUsername(self, username):
    self.log.info("输入用户名：%s" % username)
    self.base_driver.element_clear_input(self.selector["USERNAME"], username)

@lazyTest.Sleep()
@allure.step("输入密码:{password}")
def inputPassword(self, password):
    self.log.info("输入密码：%s" % password)
    self.base_driver.element_clear_input(self.selector["PASSWORD"], password)

@lazyTest.Sleep()
@allure.step("在次输入密码:{repassword}")
def inputRepassword(self, repassword):
    self.log.info("在次输入密码：%s" % repassword)
    self.base_driver.element_clear_input(self.selector["REPASSWORD"], repassword)

@lazyTest.Sleep()
@allure.step("输入安全问题:{issue}")
def inputIssue(self, issue):
    self.log.info("输入安全问题：%s" % issue)
    self.base_driver.element_clear_input(self.selector["ISSUE"], issue)

@lazyTest.Sleep()
@allure.step("输入答案:{answer}")
def inputAnswer(self, answer):
    self.log.info("输入答案：%s" % answer)
    self.base_driver.element_clear_input(self.selector["ANSWER"], answer)

@lazyTest.Sleep()
@allure.step("点击提交")
def clickSubmit(self):
    self.log.info("点击提交")
    self.base_driver.element_click(self.selector["SUBMIT"])

@lazyTest.Sleep()
@allure.step("获取注册后的弹窗文本")
def getalertText(self):
    text = self.base_driver.getAlertText()
    self.log.info("弹窗的文本：%s" % text)
    return text
"""
# 注册用例resources层demo
RegisterPageyaml = """
REGISTER: /view/register.html
ACCOUNT: x,//*[@id="account"]/input
USERNAME: x,/html/body/div/div/div/form/div[2]/input
PASSWORD: x,/html/body/div/div/div/form/div[3]/input
REPASSWORD: x,/html/body/div/div/div/form/div[4]/input
ISSUE: x,/html/body/div/div/div/form/div[5]/input
ANSWER: x,/html/body/div/div/div/form/div[6]/input
SUBMIT: x,/html/body/div/div/div/form/div[7]/button
"""
# 登录Page层
LoginPage = '''
# project  :
# -*- coding = UTF-8 -*-
# Author    : 
# File     :LoginPage.py
# time     :
# Describe : 登录页面
# 如果用例执行过快可通过在每一个步骤添加装饰器：lazyTest.Sleep() 默认在一个步骤执行前后等待1s
# ---------------------------------------
import os
import allure
import lazyTest

class LoginPage(lazyTest.Page):
    """
    page类必须继承lazyTest.page
    """

    def getProjectPath(self) -> str:
        return os.path.dirname(os.path.dirname(__file__))

    @lazyTest.Sleep()
    @allure.step("进入登录页面")
    def getLoginPage(self):
        """进入登录页面"""
        self.base_driver.get(self.selector["GETLOGINPAGE"])
        self.log.info("成功进入登录页面")

    @allure.step("前置输入:{setUp}")
    def inputSetup(self, setUp):
        """前置输入"""
        self.base_driver.element_clear_input(self.selector["INPUTSETUP"], setUp)
        self.log.info("已输入前置")

    @allure.step("输入用户名:{username}")
    def inputUsername(self, username):
        """输入用户名"""
        self.base_driver.element_clear_input(self.selector["INPUTUSERNAME"], username)
        self.log.info("已输入用户名")

    @allure.step("输入密码:{password}")
    def inputPassword(self, password):
        """输入密码"""
        self.base_driver.element_clear_input(self.selector["INPUTPASSWORD"], password)
        self.log.info("已输入密码")

    @allure.step("后置输入:{teardown}")
    def inputTeardown(self, teardown):
        """后置输入"""
        self.base_driver.element_clear_input(self.selector["INPUTTEARDOWN"], teardown)
        self.log.info("已输入后置")

    @allure.step("点击记住我")
    def clickReadme(self):
        """点击记住我"""
        self.base_driver.element_click(self.selector["CLICKREADME"])
        self.log.info("点击记住我")

    @allure.step("点击登录")    # 用于报告中展示
    def clickLogin(self):   
        """点击登录"""          # 用于生成的yaml文件中的注释
        self.base_driver.element_click(self.selector["CLICKLOGIN"])
        self.log.info("点击登录")   # 日志中输出


if __name__ == '__main__':
    LoginPage.writeKey()    # 通过该方法自动创建元素存放的yaml文件,
'''
# 登录的service层
LoginService = '''
# project  :
# -*- coding = UTF-8 -*-
# Author    : 
# File     :LoginService.py
# time     :
# Describe : 登录业务流程
# 可根据登录时不同的业务选择，提供给conftest.py文件使用
# ---------------------------------------
import allure

from pages.LoginPage import LoginPage


@allure.feature("登录业务")
class LoginService:

    def __init__(self, driver):
        self.lo = LoginPage(driver)
        self.lo.getLoginPage()

    @allure.story("简单登录流程")
    def loginService_1(self, username, password):
        self.lo.inputUsername(username)  # 输入用户名
        self.lo.inputPassword(password)  # 输入密码
        self.lo.clickLogin()  # 点击登录

    @allure.story("带记住我的登录流程")
    def loginService_2(self, username, password):
        self.lo.inputUsername(username)  # 输入用户名
        self.lo.inputPassword(password)  # 输入密码
        self.lo.clickReadme()  # 点击记住我
        self.lo.clickLogin()  # 点击登录

    @allure.story("带前置输入的登录流程")
    def loginService_3(self, setup, username, password):
        self.lo.inputSetup(setup)  # 输入前置
        self.lo.inputUsername(username)  # 输入用户名
        self.lo.inputPassword(password)  # 输入密码
        self.lo.clickLogin()  # 点击登录

    @allure.story("带后置输入的登录流程")
    def loginService_4(self, username, password, teardown):
        self.lo.inputUsername(username)  # 输入用户名
        self.lo.inputPassword(password)  # 输入密码
        self.lo.inputTeardown(teardown)  # 输入后置
        self.lo.clickLogin()  # 点击登录

    @allure.story("带前置和后置输入的登录流程")
    def loginService_5(self, setup, username, password, teardown):
        self.lo.inputSetup(setup)  # 输入前置
        self.lo.inputUsername(username)  # 输入用户名
        self.lo.inputPassword(password)  # 输入密码
        self.lo.inputTeardown(teardown)  # 输入后置
        self.lo.clickLogin()  # 点击登录
'''
# 登录的资源文件
LoginPageYaml = """
GETLOGINPAGE: /login  # 进入登录页面
INPUTSETUP: 前置输入
INPUTUSERNAME: x,/html/body/div/form/input[1] # 输入用户名
INPUTPASSWORD: x,/html/body/div/form/input[2] # 输入密码
INPUTTEARDOWN: 后置输入
CLICKREADME: 点击记住我
CLICKLOGIN: x,/html/body/div/form/button  # 点击登录
"""

TEMP = {
    "conftest": CONFTEST,
    "pytest":   PYTEST,
    "main":     MAIN,
    "RegisterCase":RegisterCase,
    "RegisterService":RegisterService,
    "RegisterPage":RegisterPage,
    "RegisterPageyaml":RegisterPageyaml,
    "LoginPage":LoginPage,
    "LoginService":LoginService,
    "LoginPageYaml":LoginPageYaml
}
