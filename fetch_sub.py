import urllib.request
import re
import datetime
import os

# 你的机场订阅基础地址
BASE_URL = "https://node.clashnodes.com/uploads/"

def get_latest_sub():
    today = datetime.datetime.now().strftime("%Y%m%d")
    year_month = datetime.datetime.now().strftime("%Y/%m")
    # 根据你提供的链接规律，推测格式可能是 0-20260912.yaml, 1-20260912.yaml 等
    # 这里遍历 0 到 5，尝试寻找今天的最新文件
    for i in range(5):
        file_name = f"{i}-{today}.yaml"
        url = f"{BASE_URL}{year_month}/{file_name}"
        try:
            print(f"尝试下载: {url}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read()
                # 检查下载的内容是不是有效的 YAML 配置（含有 proxies 或 mixed-port 字样）
                if b"proxies:" in content or b"mixed-port:" in content:
                    print(f"成功获取最新订阅: {file_name}")
                    with open("latest.yaml", "wb") as f:
                        f.write(content)
                    return True
        except Exception as e:
            print(f"下载失败 {url}: {e}")
            continue
    return False

if __name__ == "__main__":
    if not get_latest_sub():
        print("未找到今天的可用订阅，请检查链接格式是否需要调整。")
        exit(1)
