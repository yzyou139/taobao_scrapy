import requests
import hashlib
import json
import time
import random
import urllib.parse

# ==================== 配置 ====================
KEYWORD = "月子水"
MAX_PAGES = 5
PAGE_SIZE = 50
REQUEST_INTERVAL = random.uniform(3, 5)

# ==================== Cookie ====================
cookies = {
    'cookie2': '1c3a7b1ed0641720e092f41ee6723dc6',
    't': 'c47dac2677fb49f2f8f289046dc55a03',
    '_tb_token_': 'eb5b908bb5f15',
    'thw': 'cn',
    'cna': 'pOWnItduBBUCAbdFjbGWsjg1',
    '3PcFlag': '1780545461953',
    'wk_cookie2': '12e30fa7d5c2630e8ea0fe2e1d38f71d',
    'wk_unb': 'UUpgRK%2FTNtpRJXkv2w%3D%3D',
    '_hvn_lgc_': '0',
    'lgc': 'tb930519158',
    'cancelledSubSites': 'empty',
    'dnk': 'tb930519158',
    'tracknick': 'tb930519158',
    'sn': '',
    'aui': '2212201318745',
    'mtop_partitioned_detect': '1',
    '_m_h5_tk': 'b3c7681658b96ec1dcc88deb9da8bc07_1781149906548',
    '_m_h5_tk_enc': 'edbfd2bfd005c765a3336412d8ec55aa',
    'xlly_s': '1',
    'sca': '8d7de7b1',
    '_samesite_flag_': 'true',
    'unb': '2212201318745',
    'csg': 'a9e2b227',
    'cookie17': 'UUpgRK%2FTNtpRJXkv2w%3D%3D',
    'skt': '4a241f490ca6eb9a',
    'existShop': 'MTc4MTA1NTYxNw%3D%3D',
    '_cc_': 'UtASsssmfA%3D%3D',
    '_l_g_': 'Ug%3D%3D',
    'sg': '85f',
    '_nk_': 'tb930519158',
    'cookie1': 'UUGrdwHm286RNNK3TxEI9lPW5u%2FBtIi5owQF4CR2dGU%3D',
    'sgcookie': 'E100kjgcDrTi4fKl10BDxs9ww%2BA5T%2BDWPEQl%2F6zIwWzOcI8K9E9xlP7P%2BdGQGViz9qv3rCDObqiHL1VkaNmwpQAgqTougi0qAKN54m7dVnn5prY%3D',
    'uc1': 'cookie21=VFC%2FuZ9ainBZ&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&cookie14=UoYWPA6J5ynVMw%3D%3D&existShop=false&pas=0&cookie15=UIHiLt3xD8xYTw%3D%3D',
    'uc3': 'nk2=F5RMGoRHM3O%2BgKs%3D&id2=UUpgRK%2FTNtpRJXkv2w%3D%3D&vt3=F8dD1NM37w%2FO8PnyhEg%3D&lg2=URm48syIIVrSKA%3D%3D',
    'uc4': 'id4=0%40U2gqy16dm15mcLj0tDdJ1fTYAnE4mOlv&nk4=0%40FY4HX7Z4uJWrPa%2BO8UAJL%2B%2F8kDmhHw%3D%3D',
    'tfstk': 'hMY-_x2zewvsRwhmXZ_I837npfcmS8FdOCRQrW_5P9tv_pBoT07kD9pXHTaoa0SCpL7KIAjgVdzR56y7PJjCGts7gj0mSVAya7fSsItHRN2fs14CRg1WGs6V9JN5Opsbl6WbP6a5O-GATt6CRMsIlr1Fw6w7P_GvGt5CR99CVjQf36_Cdp_CrZSSZlSvyFlby0Wi7k4QRUgF2vO_xzUkk_dYGQBAt6XN2-02MQD87IbPkdCMEqaJBC82Hs9sJxQe3H9C9KgwYQLnGkiebhOMjPiByATJWHK4Fy8ExnYWoGySycTJ3M9XA74x-FtDaNdaE2HrxCTwBI0zJf8esdv1X7kqScvAfGYL3YkZa01qV69XJkF9XDfAIb3LYkSqgsBiMjEUYg1VMOc-ekrF0j5..',
    'isg': 'BHl567ywN0AWEevc_MEeR-xmiOVThm048mxA4ZuojaKqIpO049fpCeM0pCbUmgVw',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://s.taobao.com/search?q=' + urllib.parse.quote(KEYWORD),
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 QuarkPC/6.8.7.860',
}

API = 'https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/'
APP_KEY = '12574478'
TOKEN = cookies['_m_h5_tk'].split('_')[0]


def build_data(page: int) -> str:
    params_inner = json.dumps({
        "device": "HMA-AL00",
        "isBeta": "false",
        "grayHair": "false",
        "from": "nt_history",
        "brand": "HUAWEI",
        "info": "wifi",
        "index": "4",
        "rainbow": "",
        "schemaType": "auction",
        "elderHome": "false",
        "isEnterSrpSearch": "true",
        "newSearch": "false",
        "network": "wifi",
        "subtype": "",
        "hasPreposeFilter": "false",
        "prepositionVersion": "v2",
        "client_os": "Android",
        "gpsEnabled": "false",
        "searchDoorFrom": "srp",
        "debug_rerankNewOpenCard": "false",
        "homePageVersion": "v7",
        "searchElderHomeOpen": "false",
        "search_action": "initiative",
        "sugg": "_4_1",
        "sversion": "13.6",
        "style": "list",
        "ttid": "600000@taobao_pc_10.7.0",
        "needTabs": "true",
        "areaCode": "CN",
        "vm": "nw",
        "countryNum": "156",
        "m": "pc",
        "page": page,
        "n": PAGE_SIZE,
        "q": KEYWORD,
    }, separators=(',', ':'))

    outer = json.dumps({
        "appId": "34385",
        "params": params_inner
    }, separators=(',', ':'))

    return outer


def build_params(page: int) -> dict:
    t = str(int(time.time() * 1000))
    data = build_data(page)
    raw = TOKEN + '&' + t + '&' + APP_KEY + '&' + data
    sign = hashlib.md5(raw.encode()).hexdigest()

    return {
        'jsv': '2.7.4',
        'appKey': APP_KEY,
        't': t,
        'sign': sign,
        'api': 'mtop.relationrecommend.wirelessrecommend.recommend',
        'v': '2.0',
        'timeout': '10000',
        'type': 'jsonp',
        'dataType': 'jsonp',
        'callback': f'mtopjsonp{page + 100}',
        'data': data,
    }


def parse_jsonp(text: str) -> dict:
    text = text.strip()
    if text.startswith('mtopjsonp'):
        json_str = text[text.index('{'):text.rindex('}')+1]
        return json.loads(json_str)
    return json.loads(text)


def fetch_page(page: int):
    params = build_params(page)
    resp = requests.get(API, params=params, cookies=cookies, headers=headers)
    return parse_jsonp(resp.text)


def parse_item(item: dict) -> dict:
    """解析单条商品信息"""
    item_data = item.get('item', item)

    # 店铺信息
    shop_info = item_data.get('shopInfo', {}) or {}

    return {
        'shop_name': item_data.get('nick', ''),
        'title': item_data.get('title', '').replace('<span class=H>', '').replace('</span>', ''),
        'price': item_data.get('priceShow', {}).get('price', '') or item_data.get('price', ''),
        'sales': item_data.get('realSales', ''),
        'shop_location': item_data.get('procity', ''),
        'item_id': item_data.get('item_id', ''),
        'shop_url': f"https://shop{item_data.get('shopId', '')}.taobao.com" if item_data.get('shopId') else
                    f"https://store.taobao.com/shop/view_shop.htm?user_number_id={item_data.get('userId', '')}" if item_data.get('userId') else '',
        'item_url': item_data.get('auctionURL', '').strip('` '),  # 原始推广链接，去掉首尾反引号和空格
    }


def get_all_items(data: dict) -> list:
    """从响应 data 中提取商品列表"""
    # 尝试多种字段路径
    for key in ['itemsArray', 'resultList', 'itemList', 'items']:
        items = data.get(key, [])
        if items:
            return items
    return []


# ==================== 主程序 ====================
if __name__ == '__main__':
    all_items = []

    for page in range(1, MAX_PAGES + 1):
        print(f"\n请求第 {page} 页...")
        resp = fetch_page(page)
        ret = resp.get('ret', [])
        print(f"  ret: {ret}")

        if not any('SUCCESS' in str(r) for r in ret):
            print(f"  ❌ 请求失败")
            break

        data = resp.get('data', {})
        items = get_all_items(data)

        print(f"  商品数: {len(items)}")

        for item in items:
            parsed = parse_item(item)
            all_items.append(parsed)
            # 打印前 3 条看看
            if len(all_items) <= 3:
                print(f"    → {parsed['title'][:40]} | {parsed['price']} | {parsed['shop_name']}")

        time.sleep(REQUEST_INTERVAL)

    print(f"\n{'='*50}")
    print(f"共获取 {len(all_items)} 条商品")

    # 打印前 5 条完整信息
    print(f"\n前 5 条商品:")
    for i, item in enumerate(all_items[:5], 1):
        print(f"\n  [{i}] {item['title'][:60]}")
        print(f"      店铺: {item['shop_name']}")
        print(f"      价格: ¥{item['price']}")
        print(f"      销量: {item['sales']}")
        print(f"      所在地: {item['shop_location']}")
        print(f"      商品链接(前200): {item['item_url'][:200]}")

    # 保存到文件
    filename = f'搜索_{KEYWORD}_{MAX_PAGES}页.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 已保存 {len(all_items)} 条数据到 {filename}")
