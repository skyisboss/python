import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

"""
python 对进程采集猫眼电影TOP100排行
python 版本：3.x
"""

# getPage 下载网站
# url - 网页地址
# headers - headers头信息
def getPage(url):
	try:
		headers = {'content-type': 'text/html; charset=utf-8',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
		res = requests.get(url ,headers = headers)
		if res.status_code ==200:
			return res.text
	except ReferenceError:
		return None

#　parsePage分析网页
#　html - 未经处理的html页码
def parsePage(html):
	# 使用正则匹配页面元素
	patten = re.compile('<dd>.*?board-index.*?">(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
	items = re.findall(patten,html)
	# 转换成键值对字段
	for item in items:
		yield {
			'index' : item[0],
			'image' : item[1],
			'titme' : item[2],
			'actor' : item[3].strip()[3:],
			'title' : item[4].strip()[5:],
			'score' : item[5] + item[6]
		}

#  writeToFile 写入文件
#  content - 内容
def writeToFile(content):
	# encoding='utf-8' ， ensure_ascii=False 保存不转义中文
	with open('resule.txt','a',encoding='utf-8') as f:
		f.write(json.dumps(content,ensure_ascii=False) + '\n')
		f.close()

# 处理程序
# pages - 页码
def main(pages):
	url = 'http://maoyan.com/board/4?offset=' + str(pages)
	print('正在处理' + str(pages) + '页')
	html = getPage(url)	
	for item in parsePage(html):
		writeToFile(item)
	print('			[ok]')

if __name__ == '__main__':
	for i in range(10):
		main(i*10)
	#pool = Pool()
	#pool.map(main , [i*10 for i in range(10)])
