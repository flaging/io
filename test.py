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

f1 = open('raw.md', 'r+')
f2 = open('result.md', 'a+')

for line in f1.readlines():
  f2.write(replace(line))