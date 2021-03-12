import re
from random import randint
from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.simple_tag()
def random_num():
    return randint(1, 10)


@register.filter(is_safe=True)
@stringfilter
def custom_markdown(content):
    # 给code标签中的代码快添加语言和行号
    code_list = re.findall(r'<pre><code class="lang-(.*)">', content, re.M)
    for code in code_list:
        content = re.sub(r'<pre><code class="(.*)">',
                         '<pre class="language-{code}"><code class="language-{code} line-numbers">'.format(code=code.lower()), content,  # line-numbers添加行号
                         1)

    # # 给所有的h标签添加id属性值
    # h_list = re.findall(r'<h\d>')

    return content


@register.inclusion_tag('navigation.html')
def navigation(categories):
    return {'categories': categories,}
