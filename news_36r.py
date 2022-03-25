import requests
from lxml import etree
import time


def req_for_36kr_news():
    # 36氪新闻资讯每日快讯
    # 查询8点1氪用户文章列表
    resp = requests.get("https://36kr.com/user/5652071")
    parse_html = etree.HTML(resp.content)
    # 获取第一篇文档dom
    parse_html
    first_new = parse_html.xpath(
        '//*[@class="author-detail-flow-list "]/div[1]/div/div/div[2]/div[1]/a'
    )
    # 打开第一篇文章
    today_news_resp = requests.get("https://36kr.com" + first_new[0].get("href"))
    today_news_html = etree.HTML(today_news_resp.content)
    # 提取文件内容
    today_news_html_list = today_news_html.xpath(
        '//*[@class="article-mian-content"]/div/div[2]/div'
    )
    list = today_news_html_list[0]
    content = time.strftime("%Y年%m月%d日", time.localtime()) + "\n"
    for item in list.iter():
        if item.tag == "h2":
            content = content + "## " + item.text + "\n"
        elif item.tag == "strong":
            content = content + "- " + item.text + "\n"
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
