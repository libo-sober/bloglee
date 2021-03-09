$(function () {
	//开启bootstrap的插件tooltip
	$('[data-toggle="tooltip"]').tooltip();
	//开启bootstrap的插件popover
	$('[data-toggle="popover"]').popover();

	// 侧边栏添加书签事件
    $(".bookmark").on("click",function(){
        Swal.fire("按CTRL+D键将本页添加书签");
        //layer.msg("按CTRL+D键将本页添加书签",{icon:6,time:1000});
    })

	//评论页面提交按钮鼠标移入事件
	// $("#comment-submit").on("mouseover",function () {
	//     Swal.fire('呐 首次评论需要审核，请耐心等待哦~');
	// 	//layer.msg("呐 首次评论需要审核，请耐心等待哦~",{icon:6,time:1000});
	// });

    //注册刷新验证码点击事件
    $('#register-form .captcha').click({'form_id':'register-form'},refresh_captcha);


    //首页footer右边底部工具栏
	$(".box-gotop").click(function(){
		$('html, body').animate({
			scrollTop: $('html').offset().top
		}, 500);
	})

    //首页footer右边底部工具栏动态显示
	$(window).scroll(function(){
		var $win = $(window);
		if ($win.scrollTop()>200){
			$('.box-gotop').addClass('active');
		}else {
			$('.box-gotop').removeClass('active');
		}
	})
    //开始阅读按钮事件
    $("#start-view").on( 'click', function(e) {
        e.preventDefault();
        var movingPosition = 0;
        if ( $(this).offset().top > $( document ).height() - $( window ).height() ) {
            movingPosition = $( document ).height() - $( window ).height();
        } else {
            movingPosition = $( this).offset().top;
        }
        $( 'html, body' ).animate({
        scrollTop: movingPosition
        }, 500, 'swing' );
    });


    //点击显示文章导航
    $("#btn-catalog").click(function () {
        if ($(".article-toc").css("display") === 'block') {
            //$("#article_navigation").css("display", "none");  //普通隐藏
            $(".article-toc").slideUp();
        } else {
            //文章导航定位，是否显示滚动条
            let windowHeight = $(window).height();
            $("#tocContainer").css({"margin-top": 0, "max-height": windowHeight - 260});
            $(".article-toc").slideDown();

        }
    });
    //控制侧边栏滚动
    controlSidebar();

    //页面初始化的时候，获取滚动条的高度（上次高度）,实现导航栏隐藏
    let start_height = $(document).scrollTop();
    //获取导航栏的高度(包含 padding 和 border)
    let navigation_height = $('.navbar ').outerHeight();
    $(window).scroll(function () {
        //触发滚动事件后，滚动条的高度（本次高度）
        let end_height = $(document).scrollTop();
        //触发后的高度 与 元素的高度对比
        if (end_height > navigation_height) {
            //$('#header').slideUp(1000);
            $('.navbar ').css('top', '-60px');
        } else {
            //$('#header').removeClass('hide');
            //$('#header').slideDown(1000);
            $('.navbar').css('top', '0');
        }
        //触发后的高度 与 上次触发后的高度
        if (end_height < start_height) {
            //$('#header').removeClass('hide');
            //$('#header').slideDown(1000);
            $('.navbar ').css('top', '0');
        }
        //再次获取滚动条的高度，用于下次触发事件后的对比
        start_height = $(document).scrollTop();
    });




$("#comment-submit").click(function () {

    $("#comment-submit").html("正在提交评论...");
    $("#comment-form").ajaxSubmit(function (data) {
                console.log(data);
                if(data.success==false){
                    if(data.error.username){
                        $("#username").addClass("is-invalid");
                        $("#username-feedback").html(data.error.username.join(","));
                    }
                    if(data.error.email){
                         $("#email").addClass("is-invalid");
                        $("#email-feedback").html(data.error.email.join(","));
                    }
                    if(data.error.link){
                        $("#link").addClass("is-invalid");
                    }
                    if(data.error.content){
                         $("#content").addClass("is-invalid");
                          $("#content-feedback").html(data.error.content.join(","));
                    }if(data.error.article_id) {
                        Swal.fire({text:data.error.article_id.join(","), type:'error'});
                        //layer.msg(data.error.article_id.join(","),{icon:2,time:3000});
                    }if(data.error.category_id){
                        Swal.fire({text:data.error.category_id.join(","), type:'error'});
                        //layer.msg(data.error.category_id.join(","),{icon:2,time:3000});
                    }if(data.error.parent_id){
                        Swal.fire({text:data.error.parent_id.join(","), type:'error'});
                    }if(data.error.msg){
                        Swal.fire({text:data.error.msg,type:'error'});
                    }
                }else {
                    if ($("input[name='parent']").val() != '0') {
                        $('#respond').before('<ol class="children">' + data.data + '</ol>');
                    } else {
                        $(".comment-list").append(data.data);
                    }
                    $("input[name='parent']").val(0);
                    $("#content").text("");//清空评论内容
                    //触发取消评论按钮点击事件即恢复评论输入框位置，同时隐藏取消评论按钮
                    $("#cancel-reply").trigger("click").addClass("d-none");
                    //页面反馈信息
                    Swal.fire("提交成功");
                }
                //恢复提交按钮内容
                $("#comment-submit").html("提交评论");
    })
})

})



//全局变量
var DoubanBookAPI=window.location.origin+"/douban/book/";
var DoubanSingleBookAPI=window.location.origin+"/douban/book/single";
var DoubanMovieAPI=window.location.origin+"/douban/movie/";
var DoubanSingleMovieAPI=window.location.origin+"/douban/movie/single";
var DoubanPageSize=10;


//初始化文章页面相关js
function initArticleJS(){
    //文章页面分享渠道——微信x悬浮事件
	$("#weixin").popover({html:true,trigger:"hover",placement:"auto",title:"分享到微信",content:generateQRcode(document.URL)});
	//文章页面分享按钮点击事件
	$("#share").click(function(){$(".share-group").fadeToggle("slow");});
	//文章页面audio标签设置微信audio样式
	$('.weixinAudio').weixinAudio({autoplay:false,});
	//文章页面关闭侧边栏事件
    $(".close-sidebar").on("click",function(){
        $(this).hide();
        $('#aside').fadeOut(1000);
        $('#main').animate(1000,function(){$(this).removeClass("col-lg-8").addClass("col-lg-12")});
        $('.show-sidebar').show();
    })
    //文章页面开启侧边栏事件
    $(".show-sidebar").on("click",function(){
        $(this).hide();
         $('.close-sidebar').show();
        $('#main').animate(1000,function(){$(this).removeClass("col-lg-12").addClass("col-lg-8")});
        $('#aside').fadeIn(1000);

    })
    //文章阅读模式初始化
    $("[data-morphing]").fancyMorph({hash : 'morphing'});
    $.fancybox.defaults.buttons = ["zoom", "download", "thumbs", "close"];
    //执行fancybox的画廊效果
    $('[data-fancybox="gallery"]').fancybox({});
}

//页面加载时间统计事件
function loadNeedTime(){
    var now = new Date().getTime();
    var page_load_time = now-performance.timing.navigationStart;
    //console.clear();
    console.log('%c页面加载完毕消耗了'+Math.round(performance.now()*100)/100+'ms','background:#fff;color:#333;text-shadow:0 0 2px #eee,0 0 3px #eee,0 0 3px #eee,0 0 2px #eee,0 0 3px #eee;');
}

//切换标签实现网页标题变化
function changePageTitle(){
    var OriginTitile = document.title;
    var titleTime;
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            document.title = '404啦！!!!∑(ﾟДﾟノ)ノ ';
            clearTimeout(titleTime);
        } else {
            document.title = '哈哈，骗你的！ヾ(ﾟ∀ﾟゞ)';
            titleTime = setTimeout(function() {
                document.title = OriginTitile;
            }, 3000);
        }
    });
}

function loadJustifiedGallery(selector){
    //先判断是否加载了该js
    if (typeof $.fn.justifiedGallery == 'function') {
         //该插件依赖模式为<a><img/></a>,先等待fancybox加载完毕
         $(selector).justifiedGallery({margins: 5, padding: 5, rowHeight: 150})
    }

}


//markdown文章代码高亮
function highlightCodeForMDArticle(){
    if (typeof Prism !== 'undefined') {
        var pres = document.getElementsByTagName('pre');
        for (var i = 0; i < pres.length; i++){
            if (pres[i].getElementsByTagName('code').length > 0)
                pres[i].className += ' line-numbers';
        }
        Prism.highlightAll(true,null);
    }
}

//ueditor文章高亮代码
function highlightCodeForUEArticle(){
    if (typeof Prism !== 'undefined') {
        var pres = document.getElementsByTagName('pre');
        for (var i = 0; i < pres.length; i++){
            var content = document.getElementsByTagName("pre")[i].innerHTML;
            pres[i].innerHTML= '<code>'+content+'</code>';
            if (pres[i].getElementsByTagName('code').length > 0)
                pres[i].className += ' line-numbers';
        }
        Prism.highlightAll(true,null);
    }
}


//

//给图片添加fancybox特效（考虑页面加载速度，需要延时执行）
function loadFancyBox(selector,lazyload){
    //默认参数
	$.fancybox.defaults.buttons = ["zoom", "download", "thumbs", "close"];
	$(selector).each(function() {
		var b = $(this);
		//获取图片的alt属性
		if (void 0 !== b.attr("alt")) var c = b.attr("alt");
		else var c = "";
		//获取图片的父节点
		var d = b.parent("a"),
		//判断是否有该noGallery属性
		e = typeof b.attr("gallery-off"),
		//判断是否有imgblur属性
		f = typeof b.attr("fancybox-on");
		//debugger;
		if ("undefined"===e) {
			var h = b.attr("class"),
			g=this.getAttribute("src");
			if(lazyload) {
                b.attr("data-original", g);
                b.removeAttr("src").removeAttr("style");
            }
			var j = b.prop("outerHTML");
			"undefined" !== f ? b.prop("outerHTML", '<a class="fancybox-on" data-fancybox="gallery" data-type="image" data-caption="'+c+'" href="' + g + '">' + j + "</a>") :
			b.prop("outerHTML", '<a class="" data-fancybox="gallery" data-type="image" data-caption="' + c + '" href="' + g + '">' + j + "</a>");
		}


	});
}



function loadRightMenu(){
    /*自定义右键菜单*/
    var oMenu = document.getElementById("rightClickMenu");
    var aLi = oMenu.getElementsByTagName("li");
    //加载后隐藏自定义右键菜单
    //oMenu.style.display = "none";
    //菜单鼠标移入/移出样式
    for (i = 0; i < aLi.length; i++) {
        //鼠标移入样式
        aLi[i].onmouseover = function () {
            $(this).addClass('active');
        };
        //鼠标移出样式
        aLi[i].onmouseout = function () {
            $(this).removeClass('active');
        };
    }
    //自定义菜单
    document.oncontextmenu = function (event) {
        $(oMenu).fadeOut(0);
        var event = event || window.event;
        var style = oMenu.style;
        $(oMenu).fadeIn(300);
        //style.display = "block";
        style.top = event.clientY + "px";
        style.left = event.clientX + "px";
        return false;
    };
    //页面点击后自定义菜单消失
    document.onclick = function () {
        $(oMenu).fadeOut(100);
        //oMenu.style.display = "none"
    }
}

//给文章h标签生成ID
function generateHID(){
    $("#article-content").children().each(function (index, element) {
    var tagName = $(this).get(0).tagName;
    if (tagName.substr(0, 1).toUpperCase() === "H") {
        var contentH = $(this).text();//获取内容
        var markid = "mark-" + tagName + "-" + index.toString();
        $(this).attr("id", markid);//为当前h标签设置id
        let spaceNum = "";
        if (tagName === 'H1') {
            spaceNum = "";
        } else if (tagName === 'H2') {
            spaceNum = "1";
        } else if (tagName === 'H3') {
            spaceNum = "1.5";
        } else if (tagName === 'H4') {
            spaceNum = "2";
        } else if (tagName === 'H5') {
            spaceNum = "2.5";
        } else if (tagName === 'H6') {
            spaceNum = "3";
        }
    }
    });
}

//控制侧边栏异步滚动
function controlSidebar(){
    if($("#sidebar").height()){
        if($("#main").height()>$("#sidebar").height()){
            console.log($("#sidebar").height());
            var footerHeight = 0;
            if($('#page-footer').length>0){
                footerHeight = $('#page-footer').outerHeight(true);
            }
            $('#sidebar').affix({
                offset:{
                    top:$('#sidebar').offset().top,
                    bottom:$('#footer').outerHeight(true)+footerHeight+30
                }

            });
        }
    }

}

//函数
//分享组点击事件
function share(obj,title,summary,pic){
	var qqShareURL="https://connect.qq.com/widget/shareqq/index.html?";
	var weiboShareURL="https://service.weibo.com/share/share.php?";
	var qzoneShareURL="https://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?";
	var host_url=window.location.href;
	var pic=window.location.host+pic;
	var _URL;
	if(obj=="qq"){
		_URL=qqShareURL+"url="+host_url+"&title="+title+"&pics="+pic+"&desc=&summary="+summary;
	}else if(obj=="weibo"){
		_URL=weiboShareURL+"url="+host_url+"&title="+title+summary+"&pic="+pic;
	}else if(obj=="qzone"){
		_URL=qzoneShareURL+"url="+host_url+"&title="+title+"&pics="+pic+"&desc=&summary="+summary;
	}
	window.open(_URL);
}

//回复函数
function reply(parentCommentDivId, parentCommentId) {
	//获取当前评论的div标签
	var parentCommentDiv = document.getElementById(parentCommentDivId),
	//获取输入框表单所在div
	responseDiv = document.getElementById('respond'), 
	//获取包含父评论信息的hidden的input
	input = document.getElementById('comment_parent'),
	//获取表单
	form = 'form' == responseDiv.tagName ? responseDiv : responseDiv.getElementsByTagName('form')[0],
	//获取文本域
	textarea = responseDiv.getElementsByTagName('textarea')[0];
	//如果还未生成隐藏域，则创建一个input，type为hidden，用来存储父评论信息
	if (null == input) {
		input = document.createElement('input');
		input.setAttribute('type','hidden');
		input.setAttribute('name','parent');
		input.setAttribute('id','comment_parent');
		//追加到表单末尾，用于向后台传递值
		form.appendChild(input);
	}
	//保存父评论id到隐藏域input上
	input.setAttribute('value',parentCommentId);

	//如果一个空的div不存在，则创建一个空的
	if (null == document.getElementById('comment-form-place-holder')) {
		var holder = document.createElement('div');
		holder.setAttribute("id","comment-form-place-holder");
		//将新建的div插入到评论div的前面（便于取消评论找到插入点）
		responseDiv.parentNode.insertBefore(holder, responseDiv);
	}
	//在父亲评论末尾追加评论表单div
	insertAfter(responseDiv,parentCommentDiv);
	
	
	//显示"取消回复按钮"
	document.getElementById('cancel-reply').classList.remove("d-none");
	//页面聚焦到文本域
	if (null != textarea && 'content' == textarea.name) {
		//聚焦到textarea
		textarea.focus();
	}
	//之所以返回false，是防止表单自动提交了
	return false;
}
//取消回复函数
function cancelReply(){
	//获取评论所在div
	var responseDiv = document.getElementById('respond'),
	//获取空的div
	holder = document.getElementById('comment-form-place-holder');
	//获取隐藏域
	input = document.getElementById('comment_parent');

	if (null != input) {
		input.setAttribute('value','0');
	}

	//如果空的div不存在，说明评论div未移动直接返回true
	if (null == holder) {
		return true;
	}
	//隐藏"取消回复"按钮
	document.getElementById('cancel-reply').classList.add('d-none');
	holder.parentNode.insertBefore(responseDiv, holder);
	holder.parentNode.removeChild(holder);
	return false;
}

//因为js没有直接追加到指定元素后面的方法，所以要自己创建一个方法 
function insertAfter(newElement,targetElement){
	// newElement是要追加的元素 targetElement 是指定元素的位置
	// 找到指定元素的父节点
	var parent = targetElement.parentNode;
	// 判断指定元素的是否是节点中的最后一个位置 如果是的话就直接使用appendChild方法
	if( parent.lastChild == targetElement){ 
		parent.appendChild(newElement);
	}else{
		parent.insertBefore(newElement, targetElement.nextSibling);
	}
}

//注册页面刷新验证码
function refresh_captcha(event){
    $.get({url:"/captcha/refresh/?"+Math.random(),processData:false,contentType:false,async:false},function(result){
        $('#'+event.data.form_id+' .captcha').attr("src",result.image_url);
        $('#id_captcha_0').attr("value",result.key);
    });
    return false;
}




//自动生成二维码插件
function generateQRcode(url) {
	//给文章生成二维码链接
	var element=document.createElement("div");
	var qrcode = new QRCode(element, {
	width: 100,
	height: 100,
	colorDark : "#000000",
	colorLight : "#ffffff",
	correctLevel : QRCode.CorrectLevel.H
	});
	qrcode.clear();
	qrcode.makeCode(url);
	return element;
}
//站点运行倒计时
function createtime(){
    var now = new Date();
    var grt = new Date("03/01/2020 00:00:00");//站点开始运行时间
    now.setTime(now.getTime()+250);
    days = (now-grt)/1000/60/60/24;dnum = Math.floor(days);
    hours = (now-grt)/1000/60/60-(24*dnum);hnum = Math.floor(hours);
    if(String(hnum).length==1){hnum = "0"+hnum;}
    minutes = (now-grt)/1000/60-(24*60*dnum)-(60*hnum);mnum = Math.floor(minutes);
    if(String(mnum).length==1){mnum = "0"+mnum;}
    seconds = (now-grt)/1000-(24*60*60*dnum)-(60*60*hnum)-(60*mnum);snum = Math.round(seconds);
    if(String(snum).length==1){snum = "0"+snum;}
    document.getElementById("web-time").innerHTML = dnum+"天"+hnum+"小时"+mnum+"分"+snum+"秒";
}



//bootstrap的affix.js插件，由于bootstap4移除了，需要单独引用
(function ($){
  'use strict';
  // AFFIX CLASS DEFINITION
  // ======================

  var Affix = function (element, options) {
    this.options = $.extend({}, Affix.DEFAULTS, options)

    this.$target = $(this.options.target)
      .on('scroll.bs.affix.data-api', $.proxy(this.checkPosition, this))
      .on('click.bs.affix.data-api',  $.proxy(this.checkPositionWithEventLoop, this))

    this.$element     = $(element)
    this.affixed      = null
    this.unpin        = null
    this.pinnedOffset = null

    this.checkPosition()
  }

  Affix.VERSION  = '3.3.7'

  Affix.RESET    = 'affix affix-top affix-bottom'

  Affix.DEFAULTS = {
    offset: 0,
    target: window
  }

  Affix.prototype.getState = function (scrollHeight, height, offsetTop, offsetBottom) {
    var scrollTop    = this.$target.scrollTop()
    var position     = this.$element.offset()
    var targetHeight = this.$target.height()

    if (offsetTop != null && this.affixed == 'top') return scrollTop < offsetTop ? 'top' : false

    if (this.affixed == 'bottom') {
      if (offsetTop != null) return (scrollTop + this.unpin <= position.top) ? false : 'bottom'
      return (scrollTop + targetHeight <= scrollHeight - offsetBottom) ? false : 'bottom'
    }

    var initializing   = this.affixed == null
    var colliderTop    = initializing ? scrollTop : position.top
    var colliderHeight = initializing ? targetHeight : height

    if (offsetTop != null && scrollTop <= offsetTop) return 'top'
    if (offsetBottom != null && (colliderTop + colliderHeight >= scrollHeight - offsetBottom)) return 'bottom'
    return false
  }

  Affix.prototype.getPinnedOffset = function () {
    if (this.pinnedOffset) return this.pinnedOffset
    this.$element.removeClass(Affix.RESET).addClass('affix')
    var scrollTop = this.$target.scrollTop()
    var position  = this.$element.offset()
    return (this.pinnedOffset = position.top - scrollTop)
  }

  Affix.prototype.checkPositionWithEventLoop = function () {
    setTimeout($.proxy(this.checkPosition, this), 1)
  }

  Affix.prototype.checkPosition = function () {
    if (!this.$element.is(':visible')) return

    var height       = this.$element.height()
    var offset       = this.options.offset
    var offsetTop    = offset.top
    var offsetBottom = offset.bottom
    var scrollHeight = Math.max($(document).height(), $(document.body).height())

    if (typeof offset != 'object')         offsetBottom = offsetTop = offset
    if (typeof offsetTop == 'function')    offsetTop    = offset.top(this.$element)
    if (typeof offsetBottom == 'function') offsetBottom = offset.bottom(this.$element)

    var affix = this.getState(scrollHeight, height, offsetTop, offsetBottom)

    if (this.affixed != affix) {
      if (this.unpin != null) this.$element.css('top', '')

      var affixType = 'affix' + (affix ? '-' + affix : '')
      var e         = $.Event(affixType + '.bs.affix')

      this.$element.trigger(e)

      if (e.isDefaultPrevented()) return

      this.affixed = affix
      this.unpin = affix == 'bottom' ? this.getPinnedOffset() : null

      this.$element
        .removeClass(Affix.RESET)
        .addClass(affixType)
        .trigger(affixType.replace('affix', 'affixed') + '.bs.affix')
    }

    if (affix == 'bottom') {
      this.$element.offset({
        top: scrollHeight - height - offsetBottom
      })
    }
  }


  // AFFIX PLUGIN DEFINITION
  // =======================

  function Plugin(option) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.affix')
      var options = typeof option == 'object' && option

      if (!data) $this.data('bs.affix', (data = new Affix(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  var old = $.fn.affix

  $.fn.affix             = Plugin
  $.fn.affix.Constructor = Affix


  // AFFIX NO CONFLICT
  // =================

  $.fn.affix.noConflict = function () {
    $.fn.affix = old
    return this
  }


  // AFFIX DATA-API
  // ==============

  $(window).on('load', function () {
    $('[data-spy="affix"]').each(function () {
      var $spy = $(this)
      var data = $spy.data()

      data.offset = data.offset || {}

      if (data.offsetBottom != null) data.offset.bottom = data.offsetBottom
      if (data.offsetTop    != null) data.offset.top    = data.offsetTop

      Plugin.call($spy, data)
    })
  })
})(jQuery);