 # Markdown插入视频
# https://www.jianshu.com/p/3525536f9dcd
import html
s = 'dasdasdas<script> alert("哈哈") </script>dsadasdas'
res = html.escape()
print(res)
