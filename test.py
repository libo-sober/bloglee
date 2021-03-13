# import collections
#
# TEMP1 = """
# <div class='content' style='margin-left:%s;'>
#     <span>%s</span>
# """
#
#
# def generate_comment_html(sub_comment_dic, margin_left_val):
#     html = '<div class="comment">'
#     # 遍历子元素
#     for k, v_dic in sub_comment_dic.items():
#         html += TEMP1 % (margin_left_val, k[1])
#         # 假如子元素的值为真,说明有子评论
#         if v_dic:
#             # 递归处理,直到全部处理完
#             html += generate_comment_html(v_dic, margin_left_val)
#         html += "</div>"
#     html += "</div>"
#     return html
#
#
# def tree(comment_dic):
#     html = '<div class="comment">'
#     for k, v in comment_dic.items():
#
#         html += TEMP1 % (0, k[1])
#         print(html)
#         # 设置向右偏移30个像素
#         html += generate_comment_html(v, 30)
#         html += "</div>"
#     html += '</div>'
#
#     return (html)
#
#
# def tree_search(d_dic, comment_obj):
#     # 在comment_dic中一个一个的寻找其回复的评论
#     # 检查当前评论的 reply_id 和 comment_dic中已有评论的nid是否相同，
#     # 如果相同，表示就是回复的此信息
#     #   如果不同，则需要去 comment_dic 的所有子元素中寻找，一直找，如果一系列中未找，则继续向下找
#     for k, v_dic in d_dic.items():
#         # 找回复的评论，将自己添加到其对应的字典中，例如： {评论一： {回复一：{},回复二：{}}}
#         if k[0] == comment_obj[2]:
#             d_dic[k][comment_obj] = collections.OrderedDict()
#             return
#         else:
#             # 在当前第一个跟元素中递归的去寻找父亲
#             tree_search(d_dic[k], comment_obj)
#
#
# def build_tree(comment_list):
#
#     comment_dic = {}
#     for comment_obj in comment_list:
#         comment_obj['children'] = []
#         comment_dic[comment_obj['pk']] = comment_obj
#
#     for comment in comment_list:
#         p_obj = comment_dic.get(comment['pid'])
#         if not p_obj:
#             ret.append(comment)
#         else:
#             p_obj['children'].append(comment)
#
#     return comment_dic
#
#
# # comment_list = [
# #     (1, '111', None),
# #     (2, '222', None),
# #     (3, '33', None),
# #     (9, '999', 5),
# #     (4, '444', 2),
# #     (5, '555', 1),
# #     (6, '666', 4),
# #     (7, '777', 2),
# #     (8, '888', 4),
# # ]
# comment_list = [{'pid': None, 'fu_username': None, 'pk': 21, 'content': '哈哈哈', 'username': 'libo',
#                  'add_time': '2021-03-11 12:53:14'},
#                 {'pid': 21, 'fu_username': 'libo', 'pk': 29, 'content': '笑你妈', 'username': 'h8fanc6o',
#                  'add_time': '2021-03-11 13:34:41'},
#                 {'pid': 29, 'fu_username': 'h8fanc6o', 'pk': 30, 'content': '你管人家', 'username': 'gzjuq2rh',
#                  'add_time': '2021-03-11 13:35:29'},
#                 {'pid': None, 'fu_username': None, 'pk': 31, 'content': '我来了', 'username': 'taibai',
#                  'add_time': '2021-03-11 13:35:49'},
#                 {'pid': 21, 'fu_username': 'libo', 'pk': 32, 'content': '开心吗', 'username': 'taibai666',
#                  'add_time': '2021-03-11 13:36:20'},
#                 {'pid': 21, 'fu_username': 'libo', 'pk': 34, 'content': '<img src="/static/picture/aini_org.png">',
#                  'username': 'libo', 'add_time': '2021-03-13 10:52:43'}]
#
# comment_dict = build_tree(comment_list)
# print(ret)
def tree_son(comment):
    zi_com = ''
    for com in comment:
        zi_com += f"daa{com['content']}daad"
        if com['children'] != []:
            zi_com += tree_son(com['children'])
    return zi_com

def tree(ret):
    comment = ''
    for comment_dicts in ret:
        # print(comment_dicts)
        comment += f"dda{comment_dicts['content']}dada"
        # print(comment_dicts['children'])
        if comment_dicts['children'] != []:
            # print(comment_dicts['children'])
            comment += tree_son(comment_dicts['children'])
    return comment


ret = [{
	'pid': None,
	'fu_username': None,
	'pk': 21,
	'content': '哈哈哈',
	'username': 'libo',
	'add_time': '2021-03-11 12:53:14',
	'children': [{
		'pid': 21,
		'fu_username': 'libo',
		'pk': 29,
		'content': '笑你妈',
		'username': 'h8fanc6o',
		'add_time': '2021-03-11 13:34:41',
		'children': [{
			'pid': 29,
			'fu_username': 'h8fanc6o',
			'pk': 30,
			'content': '你管人家',
			'username': 'gzjuq2rh',
			'add_time': '2021-03-11 13:35:29',
			'children': []
		}]
	}, {
		'pid': 21,
		'fu_username': 'libo',
		'pk': 32,
		'content': '开心吗',
		'username': 'taibai666',
		'add_time': '2021-03-11 13:36:20',
		'children': []
	}, {
		'pid': 21,
		'fu_username': 'libo',
		'pk': 34,
		'content': '<img src="/static/picture/aini_org.png">',
		'username': 'libo',
		'add_time': '2021-03-13 10:52:43',
		'children': []
	}]
}, {
	'pid': None,
	'fu_username': None,
	'pk': 31,
	'content': '我来了',
	'username': 'taibai',
	'add_time': '2021-03-11 13:35:49',
	'children': []
}]



print(tree(ret))