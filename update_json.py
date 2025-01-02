import os
import random
import json
import requests
from datetime import datetime

user_id = "dR2OCZ8AAAAJ"

def update_json():
    ualist = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]
    ua = random.choice(ualist)
    headers = {"Connection": "Keep-alive", "User-Agent": ua}
    url = "http://cse.bth.se/~fer/googlescholar-api/googlescholar.php?user=" + user_id
    try:
        response = requests.get(url, headers)
    except requests.exceptions.RequestException as e:
        print("请求出错：", e)
    # 若请求成功
    if response.status_code == 200:
        html_content = response.text
        # 现在你可以使用html_content来解析HTML内容
        citation_data = json.loads(html_content)

        # 获取当前时间, 并将 datetime 对象转换为字符串
        current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        citation_data['datetime'] = current_time_str

        # 统计值
        i10 = 0
        for paper in citation_data['publications']:
            if int(paper['citations']) >= 10:
                i10 = i10 + 1

        # 根据引用次数对论文进行排序
        sorted_publications = sorted(citation_data['publications'], key=lambda x: int(x['citations']), reverse=True)

        # 初始化h指数
        h_index = 0

        # 遍历排序后的论文列表
        for i, paper in enumerate(sorted_publications):
            if int(paper['citations']) >= h_index + 1:
                h_index += 1
            else:
                break

        citation_data['num_papers'] = len(citation_data['publications'])
        citation_data['h'] = h_index
        citation_data['i10'] = i10

        json_str = json.dumps(citation_data)
        # 获取当前工作目录
        # current_directory = os.getcwd()
        # 获取当前脚本所在目录路径
        current_directory = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_directory, 'assets', 'citation_data.json')
        with open(json_path, 'w') as json_file:
            json_file.write(json_str)
    else:
        print("Failed to retrieve HTML content. Status code:", response.status_code)

if __name__ == '__main__':
    update_json()