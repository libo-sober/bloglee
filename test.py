 # Markdown插入视频
# https://www.jianshu.com/p/3525536f9dcd
import html
import re
s2 = 'dasdasdas<script> alert("哈哈") </script>dsadasdas'
s = 'dasdasdas<img src="sss">>dsadasdas'
re_script = re.compile(r'<script>(.*?)</script>')

if re_script.search(s):
    res = html.escape(s)
else:
    res = s
print(res)
