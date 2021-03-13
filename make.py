import re

# s = '<link rel="stylesheet" href="static/css/jquery.fancybox.min.css">' \
#     '<script src="static/js/jquery.fancybox.min.js"></script><script ' \
#     'src="static/js/qrcode.min.js"></script>'

# pattern = re.compile("'static/(.*?)'",flags=re.S)  # 一种是单引号引起
# pattern = re.compile('"static/(.*?)"',flags=re.S) # 一种是双引号引起
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
# with open('templates/datail.html', mode='r', encoding='utf-8') as fp:
#     s = fp.read()
#     rs = re.findall(pattern, s)
#     for s1 in rs:
#         ss = 'static/' + s1
#         su = "{% static '" + s1 + "' %}"
#         s = re.sub(ss, su, s)
#     with open('index.html', mode='w+', encoding='utf-8') as f:
#         f.write(s)

comment_list = [{'pid': None, 'fu_username': None, 'pk': 21, 'content': '哈哈哈', 'username': 'libo',
                 'add_time': '2021-03-11 12:53:14'},
                {'pid': 21, 'fu_username': 'libo', 'pk': 29, 'content': '笑你妈', 'username': 'h8fanc6o',
                 'add_time': '2021-03-11 13:34:41'},
                {'pid': 29, 'fu_username': 'h8fanc6o', 'pk': 30, 'content': '你管人家', 'username': 'gzjuq2rh',
                 'add_time': '2021-03-11 13:35:29'},
                {'pid': None, 'fu_username': None, 'pk': 31, 'content': '我来了', 'username': 'taibai',
                 'add_time': '2021-03-11 13:35:49'},
                {'pid': 21, 'fu_username': 'libo', 'pk': 32, 'content': '开心吗', 'username': 'taibai666',
                 'add_time': '2021-03-11 13:36:20'},
                {'pid': 21, 'fu_username': 'libo', 'pk': 34, 'content': '<img src="/static/picture/aini_org.png">',
                 'username': 'libo', 'add_time': '2021-03-13 10:52:43'}]

comment_dic = {}
for index, comment_obj in enumerate(comment_list):
    comment_dic[index] = comment_obj
print(comment_dic)

