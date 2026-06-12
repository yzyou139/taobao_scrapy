BOT_NAME = "taobao_scrapy"

SPIDER_MODULES = ["taobao_scrapy.spiders"]
NEWSPIDER_MODULE = "taobao_scrapy.spiders"

# 淘宝 API，不遵守 robots.txt
ROBOTSTXT_OBEY = False

# 请求间隔（秒），避免风控
DOWNLOAD_DELAY = 3

# 并发控制
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# Cookie 启用
COOKIES_ENABLED = True

# 默认请求头
DEFAULT_REQUEST_HEADERS = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'https://s.taobao.com/search?q=',
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 QuarkPC/6.8.7.860',
}

FEED_EXPORT_ENCODING = "utf-8"
# FEEDS 配置在 spider 的 custom_settings 中动态设置（带上关键词）
