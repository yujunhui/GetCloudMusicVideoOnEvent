import requests
import csv
from selenium import webdriver

from encrypt_api import encrypt_data

#############################################
# BEGIN 一些url和http请求头的设置
header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'music.163.com',
    'Referer': 'http://music.163.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
}

event_url = 'http://music.163.com/#/user/event?id=343142613'
enent_mv_api_url = 'http://music.163.com/weapi/cloudvideo/playurl'

# END 一些url和http请求头的设置
#############################################

driver = webdriver.PhantomJS(executable_path=r'E:\Study\phantomjs-2.1.1-windows\bin\phantomjs.exe')
driver.get(event_url)
# 滚动到页底
js = "document.getElementById('g_iframe').contentWindow.scrollTo(0,9999999)"
driver.execute_script(js)
driver.get_screenshot_as_file('test_screenshot.png')
driver.switch_to.frame('g_iframe')
event_mv_list = [{'details': i.text, 'id': i.get_attribute('data-vid')}
                 for i in driver.find_elements_by_css_selector('div.info.f-pa') if i is not None]
# event_mv_list[0]
# {'name': '【耳机体验】3DC音效《BINGBIAN病变》秋仁 - by 自由者音效\n47149\n04:10', 'id': '5B0AF067CBB42F7789F7B97E13827565'}

print('共有%d个视频' % len(event_mv_list))
if len(event_mv_list):
    event_mv_list_ids = [i['id'] for i in event_mv_list]
    data = {
        'ids': str(event_mv_list_ids),
        "resolution": "1080",
        "csrf_token": ""
    }
    data = encrypt_data(data)
    sess = requests.session()
    resp = sess.post(enent_mv_api_url, data=data, headers=header)

    if resp.status_code == 200:
        with open('mv_urls.txt', 'w') as f:
            for each in resp.json()['urls']:
                f.write(each['url']+'\n')
        with open('resp_json.txt', 'w') as f:
                f.write(resp.text)
        with open('mv_info.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, ['name','like','time','id','url','size','validityTime','r'])
            writer.writeheader()
            csv_dict_data = resp.json()['urls']
            for i, each in enumerate(csv_dict_data):
                each['name'], each['like'], each['time'] = event_mv_list[i]['details'].split('\n')
                writer.writerow(each)
