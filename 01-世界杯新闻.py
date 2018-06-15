#coding:utf-8
import requests
from bs4 import BeautifulSoup
import pymysql

"""
1.查看我们想要抓取的页面，打开F12开发者工具，发现网页源代码中含有链接，直接构造请求获取网页源代码。
2.通过分析我们想要的内容所在的位置，选择使用beautifulsoup来获取数据.
3.使用mysql存储数据，构建mysql表结构，同时使用pymysql来和数据库进行交互
"""
headers = {
	"User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
}


def get_html(url):
	try:
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			html = response.text
			return html
		else:
			print(response.status_code)
			return None
	except Exception as e:
		print(e)
		return None

def parse_html(html):
	# 创建一个字典来存储每一组信息
	infos = {}
	# 构建BeautifulSoup对象
	soup = BeautifulSoup(html, 'lxml')
	# 通过css选择器来获取在class为yaowen下的所有a标签，返回一个list
	news = soup.select("div.yaowen a[href^='http://2018.qq.com/a/']")
	for new in news:
		# 使用get()方法获取属性，get_text()方法获取文本
		infos[new.get("href")] = new.get_text()
	# 返回存储了所有信息的字典
	return infos

def save_to_mysql(infos):
	# 创建connect对象
	conn = pymysql.connect(host="localhost", user="root", passwd="mysql", db="spider", port=3306, charset="utf8")
	# 创建cursor对象
	cursor = conn.cursor()
	# 循环遍历每一组数据存入数据库
	for href,title in infos.items():
		# 构造一个列表形式的参数
		params = [title, href]
		# sql语句
		sql = "insert into world_cup(title, href) values(%s, %s)"
		try:
			# 使用cursor.execute()执行语句
			cursor.execute(sql, params)
			# 使用conn.commit()提交事务
			conn.commit()
			print("插入数据成功")
		except Exception as e:
			print(e)
	cursor.close()
	conn.close()

def main():
	url = "http://2018.qq.com/"
	html = get_html(url)
	# 判断获得html是否为空
	if html:
		# 解析html获得数据
		infos = parse_html(html)
		# 将数据存入数据库
		save_to_mysql(infos)
	else:
		print("没有获取到html")


if __name__ == "__main__":
	main()