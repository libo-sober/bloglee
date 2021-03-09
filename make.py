import re

# s = '<link rel="stylesheet" href="static/css/jquery.fancybox.min.css">' \
#     '<script src="static/js/jquery.fancybox.min.js"></script><script ' \
#     'src="static/js/qrcode.min.js"></script>'

# pattern = re.compile("'static/(.*?)'",flags=re.S)  # 一种是单引号引起
pattern = re.compile('"static/(.*?)"',flags=re.S) # 一种是双引号引起
# rs = re.findall(pattern, s)
# for s1 in rs:
#     ss = 'static/' + s1
#     # print(ss)
#     su = "{% static '" + s1 + "' %}"
#     # print(su)
#     s = re.sub(ss,su,s)
# with open('111', mode='r', encoding='utf-8') as fp:
#     # print(fp)
#     r = fp.read()
#     print(r)
#     with open('index.html', mode='w+', encoding='utf-8') as f:
#         f.write(s)
# print(rs)
with open('templates/datail.html', mode='r', encoding='utf-8') as fp:
    s = fp.read()
    rs = re.findall(pattern, s)
    for s1 in rs:
        ss = 'static/' + s1
        su = "{% static '" + s1 + "' %}"
        s = re.sub(ss, su, s)
    with open('index.html', mode='w+', encoding='utf-8') as f:
        f.write(s)
