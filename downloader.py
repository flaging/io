import requests
from lxml import html
import random
import time

class Base:
  user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
  def __init__(self):
    self.page_root = None
    self.html_bytes = None
  def random_sleep(self, scale = 2, sleep=1, ratio=0.3):
    index = random.uniform(0.0, 1.0)
    scale = 1 if index > ratio else scale
    time.sleep(random.uniform(0.01, 1) * sleep * scale)
  def download(self, url, cookie):
    headers = {'User_Agent': user_agent, 'Cookie': cookie} \
      if cookie is not None else {'User_Agent': user_agent}
    random_sleep()
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    page = resp.text
    self.html_bytes = page.encode('utf-8')
    self.page_root = html.fromstring(self.html_bytes)
  def get_content(self, pattern):
    return page_root.xpath(pattern)
  def page_parse(self):
    patterns = build_pattern()
    page_data = {}
    for content_type, pattern in patterns:
      page_data[content_type] = get_content(pattern)
    page_data['raw_data']= self.html_bytes
    return page_data
  def build_pattern(self):
    assert "patterns not implemented"

from dataclasses import dataclass
@dataclass
class Data:
  origin_url: str
  default_title: str
  contained_urls = []
  weibo_urls = []
  zhihu_urls = []
  github_urls = []
  contents = []
  
class DataFormat:
  def to_markdown(data:Data):
    
  
    