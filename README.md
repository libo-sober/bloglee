# bloglee<a href="https://www.liboer.top/" target="_blank">
# 建站呕血历程（Django3强力驱动）

## 前言

> 关于建立自己的个人网站，我也是尝试了很多次。第一次是学生活动免费试用阿里云服务器，结果几天后就到期啦。只会的一段时间，又碰到一个活动机会，申请了两个月的服务器。当时借助于<span style="color: rgb(75, 172, 198);">WordPress</span>建立了一个博客网站，虽然有很多风格可选择，但是，仍然感觉巨丑。随后，服务器也到期了，便没做他想。到了今天，看到别人的华丽博客后，终于忍不住自己斥资也建立了一个。整个网站前后差不多一个月就上线啦吧，其中无时无刻不在忙它。主要有了这个想法之后，完不成心里就一直想着，也无心干其他事情。

## 前端布局

这里还是要声明一下，我前端没有设计天赋，也是找各种大神的博客做<span style="color: rgb(75, 172, 198);">参照</span>，根据他们的样式来做前端。本人设计思想也不出众，只好<span style="color: rgb(75, 172, 198);">借助</span>别人设计好的风格，加上<span style="color: rgb(75, 172, 198);">bootstrap</span>快速建立了前端。前端布局主要借助了<a href="https://oneisall.top/" target="_blank">未雨晴空</a>大佬的博客，其中也想到过是不是设计到<span style="color: rgb(75, 172, 198);">版权</span>问题，但想到自己纯属借鉴，又不是全搬照抄。再者也不是商业用途，也加上了自己的思想，所以应该不构成版权纠纷。当然，这里也欢迎所有的朋友们来借鉴我的博客，本人会非常欢迎。在这里如果有设计到<span style="color: rgb(75, 172, 198);">侵权</span>的问题，也欢迎当事人联系我更改或删除。

 关于前端页面，大家也可以去各大模板网站去寻找自己喜欢的样式。我也是主学后端的，前端确实不怎么样，但往往别人喜欢你的网站都是因为漂亮的前端<img src="/static/picture/erha_org.png">~

## 后端开发

后端主要使用的<span style="color: rgb(75, 172, 198);">Django+simpleui</span>进行开发。这里就多说一点，前端经过我的借鉴和修改后只是一个个静态的网页，什么都是已经写死的。在我开发后端的时候，需要**考虑前端的展示效果**，即需要给前端发送什么类型的数据，以实现静态页面和数据库的**动态交互**。

前后端数据交互主要有两种：

1. 通过Form来发送POST或GET请求，在action属性中指定url。后端收到数据后，对数据库进行相应的操作后将得到的数据反馈给前端，最后在前端进行渲染。例如我的注册页面：

   html页面

   ```html
   <form class="form-signin bg-white" method="post" action="/user/register" id="register-form">
       {% csrf_token %}
       // 只取了一个input
       <div class="form-label-group">
           <input type="text" id="inputUsername" name="username" value="" class="form-control " placeholder="用户名"
                  aria-describedby="usernameHelpBlock" required="" autofocus="">
           <label for="inputUsername">用户名</label>
           <small id="usernameHelpBlock" class="form-text text-muted">
               用户名只能包括中文，字母，数字,长度限制在2—15位
           </small>
           <div class="invalid-feedback" id="username-feedback">
           </div>
       </div>
   
   </form>
   ```

2. 使用Ajax。Ajax主要优点就是可以实现不刷新页面和后端交互，Form必须刷新页面才会发送请求。

   ```javascript
   <script>
       $('.dianjipwd').click(function () {
   
           var new_password = $('#new_password').val()
           var old_password = $('#old_password').val()
           var csrf = $("[name=csrfmiddlewaretoken]").val()
   
           $.ajax({
               url: "{% url 'modify' %}",
               type: "post",
               data: {
                   new_password: new_password,
                   old_password: old_password,
                   csrfmiddlewaretoken: csrf,
               },
               success: function (data) {
                   console.log(data)
                   if (data.code != 200) {
   
                   } else {
                   
                   }
               }
           })
                       
       })
   </script>
   ```

后端就是采用views视图函数和modles来处理了。

主要提一下<span style="color: rgb(75, 172, 198);">Django admin</span>还是很实用的。有了它就不用为文章发表专门简历一个后台了，通过admin可以很方便的操作数据库。还有就是Django的<span style="color: rgb(75, 172, 198);">ORM</span>，这是我喜欢用Django开发的一个非常重要的原因。它集成的ORM可以很方便的操作数据库，而且无论你用的什么数据库，你只需要会ORM一种语言方法即可，它会自动的帮我们转换，非常方便。使得我们不用耗费精力再去学习其他的数据库语言。

## 数据库

这里我使用的MySQL数据库，因为对MySQL的一些常规操作还算比较熟悉。况且本站也没有涉及到到大量的事务操作，因为我没有允许用户简历个人站点，只有管理员负责文章的修改和发布（**服务器配置跟不上**）。

## 项目部署

项目部署主要采用**nginx+uwsgi**。使用倒是很简单，但总会出一些小问题，这里也是配置了好久才行。记忆最深的就是搜集静态文件的路径问题，包括Django的和uwsgi的，但总算是成功了。

## 存在的问题

目前小站还存在很多待优化的问题，包括未测出的bug、页面加载速度等。在使用中遇到bug欢迎留言告知。最后感谢大家的来访，记得小红心走起来~<img src="/static/picture/1.gif">
