import urllib.request
import datetime
import os

# 你的机场订阅基础地址
BASE_URL = "https://node.clashnodes.com/uploads/"

def get_latest_sub():
    today = datetime.datetime.now().strftime("%Y%m%d")
    year_month = datetime.datetime.now().strftime("%Y/%m")
    # 这里修改为从 5 倒序枚举到 0
    for i in range(5, -1, -1):
        file_name = f"{i}-{today}.yaml"
        url = f"{BASE_URL}{year_month}/{file_name}"
        try:
            print(f"尝试下载: {url}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read()
                # 确认内容确实是 Clash 配置
                if b"proxies:" in content or b"mixed-port:" in content:
                    print(f"成功获取最新订阅: {file_name}")
                    with open("latest_backup.yaml", "wb") as f:
                        f.write(content)
                    return True
        except Exception as e:
            print(f"下载失败 {url}: {e}")
            continue
    return False

if __name__ == "__main__":
    if not get_latest_sub():
        print("未找到今天的可用订阅，备用任务结束。")
        exit(1)
