import collections

TEMP1 = """
<div class='content' style='margin-left:%s;'>
    <span>%s</span>
"""


def generate_comment_html(sub_comment_dic, margin_left_val):
    html = '<div class="comment">'
    # 遍历子元素
    for k, v_dic in sub_comment_dic.items():
        html += TEMP1 % (margin_left_val, k[1])
        # 假如子元素的值为真,说明有子评论
        if v_dic:
            # 递归处理,直到全部处理完
            html += generate_comment_html(v_dic, margin_left_val)
        html += "</div>"
    html += "</div>"
    return html


def tree(comment_dic):
    html = '<div class="comment">'
    for k, v in comment_dic.items():

        print(k, '++++++' ,v)
        print(k[1])
        html += TEMP1 % (0, k[1])
        print(html)
        # 设置向右偏移30个像素
        html += generate_comment_html(v, 30)
        html += "</div>"
    html += '</div>'

    return (html)


def tree_search(d_dic, comment_obj):
    # 在comment_dic中一个一个的寻找其回复的评论
    # 检查当前评论的 reply_id 和 comment_dic中已有评论的nid是否相同，
    # 如果相同，表示就是回复的此信息
    #   如果不同，则需要去 comment_dic 的所有子元素中寻找，一直找，如果一系列中未找，则继续向下找
    for k, v_dic in d_dic.items():
        # 找回复的评论，将自己添加到其对应的字典中，例如： {评论一： {回复一：{},回复二：{}}}
        if k[0] == comment_obj[2]:
            d_dic[k][comment_obj] = collections.OrderedDict()
            return
        else:
            # 在当前第一个跟元素中递归的去寻找父亲
            tree_search(d_dic[k], comment_obj)


def build_tree(comment_list):
    comment_dic = collections.OrderedDict()

    for comment_obj in comment_list:
        if comment_obj[2] is None:
            # 如果是根评论，添加到comment_dic[评论对象] ＝ {}
            comment_dic[comment_obj] = collections.OrderedDict()
        else:
            # 如果是回复的评论，则需要在 comment_dic 中找到其回复的评论
            tree_search(comment_dic, comment_obj)
    return comment_dic


comment_list = [
    (1, '111', None),
    (2, '222', None),
    (3, '33', None),
    (9, '999', 5),
    (4, '444', 2),
    (5, '555', 1),
    (6, '666', 4),
    (7, '777', 2),
    (8, '888', 4),
]



comment_dict = build_tree(comment_list)
res = tree(comment_dict)
print(res)
# OrderedDict(
#     [
#         (
#             (1, '111', None),
#             OrderedDict(
#                 [(
#                     (5, '555', 1),
#                     OrderedDict()
#                 )
#                  ])
#         ),
#
#         (
#             (2, '222', None),
#             OrderedDict(
#                 [(
#                     (4, '444', 2),
#                     OrderedDict([
#                         ((6, '666', 4), OrderedDict()),
#                         ((8, '888', 4), OrderedDict())])
#                 ),
#             (
#                 (7, '777', 2), OrderedDict())]
#             )
#         ),
#
#         (
#             (3, '33', None),
#             OrderedDict()
#         )
#     ]
# )
