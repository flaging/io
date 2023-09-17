import re
import os

# text = "[Example](https://www.example.com):This is an example link"

def parse_pattern(text):
  pattern = r'\[([^]]+)\]\(([^)]+)\):(.*)'
  pattern2 = r'\[([^]]+)\]\(([^)]+)\)'

  match = re.search(pattern, text)
  match2 = re.search(pattern2, text)

  # print('match succes', match, match2)
  # exit()
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
# file_name = 'src/23-09-09-2.md'
def match_link(file_name, total_link):
# file_name = 'src/02.deep-models.md'
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
      # elif other not in total_link[link]:
      #   total_link[link][file_name] = other
  return total_link

for file in os.listdir('src'):
  total_link = match_link('src/'+file, total_link)
cnt = 0
for link in total_link.keys():
  if len(total_link[link]) > 1 or 'kuaishou.com' in link:
    for var in total_link[link]:
      cnt +=1
      print(link, var[0], var[1], var[2]+':'+str(var[3]))
      
print('links dup num: ', cnt)
print('all link num :', len(total_link.keys()))
    