import re
import os

# text = "[Example](https://www.example.com):This is an example link"

def parse_pattern(text):
  pattern = r'\[([^]]+)\]\(([^)]+)\):(.*)'
  pattern2 = r'\[([^]]+)\]\(([^)]+)\)'

  match = re.search(pattern, text)
  match2 = re.search(pattern2, text)

  if match:
    title = match.group(1)
    link = match.group(2)
    note = match.group(3).strip()
  elif match2:
    title = match2.group(1)
    link = match2.group(2)
    note = None
  else:
    title = None
    link = None
    note = None
  return link, (title, note)
total_link = {}
def match_link(file_name, total_link):
  line_num = 0
  for line in open(file_name).readlines():
    line_num += 1
    if len(line) <= 1:continue
    link, other = parse_pattern(line)
    # print(link, other)
    other = other + (file_name,)
    other = other + (line_num,)
    if link is not None:
      if link not in total_link.keys():
        total_link[link] = [other]
      else:
        total_link[link].append(other)
  return total_link
import random
import time
def print_github(succeed, content):
  pattern = r'github\.com/[A-Za-z0-9./\-\_]+'  
  links = re.findall(pattern, content)
  for link in links:
    if link.startswith('http'):
      succeed.writelines('\n\nGithub: ['+link+']('+link+')')
    else:
      succeed.writelines('\n\nGithub: ['+link+'](https://'+link+')')
def print_md(succeed, title, link, content, links, mobile_pic_link):
  if len(content) > 1:
    if content.startswith(':'): content = content[1:]
  title_content = content[:50] if len(content) > 50 else content
  title = title if title.startswith('@') else '@'+title
  succeed.writelines('\n\n#### [' + title_content + ' ' + title + ']('+link+')')
  content.strip()
  if len(content) > 1:
    succeed.writelines('\n\nNote: '+content)
  for num, link in enumerate(links):
    succeed.writelines('\n\nPicture: ['+link.split('/')[-1]+']('+mobile_pic_link[0]+')')
  print_github(succeed, content)
  succeed.flush()
  
def random_sleep():
  index = random.randint(1,10)
  scale = 1
  if index > 8: scale = 10
  time.sleep(random.randint(1, 200)/200.0*scale)
total_link = match_link('src/23-12-09.md', total_link)
# total_link = open('2023-09-23-16:58:35.failed.txt', 'r').readlines()
from  weibo import get_weibo_data_from_url as downloader
now = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
failed = open(now+'.failed.txt', 'w')
failed.writelines('failed urls:\n')
succeed = open(now+'.md', 'w')
for link in total_link.keys():
# for link in total_link:
  if 'weibo.com' in link:
    link_mobile = link.replace('weibo.com', 'weibo.cn')
    html_bytes = ''
    try:
      content, images, title, mobile_pic_link, html_bytes = downloader(link_mobile)
      print_md(succeed, title, link, content, images, mobile_pic_link)
    except:
      failed.writelines(link+'\n')
      failed.flush()
      if len(html_bytes)>1:
        print(html_bytes)
  random_sleep()