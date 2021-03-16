import re
from random import randint
from django import template
from blog import models
from BlogLee import settings
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.simple_tag()
def random_num():
    return randint(1, 10)


@register.simple_tag()
def img_url(comment):
    qq_number = comment.qq_email[:-7]
    user_obj = models.UserInfo.objects.filter(username=comment.username).first()
    if user_obj:
        if user_obj.is_admin:
            img_url = settings.ADMIN_IMG
        else:
            img_url = f'http://q.qlogo.cn/headimg_dl?dst_uin={qq_number}&spec=640&img_type=jpg'
    else:
        img_url = f'http://q.qlogo.cn/headimg_dl?dst_uin={qq_number}&spec=640&img_type=jpg'
    return img_url


@register.filter(is_safe=True)
@stringfilter
def custom_markdown(content):
    # 给code标签中的代码快添加语言和行号
    code_list = re.findall(r'<pre><code class="lang-(.*)">', content, re.M)
    for code in code_list:
        content = re.sub(r'<pre><code class="(.*)">',
                         '<pre class="language-{code}"><code class="language-{code} line-numbers">'.format(
                             code=code.lower()), content,  # line-numbers添加行号
                         1)

    # # 给所有的h标签添加id属性值
    # h_list = re.findall(r'<h\d>')

    return content


@register.inclusion_tag('navigation.html')
def navigation(categories, cur_user_name, columns):
    return {'categories': categories, 'cur_user_name': cur_user_name, 'columns': columns, }


def tree_son(comment):
    zi_com = ''
    for com in comment:
        pk = com['pk']
        pid = com['pid']
        username = com['username']
        add_time = com['add_time']
        content = com['content']
        fu_username = com['fu_username']
        qq_url = com['qq_url']
        is_admin = com['is_admin']
        fu_is_admin = com['fu_is_admin']
        admin_img = com['admin_img']
        img = admin_img if is_admin else qq_url

        zi_com += f"""
    <ol class="children">
        <li class="list-group-item comment-{pk} mt-3 px-2 pt-3 pb-2 depth-0" comment_id={pk}>
                    <div class="clearfix" id="div-comment-{pk}">
                        <div class="media">
                            <img src={img}
                                 class="mr-3 rounded-circle" width="50" height="50 "
                                 onerror="javascript:this.src='/static/image/unknow.png';">
                            <div class="media-body">
                                <div class="comment-info">
                """
        if is_admin:
            zi_com += f"""
                                                <cite class="c3">

                                                   <a href="/" class='text-reset superuser'>{username}</a>

                                                </cite>
                        """
        else:
            zi_com +=    f"""
                                    <cite class="c3">

                                        {username}

                                    </cite>
            """

        zi_com +=   f"""
                       <i class="fa fa-share fa-fw fa-1x mr-2 c1" aria-hidden="true"></i>
                       <cite class="c3"><a href="#div-comment-{pid}" class="text-reset">
"""
        if fu_is_admin:
            zi_com += f"""
                       <a href="/" class='text-reset superuser'>{fu_username}</a>
                    """
        else:
            zi_com += f"""
                       {fu_username}
                    """
        zi_com += f"""
                       </a></cite>
                                                       </div>
                                <div class="comment-meta"><span
                                        class="font-weight-light text-muted">{add_time}</span>
                                </div>
                            </div>
                        </div>
                        <p class="text-break mt-2">{content}</p>
                        <a class="btn btn-sm btn-secondary float-right"
                           onclick="reply('div-comment-{pk}','{pk}')">回复</a>
                    </div>                </li>
        """
        if com['children'] != []:
            zi_com += tree_son(com['children'])
        zi_com += '</ol>'
    return zi_com


@register.filter(is_safe=True)
def build_coment_tree(ret):

    comment = ''
    for comment_dicts in ret:
        pk = comment_dicts['pk']
        username = comment_dicts['username']
        add_time = comment_dicts['add_time']
        content = comment_dicts['content']
        qq_url = comment_dicts['qq_url']
        is_admin = comment_dicts['is_admin']
        admin_img = comment_dicts['admin_img']
        img = admin_img if is_admin else qq_url


        comment += f""" 
                    <li class="list-group-item comment-{pk} mt-3 px-2 pt-3 pb-2 depth-0" comment_id={pk}>
                        <div class="clearfix" id="div-comment-{pk}">
                            <div class="media">
                                <img src={img}
                                     class="mr-3 rounded-circle" width="50" height="50"
                                     onerror="javascript:this.src='/static/image/unknow.png';">
                                <div class="media-body">
                                    <div class="comment-info">
                    """
        if is_admin:
            comment += f"""               <cite class="c3">

                                        <a href="/" class='text-reset superuser'>{username}</a>

                                        </cite>
                    """
        else:
            comment += f"""               <cite class="c3">

                                                        {username}

                                                    </cite>
                                """
        comment += f"""
                                    </div>
                                    <div class="comment-meta"><span
                                            class="font-weight-light text-muted">{add_time}</span>
                                    </div>
                                </div>
                            </div>
                            <p class="text-break mt-2">{content}</p>
                            <a class="btn btn-sm btn-secondary float-right"
                               onclick="reply('div-comment-{pk}','{pk}')">回复</a>
                        </div>               
                    """
        if comment_dicts['children'] != []:
            comment += tree_son(comment_dicts['children'])

        comment += ' </li>'

    return comment
