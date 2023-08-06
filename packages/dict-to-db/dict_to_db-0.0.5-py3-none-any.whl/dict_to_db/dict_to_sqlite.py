import os
import re
import sys
import time
import json
import datetime
import traceback

import httpx
from openpyxl import Workbook
from dict_to_db.dict_to_db import DictToDb
from selenium.webdriver import Chrome, ChromeOptions
from tenacity import retry, wait_random, stop_after_attempt
from selenium.webdriver.support.wait import WebDriverWait

# from a_common.dict_to_db import DictToDb

from a_common.logger import log
from a_common.check_status import check_run

base_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
session = httpx.Client(http2=True, verify=False)
db = DictToDb("Qing.DB")
table = "cui_data"
driver: Chrome
config: dict
cookies: str
token: str
headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://coms.qingchunbank.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; ) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/85.0.4153.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}
post_all_page_data = {"page": 1, "limit": 200, }
post_user_Info_data = {"caseId": "20180216012093", "custId": "B296FF0B-2169-E711-B88B-6C92BF446C53",
                       "history": "N"}  # TODO history是个隐患
post_phone_info_data = {"page": 1, "limit": 10, "caseId": "20160820095696",
                        "custId": "B9B1F424-9016-E611-9B49-008CFAE40F9C", "history": "N"}
post_query_action_data = {"page": 1, "limit": 10, "caseId": "20180904015710",
                          "custId": "DD7E6004-01D8-E711-9B51-70106FAFFB3C", "history": "N"}
post_all_page_url = "https://coms.qingchunbank.com/telcollection/queue/pageQuery.do?TOKEN_ID={token}"
post_user_info_url = "https://coms.qingchunbank.com/comprehensive/manage/queryCust.do?TOKEN_ID={token}"
post_phone_info_url = "https://coms.qingchunbank.com/comprehensive/manage/queryTelephone.do?TOKEN_ID={token}"
post_query_action_url = "https://coms.qingchunbank.com/comprehensive/manage/queryAccount.do?TOKEN_ID={token}"


def init_driver():
    try:
        global driver
        options = ChromeOptions()
        prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)  #
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 可以取消Chrome自动化测试提醒
        chrome_path = os.path.join(base_dir, 'lib/chrome.exe')
        options.binary_location = chrome_path
        options.add_argument('--no-sandbox')
        options.add_argument("window-size=1888,998")
        options.add_argument("app=https://127.0.0.1")
        driver = Chrome(executable_path=os.path.join(base_dir, "lib/dr85.exe"), options=options)
        log.info(f"浏览器引擎初始化成功")
    except:
        log.error(traceback.format_exc())


def read_config():
    try:
        global config
        with open(os.path.join(base_dir, 'qingchunbank_config.json'), 'r', encoding='utf8') as f:
            config = json.load(f)
    except:
        log.error(traceback.format_exc())


def wait_user_login():
    global cookies, token
    log.info(f"等待用户登录中")
    driver.get("https://coms.qingchunbank.com/")
    username_el = WebDriverWait(driver, 40).until(lambda x: x.find_element_by_id("userName"))
    username_el.clear()
    username_el.send_keys(config.get("username"))
    password_el = driver.find_element_by_id("passWord")
    password_el.clear()
    password_el.send_keys(config.get("password"))
    WebDriverWait(driver, 300).until(lambda x: x.find_element_by_id("fsTopMenu"))
    time.sleep(2.6)
    log.info(f"登录成功")
    cookies = "; ".join([f"{i['name']}={i['value']}" for i in driver.get_cookies()])
    token = "".join(re.findall(r'TOKEN_ID=(.*)$', driver.current_url))


def get_all_page_data():
    total_count = 1
    for i in range(1, 5000):
        try:
            if i == 1:
                total_count = get_page_list_data(i)
            elif (total_count // 200 + 1) < i:
                log.info(f"当前账号：{config.get('username')} 所有页面都抓取完毕！")
                break
            else:
                get_page_list_data(i)
        except:
            log.error(traceback.format_exc())


def request_url(url, data, header, fun_name):
    response = session.post(url, json=data, headers=header)
    response.raise_for_status()
    result = response.json()
    code = result.get("code")
    if code != 0:
        if 'msg' in result.keys():
            log.info(f"{fun_name} 请求失败：{result.get('msg')}")
        else:
            log.info(f"请求失败：{result.get('msg')}")
        raise Exception(f"{fun_name} code error")
    return result


@retry(reraise=True, wait=wait_random(min=1.5, max=3), stop=stop_after_attempt(3))
def get_page_list_data(page, ):
    log.info(f"查询列表页：{page}")
    url = post_all_page_url.format(token=token)
    post_all_page_data['page'] = page
    result = request_url(url, post_all_page_data, headers, 'get_page_list_data')
    count = result.get("count")
    data_list = result.get("data")
    for data in data_list:
        try:
            user = data['custName']
            case_id = data['caseId']
            cust_id = data['custId']
            select_data = None
            try:
                select_data = db.execute(f"select * from {table} where [案件号]=:案件号;", {"案件号": case_id}).fetchall()
            except:
                pass
            if select_data:
                log.info(f"查询过用户：{user} 的数据不重新查询！   {case_id}")
                continue
            time.sleep(5)
            save_data = {"客户姓名": user, "案件号@text#pk": case_id, "催收员": config.get("username")}
            user_info_data = get_user_info(case_id, cust_id, user)
            phone_info_data = get_phone_info(case_id, cust_id, user)
            action_info_data = get_query_action_info(case_id, cust_id, user)
            save_data.update(user_info_data)
            save_data.update(phone_info_data)
            save_data.update(action_info_data)
            db.insert(save_data, table_name=table, export=True)
            log.info(f"保存：{save_data}")
        except:
            log.error(traceback.format_exc())
    return count


@retry(reraise=True, wait=wait_random(min=1.5, max=3), stop=stop_after_attempt(3))
def get_user_info(case_id, cust_id, user):
    log.info(f"复制用户 {user} 的客户主要信息")
    url = post_user_info_url.format(token=token)
    post_user_Info_data['caseId'] = case_id
    post_user_Info_data['custId'] = cust_id
    result = request_url(url, post_user_Info_data, headers, 'get_user_info')
    data = result.get("data")
    result_data = dict()
    result_data['性别'] = data.get("gender")
    result_data['逾期天数'] = data.get("overdueDays")
    result_data['到期退案'] = data.get("expireDate")
    return result_data


@retry(reraise=True, wait=wait_random(min=1.5, max=3), stop=stop_after_attempt(3))
def get_phone_info(case_id, cust_id, user):
    log.info(f"复制用户 {user} 的手机号信息")
    url = post_phone_info_url.format(token=token)
    post_phone_info_data['caseId'] = case_id
    post_phone_info_data['custId'] = cust_id
    result = request_url(url, post_phone_info_data, headers, 'get_phone_info')
    data = result.get("data")
    result_data = {
        "电话姓名": [], "电话类型": [], "电话关系": [], "电话号码": [],
    }
    for d in data:
        try:
            result_data['电话姓名'].append(d.get('name', ''))
            result_data['电话类型'].append(d.get('telTypeName', ''))
            result_data['电话关系'].append(d.get('relationName', ''))
            result_data['电话号码'].append(d.get('telephone', ''))
        except:
            log.error(traceback.format_exc())
    return result_data


@retry(reraise=True, wait=wait_random(min=1.5, max=3), stop=stop_after_attempt(3))
def get_query_action_info(case_id, cust_id, user):
    log.info(f"复制用户 {user} 的账户详细信息")
    url = post_query_action_url.format(token=token)
    post_query_action_data['caseId'] = case_id
    post_query_action_data['custId'] = cust_id
    result = request_url(url, post_query_action_data, headers, 'get_query_action_info')
    data = result.get("data")
    result_data = {
        "账号": [], "贷款日期": [], "借款金额": [], "商品名称": [], "账户姓名": [], "开户行名称": [], "银行卡号": [], "产品大类": [],
        "门店名称": [], "商户名称": [], "门店地址省(市)": [], "门店地址市(区)": [], "门店地址区(县)": [], "还款期限": [],
        "申请状态": [], "逾期本金": [], "逾期利息": [], "逾期服务费": [], "服务费": [], "逾期金额": [], "当前逾期期数": [],
        "每月还款额": [], "账户类型": [],
    }
    for d in data:
        try:
            result_data['账号'].append(d.get("appId", ""))
            result_data['贷款日期'].append(d.get("openDate", ""))
            result_data['借款金额'].append(d.get("loanAmt", ""))
            result_data['商品名称'].append(d.get("product", ""))
            result_data['账户姓名'].append(d.get("acctName", ""))
            result_data['开户行名称'].append(d.get("bank", ""))
            result_data['银行卡号'].append(d.get("mainCardNum", ""))
            result_data['产品大类'].append(d.get("bigProductName", ""))
            result_data['门店名称'].append(d.get("storeName", ""))
            result_data['商户名称'].append(d.get("merchantName", ""))
            result_data['门店地址省(市)'].append(d.get("province", ""))
            result_data['门店地址市(区)'].append(d.get("city", ""))
            result_data['门店地址区(县)'].append(d.get("county", ""))
            result_data['还款期限'].append(d.get("installNum", ""))
            result_data['申请状态'].append(d.get("appStatusName", ""))
            result_data['逾期本金'].append(d.get("principalAmt", ""))
            result_data['逾期利息'].append(d.get("intrestAmt", ""))
            result_data['逾期服务费'].append(d.get("overdueServiceFee", ""))
            result_data['服务费'].append(d.get("serviceFee", ""))
            result_data['逾期金额'].append(d.get("overdueAmt", ""))
            result_data['当前逾期期数'].append(d.get("overdueNum", ""))
            result_data['每月还款额'].append(d.get("billAmt", ""))
            result_data['账户类型'].append(d.get("overdueNumName", ""))
        except:
            log.error(traceback.format_exc())
    return result_data


def export():
    def get_phone_value(index, _data):
        try:
            return _data[index]
        except:
            return ''

    log.info(f"正在导出数据中...")
    all_data = db.execute(f"select * from {table} where export=0;").fetchall()
    if not all_data:
        log.info(f"当前没有可以导出的数据！")
        return
    wb = Workbook(write_only=True)
    ws = wb.create_sheet("数据")
    ws.freeze_panes = "A2"
    ws.append(["客户姓名", "性别", "案件号", "逾期天数", "到期退案", "电话姓名", "电话类型", "电话关系", "电话号码", "电话姓名1", "电话类型1",
               "电话关系1", "电话号码1", "电话姓名2", "电话类型2", "关系2", "电话号码2", "催收员", "帐号", "贷款日期", "借款金额", "商品名称",
               "账户姓名", "开户行名称", "银行卡号", "产品大类", "门店名称", "商户名称", "门店地址省(市)",
               "门店地址市(区)", "门店地址区(县)", "还款期限", "申请状态", "逾期本金", "逾期利息", "逾期服务费",
               "服务费", "逾期金额", "当前逾期期数", "每月还款额", "账户类型"])
    success = []
    for data in all_data:
        try:
            for i in range(len(data['账号'])):
                save_data = list()
                save_data.append(data['客户姓名'])
                save_data.append(data['性别'])
                save_data.append(data['案件号'])
                save_data.append(data['逾期天数'])
                save_data.append(data['到期退案'])
                for _ in range(3):
                    save_data.append(get_phone_value(_, data['电话姓名']))
                    save_data.append(get_phone_value(_, data['电话类型']))
                    save_data.append(get_phone_value(_, data['电话关系']))
                    save_data.append(get_phone_value(_, data['电话号码']))
                save_data.append(data['催收员'])
                save_data.append(data['账号'][i])
                save_data.append(data['贷款日期'][i])
                save_data.append(data['借款金额'][i])
                save_data.append(data['商品名称'][i])
                save_data.append(data['账户姓名'][i])
                save_data.append(data['开户行名称'][i])
                save_data.append(data['银行卡号'][i])
                save_data.append(data['产品大类'][i])
                save_data.append(data['门店名称'][i])
                save_data.append(data['商户名称'][i])
                save_data.append(data['门店地址省(市)'][i])
                save_data.append(data['门店地址市(区)'][i])
                save_data.append(data['门店地址区(县)'][i])
                save_data.append(data['还款期限'][i])
                save_data.append(data['申请状态'][i])
                save_data.append(data['逾期本金'][i])
                save_data.append(data['逾期利息'][i])
                save_data.append(data['逾期服务费'][i])
                save_data.append(data['服务费'][i])
                save_data.append(data['逾期金额'][i])
                save_data.append(data['当前逾期期数'][i])
                save_data.append(data['每月还款额'][i])
                save_data.append(data['账户类型'][i])
                ws.append(save_data)
            success.append({"案件号": data['案件号']})
        except:
            log.error(traceback.format_exc())
    wb.save(f"导出_{datetime.datetime.now().strftime('%Y年%m月%d日_%H时%M分%S秒')}.xlsx")
    for s in success:
        try:
            db.update({"export": 1}, where=s, table_name=table, commit=True)
        except:
            log.error(traceback.format_exc())


def main():
    check_run(check_time=datetime.datetime(year=2021, month=12, day=19, hour=23))
    read_config()
    init_driver()
    wait_user_login()
    get_all_page_data()
    log.info(f"程序抓取完成，接下来将自动导出数据！（注：也可以人工手动导出数据！）")
    export()


if __name__ == '__main__':
    y = input("本程序仅用于内部员工提高工作效率使用，严禁传播，后果自负，我已知晓:  y/n")
    if y.strip().lower() != "y":
        log.info(f"error")
        time.sleep(3)
        sys.exit()
    r_input = input('请输入程序运行模式\n输入1 程序从系统复制数据到本地数据库\n输入2 程序把保存到本地数据库的数据导出到Excel中\n')
    if r_input.strip() == '1':
        main()
    elif r_input.strip() == '2':
        export()
    else:
        print(f"输入错误")
        time.sleep(3)
