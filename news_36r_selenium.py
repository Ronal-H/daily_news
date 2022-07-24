import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sys

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(sys.argv[1])


def req_for_36kr_news():
    # 36氪新闻资讯每日快讯
    # 查询8点1氪用户文章列表
    driver.get("https://36kr.com/user/5652071")
    # 获取第一篇文档dom
    first_new = driver.find_element(
        By.XPATH,
        '//*[@class="author-detail-flow-list "]/div[1]/div/div/div[2]/div[1]/a',
    )
    print("first_new href:" + first_new.get_attribute("href"))
    # 打开第一篇文章
    driver.get(first_new.get_attribute("href"))
    # 提取文件内容
    today_news_html = driver.find_element(
        By.XPATH, '//*[@class="article-mian-content"]/div/div[2]/div'
    )

    content = time.strftime("%Y年%m月%d日", time.localtime()) + "\n"
    for item in today_news_html.find_elements(By.XPATH, "*"):
        if item.tag_name == "h2" and item.text != None:
            content = content + "## " + item.text + "\n"
        elif item.tag_name == "p":
            for strong in item.find_elements(By.TAG_NAME, "strong"):
                if not strong.text.startswith("整理"):
                    content = content + "- " + strong.text + "\n"
    print(content)
    return content


def post_to_qywechat(news_md):
    requests.post(
        "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=***************",
        json={"msgtype": "markdown", "markdown": {"content": news_md},},
    )


def write_file(news_md):
    # 文件写入
    with open("new.md", "w+", encoding="utf-8") as f:
        f.write(news_md)


if __name__ == "__main__":
    news = req_for_36kr_news()
    # post_to_qywechat(news)
    write_file(news)
