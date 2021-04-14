 # Markdown插入视频
# https://www.jianshu.com/p/3525536f9dcd
import re
# content = '<p><img src="/media/editor\p=0_20210413232131323675.jpg" alt="">' \
#           '<br>' \
#           '<img src="https://er" alt="在这里插入图片描述">' \
#           '</p>'
# img_list = re.findall(r'<img src="(.*)">', content, re.M)
# print('********************************')
# print('img_list', img_list)
# print('********************************')
# for img in img_list:
#     print('********************************')
#     print('img', img)
#     print('********************************')
#     content = re.sub(r'<img src=(.*)">',
#                      f'<div align="center"><img src="{img[0]}" alt="{img[1]}" class="spotlight"></div>',
#                      content,
#                      2
#                      )
#     print('********************************')
#     print('content', content)
#     print('********************************')
content = '<pre><code class="lang-javascript">111111' \
          '</code></pre>' \
          '<pre><code class="lang-html">22222' \
          '</code></pre>'
print('custom')
code_list = re.findall(r'<pre><code class="lang-(.*)">', content, re.M)
print(code_list)
for code in code_list:
    content = re.sub(r'<pre><code class="(.*)">',
                     '<pre class="language-{code}"><code class="language-{code} line-numbers">'.format(
                         code=code.lower()), content,  # line-numbers添加行号
                     1)

