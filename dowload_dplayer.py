
import requests
import random
import time
from requests.adapters import HTTPAdapter
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='downloadplayer.log', level=logging.INFO, format=LOG_FORMAT)

def downloader(url, out):
    """
    下载器
    :param url:
    :param out:
    :return:
    """
    headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"}
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=10))
    s.mount('https://', HTTPAdapter(max_retries=10))
    r = s.get(url, headers=headers, timeout=3)
    with open(out, "ab") as f:
        f.write(r.content)


def loop_download(base_url, prefix="", postfix="", amount=1, out="", finish_num=-1):
    """
    主程序
    :param base_url:
    :param prefix:
    :param postfix:
    :param amount:
    :param out:
    :param finish_num:
    :return:
    """
    for num in range(amount+1):
        if num > finish_num: # 用来避免重复下载
            num = str(num).zfill(3) # 补位，比如“001”
            url = prefix+base_url+num+postfix
            # downloader(url, outdir+num+postfix)
            # time.sleep(random.randint(1, 3))
            downloader(url, out+postfix)
            print("{}下载完成，如果中断，请记录完成号码{}方便追加".format(url, num))
            logging.info("{}下载完成，内容追加至 {} , 已完成号码 {} ".format(url, out+postfix, num))


if __name__ == "__main__":
    # downloader("https://www7.feiluzb.com/upload/2019-01-16/599efdfb628cc8e96050de602f66a558/m3u8/abc001.ts", "001.ts")
    # loop_download(base_url="https://www7.feiluzb.com/upload/2019-01-16/599efdfb628cc8e96050de602f66a558/m3u8/abc",
    #               postfix=".ts", amount=123, finish_num=39, out="abc")
    # loop_download(base_url="https://www7.feiluzb.com/upload/2019-01-04/ac9c0864c1822423175e3e7d52e24456/m3u8/abc",
    #               postfix=".ts", amount=34, finish_num=0, out="新娘被操续集露脸这个风俗可以啊")
    # loop_download(base_url="https://www8.tangmu168.com/upload/2018-11-29/8006e94f38e1ee630eeaa815041f8f8e/m3u8/abc",
    #               postfix=".ts", amount=110, finish_num=-1, out="台湾IT男测试夜店把妹帶了个苗條风骚正妹回家啪还无套内射了")
    #
    # dowload_dplayer.loop_download(
    #     base_url="https://www8.tangmu168.com/upload/2018-12-15/b739626007267a3484aa1c11003077c6/m3u8/abc",
    #     postfix=".ts", amount=39, finish_num=-1, out="91苏州猛男震撼新作-床边倒插口交极品白嫩巨乳外教无套爆操无毛嫩逼后入猛操浪叫")
    pass