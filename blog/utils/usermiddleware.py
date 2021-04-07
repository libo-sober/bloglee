import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, reverse
from blog import models


class MyUserAuth(MiddlewareMixin):

    def process_request(self, request):
        url_re = re.compile(r'/admin/(.*?)')
        user_id = request.session.get('user_id')
        black_list =[reverse('userinfo')]
        # 登录的用户对象
        if user_id:
            cur_user_name = models.UserInfo.objects.get(id=user_id)
        else:
            cur_user_name = None
        if url_re.match(request.path):
            if user_id:
                if not cur_user_name.is_admin:
                    return render(request, '404.html')
            else:
                return render(request, '404.html')
        if request.path in black_list:
            if not user_id:
                return render(request, '404.html')
