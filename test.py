import re

def replace(text):
  pattern = r"(https?://[^\s]+)"

  for m in re.finditer(pattern, text):
      start, end = m.span()
      
      # 在左侧添加 ](
      text = text[:start] + "]( " + text[start:]

      # 在右侧添加 ) 
      text = text[:end+3] + ")"
    
  return text

f1 = open('raw.txt', 'r+')
f2 = open('result.md', 'a+')

# for line in f1.readlines():
#   f2.write(replace(line))

def reorg_line(title, note, link):
  if note is not None and link is not None:
    return '['+title+']('+link+'): '+note
  elif note is not None:
    return title +': '+note
  elif link is not None:
    return  '['+title+']('+link+')'
  else:
    return title

lines = f1.readlines()
title_start = '⬜ '
link_start = '        Notes: http'
note_start = '        Notes: '
http_pattern = r"(https?://[^\s]+)"
for line_num in range(len(lines)-1):
  line = lines[line_num]
  next_line = lines[line_num+1]
  start=end=0
  if line.startswith(title_start) and next_line.startswith(link_start):
    title = line[len(title_start):-1]
    link = next_line[len(link_start)-4:-1]
    note = None
    # print(reorg_line(title, None, link))
  elif line.startswith(title_start) and next_line.startswith(note_start):
    title = line[len(title_start):-1]
    # note = next_line[len(note_start):]
    for it in re.finditer(http_pattern, next_line):
      start, end = it.span()
    if start != end:
      link = next_line[start:end]
      note = next_line[len(note_start):start]
    else:
      link = None
      note = next_line[len(note_start):]
  elif line.startswith(title_start):
    title = line[len(title_start):-1]
    link = None
    note = None
  else:
    title = link = note = None
  if title is not None and note is not None:
    if title in note or note in title:
      note = None
  new_line = reorg_line(title, note, link)
  if new_line is not None:
    f2.writelines(new_line + '\n\n')