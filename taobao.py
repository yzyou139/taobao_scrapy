import json
import hashlib
import time
import urllib.parse
import scrapy
from ..items import TaobaoScrapyItem

# ==================== 配置 ====================
KEYWORD = "手柄"
MAX_PAGES = 5
APP_KEY = '12574478'

# ==================== Cookie ====================
COOKIES = {
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
    '_m_h5_tk': '580633a791d556ac7320ddb4a54a300f_1781235211911',
    '_m_h5_tk_enc': 'df2f23ce6fb093ed06542cb8cade92a9',
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

TOKEN = COOKIES['_m_h5_tk'].split('_')[0]
API = 'https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/'


class TaobaoSpider(scrapy.Spider):
    name = "taobao"

    # 输出文件名带上关键词，方便区分
    custom_settings = {
        'FEEDS': {
            f'搜索_{KEYWORD}_{MAX_PAGES}页.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'indent': 2,
            }
        }
    }

    def start_requests(self):
        """生成所有页面的请求（每页独立生成 sign）"""
        for page in range(1, MAX_PAGES + 1):
            url = self._build_url(page)
            self.logger.info(f'生成第 {page} 页请求')
            yield scrapy.Request(
                url=url,
                cookies=COOKIES,
                meta={'page': page},
                callback=self.parse,
                dont_filter=True,
            )

    def parse(self, response):
        """解析 JSONP 响应，提取商品数据"""
        page = response.meta['page']
        resp = self._parse_jsonp(response.text)
        ret = resp.get('ret', [])
        self.logger.info(f'第 {page} 页 ret: {ret}')

        if not any('SUCCESS' in str(r) for r in ret):
            self.logger.error(f'第 {page} 页请求失败: {ret}')
            return

        data = resp.get('data', {})
        items = data.get('itemsArray', [])
        self.logger.info(f'第 {page} 页商品数: {len(items)}')

        for item_data in items:
            parsed = self._parse_item(item_data)
            # 跳过空数据（广告位、推荐卡片等无商品信息条目）
            if parsed['item_id'] or parsed['title']:
                yield parsed

    # ========== 辅助方法 ==========

    @staticmethod
    def _build_data(page: int) -> str:
        """构造请求 data 参数（双层 JSON，紧凑格式）"""
        params_inner = json.dumps({
            "device": "HMA-AL00", "isBeta": "false", "grayHair": "false",
            "from": "nt_history", "brand": "HUAWEI", "info": "wifi",
            "index": "4", "rainbow": "", "schemaType": "auction",
            "elderHome": "false", "isEnterSrpSearch": "true", "newSearch": "false",
            "network": "wifi", "subtype": "", "hasPreposeFilter": "false",
            "prepositionVersion": "v2", "client_os": "Android", "gpsEnabled": "false",
            "searchDoorFrom": "srp", "debug_rerankNewOpenCard": "false",
            "homePageVersion": "v7", "searchElderHomeOpen": "false",
            "search_action": "initiative", "sugg": "_4_1", "sversion": "13.6",
            "style": "list", "ttid": "600000@taobao_pc_10.7.0", "needTabs": "true",
            "areaCode": "CN", "vm": "nw", "countryNum": "156", "m": "pc",
            "page": page, "n": 50, "q": KEYWORD,
        }, separators=(',', ':'))
        return json.dumps({"appId": "34385", "params": params_inner}, separators=(',', ':'))

    @staticmethod
    def _build_params(page: int) -> dict:
        """构造请求参数（含 sign 签名）"""
        t = str(int(time.time() * 1000))
        data = TaobaoSpider._build_data(page)
        raw = TOKEN + '&' + t + '&' + APP_KEY + '&' + data
        sign = hashlib.md5(raw.encode()).hexdigest()
        return {
            'jsv': '2.7.4', 'appKey': APP_KEY, 't': t, 'sign': sign,
            'api': 'mtop.relationrecommend.wirelessrecommend.recommend', 'v': '2.0',
            'timeout': '10000', 'type': 'jsonp', 'dataType': 'jsonp',
            'callback': f'mtopjsonp{page + 100}', 'data': data,
        }

    @staticmethod
    def _build_url(page: int) -> str:
        """构造完整 URL（API + 查询参数）"""
        params = TaobaoSpider._build_params(page)
        query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        return API + '?' + query

    @staticmethod
    def _parse_jsonp(text: str) -> dict:
        """解析 JSONP 响应：提取 {...} 部分"""
        text = text.strip()
        if text.startswith('mtopjsonp'):
            json_str = text[text.index('{'):text.rindex('}') + 1]
            return json.loads(json_str)
        return json.loads(text)

    @staticmethod
    def _parse_item(item: dict) -> TaobaoScrapyItem:
        """解析单条商品为 Scrapy Item"""
        item_data = item.get('item', item)
        scrapy_item = TaobaoScrapyItem()
        scrapy_item['shop_name'] = item_data.get('nick', '')
        scrapy_item['title'] = item_data.get('title', '').replace('<span class=H>', '').replace('</span>', '')
        scrapy_item['price'] = item_data.get('priceShow', {}).get('price', '') or item_data.get('price', '')
        scrapy_item['sales'] = item_data.get('realSales', '')
        scrapy_item['shop_location'] = item_data.get('procity', '')
        scrapy_item['item_id'] = item_data.get('item_id', '')
        scrapy_item['shop_url'] = (
            f"https://shop{item_data.get('shopId', '')}.taobao.com"
            if item_data.get('shopId') else
            f"https://store.taobao.com/shop/view_shop.htm?user_number_id={item_data.get('userId', '')}"
            if item_data.get('userId') else ''
        )
        scrapy_item['item_url'] = item_data.get('auctionURL', '').strip('` ')
        return scrapy_item
