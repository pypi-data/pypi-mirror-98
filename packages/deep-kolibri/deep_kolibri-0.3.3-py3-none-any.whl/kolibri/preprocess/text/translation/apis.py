
import re
import sys
import time
import json
import random
from functools import wraps
from typing import Union, Callable
from kolibri.preprocess.text.translation.constants import GOOGLE_DEFAULT_SERVICE_URLS
from urllib.parse import quote, urlencode, urlparse
from kolibri.logger import get_logger
from kolibri.preprocess.text.translation.models import Detected, Translated
from kolibri.preprocess.text.translation import utils
logger = get_logger(__name__)
import requests
import execjs
from lxml import etree



class TranslatorBase:

    @staticmethod
    def time_stat(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            t1 = time.time()
            r = func(*args, **kwargs)
            t2 = time.time()

            return r
        return wrapper

    @staticmethod
    def get_headers(host_url, if_use_api=False, if_use_referer=True, if_ajax=True):
        url_path = urlparse(host_url).path
        host_headers = {
            'Referer' if if_use_referer else 'Host': host_url,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/55.0.2883.87 Safari/537.36"
        }
        api_headers = {
            'Origin': host_url.split(url_path)[0] if url_path else host_url,
            'Referer': host_url,
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/55.0.2883.87 Safari/537.36"
        }
        if not if_ajax:
            api_headers.pop('X-Requested-With')
            api_headers.update({'Content-Type': 'text/plain'})
        return host_headers if not if_use_api else api_headers

    @staticmethod
    def check_language(from_language, to_language, language_map, output_zh=None, output_auto='auto'):
        from_language = output_auto if from_language in ('auto', 'auto-detect') else from_language
        from_language = output_zh if output_zh and from_language in ('zh','zh-CN','zh-CHS','zh-Hans') else from_language
        to_language = output_zh if output_zh and to_language in ('zh','zh-CN','zh-CHS','zh-Hans') else to_language
        
        if from_language != output_auto and from_language not in language_map:
            raise TranslatorError('Unsupported from_language[{}] in {}.'.format(from_language,sorted(language_map.keys())))
        elif to_language not in language_map:
            raise TranslatorError('Unsupported to_language[{}] in {}.'.format(to_language,sorted(language_map.keys())))
        elif from_language != output_auto and to_language not in language_map[from_language]:
            logger.exception('language_map:', language_map)
            raise TranslatorError('Unsupported translation: from [{0}] to [{1}]!'.format(from_language,to_language))
        return from_language,to_language


class TranslatorSeverRegion:
    @property
    def request_server_region_info(self):
        try:
            ip_address = requests.get('http://httpbin.org/ip').json()['origin']
            try:
                data = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=10).json()
                sys.stderr.write(f'Using {data.get("country")} server backend.\n')
                return data
            except requests.exceptions.Timeout:
                data = requests.post(
                    url='http://ip.taobao.com/outGetIpInfo',
                    data={'ip': ip_address, 'accessKey': 'alibaba-inc'}
                ).json().get('data')
                data.update({'countryCode': data.get('country_id')})
                return data

        except requests.exceptions.ConnectionError:
            raise TranslatorError('Unable to connect the Internet.\n')
        except:
            raise TranslatorError('Unable to find server backend.\n')


class TranslatorError(Exception):
    pass


class Google(TranslatorBase):
    def __init__(self, host_url=None):
        super().__init__()
        if host_url is  None:
            host_url= random.choice(GOOGLE_DEFAULT_SERVICE_URLS)


        self.host_url = 'https://{}'.format(host_url)
        self.api_url = 'https://{}/_/TranslateWebserverUi/data/batchexecute'.format(host_url)
        self.request_server_region_info = REQUEST_SERVER_REGION_INFO
        self.host_headers = None
        self.api_headers = None
        self.language_map = None
        self.rpcid = 'MkEWBc'
        self.query_count = 0
        self.output_zh = 'zh-CN'

    def get_rpc(self, query_text, from_language, to_language):
        param = json.dumps([[str(query_text).strip(), from_language, to_language, True], [1]])
        rpc = json.dumps([[[self.rpcid, param, None, "generic"]]])
        return {'f.req': rpc}

    def get_language_map(self, host_html):
        et = etree.HTML(host_html)
        lang_list = sorted(list(set(et.xpath('//*[@class="ordo2"]/@data-language-code'))))
        return {}.fromkeys(lang_list, lang_list)

    def get_info(self, host_html):
        data_str = re.findall(r'window.WIZ_global_data = (.*?);</script>', host_html)[0]
        data = execjs.get().eval(data_str)
        return {'bl': data['cfb2h'], 'f.sid': data['FdrFJe']}

    # @Tse.time_stat
    def _google_api(self, query_text: str, from_language: str = 'auto', to_language: str = 'en', **kwargs) -> Union[str, list]:
        """
        https://translate.google.com, https://translate.google.cn.
        :param query_text: str, must.
        :param from_language: str, default 'auto'.
        :param to_language: str, default 'en'.
        :param **kwargs:
                :param if_use_cn_host: boolean, default None.
                :param is_detail_result: boolean, default False.
                :param proxies: dict, default None.
                :param sleep_seconds: float, >0.05. Best to set it yourself, otherwise there will be surprises.
        :return: str or list
        """

        self.host_headers = self.get_headers(self.host_url, if_use_api=False)
        self.api_headers = self.get_headers(self.host_url, if_use_api=True, if_use_referer=True, if_ajax=True)
        proxies = kwargs.get('proxies', None)

        with requests.Session() as ss:

            host_html = ss.get(self.host_url, headers=self.host_headers, proxies=proxies).text
            if not self.language_map:
                self.language_map = self.get_language_map(host_html)
            from_language, to_language = self.check_language(from_language, to_language, self.language_map, output_zh=self.output_zh)

            rpc_data = self.get_rpc(query_text, from_language, to_language)
            r = ss.post(self.api_url, headers=self.api_headers, data=urlencode(rpc_data), proxies=proxies)
            r.raise_for_status()

            return r


    def google_api(self, query_text: str, from_language: str = 'auto', to_language: str = 'en', **kwargs) -> Union[str, list]:

        r=self._google_api(query_text, from_language, to_language, **kwargs)

        json_data = json.loads(r.text[6:])
        data = json.loads(json_data[0][2])
        is_detail_result = kwargs.get('is_detail_result', False)
        sleep_seconds = kwargs.get('sleep_seconds', 0.05 + random.random() / 2 + 1e-100 * 2 ** self.query_count)

        time.sleep(sleep_seconds)
        self.query_count += 1

        translated =''.join([x[0] for x in data[1][0][0][5]])

        # put final values into a new Translated object
        result = Translated(src=from_language, dest=to_language, origin=query_text,
                            text=translated, pronunciation=translated)

        return result

    def detect(self, text, **kwargs):
        """Detect language of the input text

        """
        if isinstance(text, list):
            result = []
            for item in text:
                lang = self.detect(item)
                result.append(lang)
            return result

        data = self._google_api(text, 'auto', 'en')

        data = utils.format_json(data.text[6:])
        data = json.loads(data[0][2])
        # actual source language that will be recognized by Google Translator when the
        # src passed is equal to auto.
        try:
            src = data[2]
            confidence = -1

        except Exception:  # pragma: nocover
            pass

        result = Detected(lang=src, confidence=confidence)

        return result

class Bing(TranslatorBase):
    def __init__(self):
        super().__init__()
        self.host_url = None
        self.host_url = 'https://www.bing.com/Translator'
        self.request_server_region_info = REQUEST_SERVER_REGION_INFO
        self.api_url = None
        self.host_headers = None
        self.api_headers = None
        self.host_info = None
        self.language_map = None
        self.query_count = 0
        self.output_auto = 'auto-detect'
        self.output_zh = 'zh-Hans'
    
    def get_host_info(self, host_html):
        et = etree.HTML(host_html)
        lang_list = et.xpath('//*[@id="tta_srcsl"]/option/@value') or et.xpath('//*[@id="t_srcAllLang"]/option/@value')
        lang_list = list(set(lang_list))
        lang_list.remove(self.output_auto)
        language_map = {}.fromkeys(lang_list,lang_list)
        iid = et.xpath('//*[@id="rich_tta"]/@data-iid')[0] + '.' + str(self.query_count + 1)
        ig = re.findall('IG:"(.*?)"', host_html)[0]
        return {'iid': iid, 'ig': ig, 'language_map': language_map}

    # @Tse.time_stat
    def bing_api(self, query_text:str, from_language:str='auto', to_language:str='en', **kwargs) -> Union[str,list]:
        """
        http://bing.com/Translator, http://cn.bing.com/Translator.
        :param query_text: str, must.
        :param from_language: str, default 'auto'.
        :param to_language: str, default 'en'.
        :param **kwargs:
                :param if_use_cn_host: boolean, default None.
                :param is_detail_result: boolean, default False.
                :param proxies: dict, default None.
                :param sleep_seconds: float, >0.05. Best to set it yourself, otherwise there will be surprises.
        :return: str or list
        """
        self.api_url = self.host_url.replace('Translator', 'ttranslatev3')
        self.host_headers = self.get_headers(self.host_url, if_use_api=False)
        self.api_headers = self.get_headers(self.host_url, if_use_api=True)
        is_detail_result = kwargs.get('is_detail_result', False)
        proxies = kwargs.get('proxies', None)
        sleep_seconds = kwargs.get('sleep_seconds', 0.05 + random.random()/2 + 1e-100*2**self.query_count)
    
        with requests.Session() as ss:
            host_html = ss.get(self.host_url, headers=self.host_headers, proxies=proxies).text
            self.host_info = self.get_host_info(host_html)

            if not self.language_map:
                self.language_map = self.host_info.get('language_map')
            from_language, to_language = self.check_language(from_language, to_language, self.language_map,
                                                             output_zh=self.output_zh,output_auto=self.output_auto)
            # params = {'isVertical': '1', '': '', 'IG': self.host_info['ig'], 'IID': self.host_info['iid']}
            self.api_url = self.api_url + '?isVertical=1&&IG={}&IID={}'.format(self.host_info['ig'],self.host_info['iid'])
            form_data = {'text': str(query_text).strip(), 'fromLang': from_language, 'to': to_language}
            r = ss.post(self.api_url, headers=self.host_headers, data=form_data, proxies=proxies)
            r.raise_for_status()
            data = r.json()
        time.sleep(sleep_seconds)
        self.query_count += 1
        return data if is_detail_result else data[0]['translations'][0]['text']



REQUEST_SERVER_REGION_INFO = TranslatorSeverRegion().request_server_region_info

_bing = Bing()
_google = Google()


def translate(text, dest, src='auto', service='google', **kwargs):

    translate_txt=None

    if service=='auto':
        service=random.choice(['bing', 'google'])
    if service=="bing":
        translate_txt = _bing.bing_api
    else:
        translate_txt = _google.google_api

    return translate_txt(query_text=text, from_language=src, to_language=dest, **kwargs)


def detect_language(text):
    return _google.detect(text)
