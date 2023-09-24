import requests
from lxml import html

def get_weibo_data_from_url(url):
  # url='https://weibo.cn/1402400261/LBuKWw2ii'
  user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
  def get_cookie():
    file = open('../cookie.txt', 'r')
    return file.read()
  
  cookie = get_cookie()
  # 请求页面
  headers = {'User_Agent': user_agent, 'Cookie': cookie}
  resp = requests.get(url, headers=headers)
  # resp = requests.get(url)
  resp.encoding = 'utf-8'
  page = resp.text
  # print(page)
  html_bytes = page.encode('utf-8')
  # print(html_bytes)
  root = html.fromstring(html_bytes)

  # 提取正文 
  article = root.xpath("//span[@class='ctt']/text()")
  content = ''.join(article)

  # 提取图片链接
  images = root.xpath('//img/@src')
  real_images = []
  for image in images:
    if 'jpg' in image:
      real_images.append(image.replace('wap180', 'large'))
  links = root.xpath('//a/@href')
  # print(links)
  # print(real_images)
  mobile_pic_link = []
  for link in links:
    if link.startswith('/') and '/pic/' in link:
      mobile_pic_link.append('https://weibo.cn/'+link)
  #     print('https://weibo.cn/'+link)
  # print(mobile_pic_link)
  title = root.xpath("//a[1]/text()")[3]
  return content, real_images, title, mobile_pic_link, html_bytes

