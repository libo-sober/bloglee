 # Markdown插入视频
# https://www.jianshu.com/p/3525536f9dcd
import re
# value = '111111111111@qq.com'
value = 'ww11_@qq.com'
email_re = re.compile(r'\w{5,12}@(.*).com$')
res = email_re.match(value)
print(res)