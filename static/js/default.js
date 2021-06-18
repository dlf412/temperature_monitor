$(function () {
    pageInitModule.setWidth();
    pageInitModule.setSidebar();
    pageInitModule.setCarousel();
});
$(window).resize(function () {
    pageInitModule.setWidth();
});
$(window).scroll(function () {
    pageInitModule.setScrollToTop();
});

var pageInitModule = (function (mod) {
    mod.setCarousel = function () {
        try {
            $('.carousel').hammer().on('swipeleft', function () {
                $(this).carousel('next');
            });
            $('.carousel').hammer().on('swiperight', function () {
                $(this).carousel('prev');
            });
        } catch (e) {
            console.log("you mush import hammer.js and jquery.hammer.js to let the carousel can be touched on mobile");
        }
    };
    mod.setWidth = function () {
        if ($(window).width() < 768) {
            $(".sidebar").css({ left: -135 });
            $(".all").css({ marginLeft: 0 });
        } else {
            $(".sidebar").css({ left: 0 });
            $(".all").css({ marginLeft: 135 });
        }
    };
    mod.setScrollToTop = function () {
        var top = $(window).scrollTop();
        if (top < 60) {
            $('#goTop').hide();
        } else {
            $('#goTop').show();
        }
    };
    mod.setSidebar = function () {
        $('[data-target="sidebar"]').click(function () {
            var asideleft = $(".sidebar").offset().left;
            if (asideleft == 0) {
                $(".sidebar").animate({ left: -135 });
                $(".all").animate({ marginLeft: 0 });
            }
            else {
                $(".sidebar").animate({ left: 0 });
                $(".all").animate({ marginLeft: 135 });
            }
        });
        $(".has-sub>a").click(function () {


            $(this).parent().find(".sub-menu").slideToggle();
        })
        var _strcurrenturl = window.location.href.toLowerCase();
    }
    return mod;
})(window.pageInitModule || {});

//控制二级菜单展示隐藏
$('.panel-menu').on('click',function(){
    var id = $(this).attr('id');
    var status = $(this).parent().find('ul').css('display');
    if(status == 'none'){
        sessionStorage.setItem(id,true);
    }else{
        sessionStorage.setItem(id,false);
    }
});

$('.panel-menu').each(function(i,v){
    var key = $(v).attr('id');
    if(sessionStorage.getItem(key)){
        $(v).parent().find('ul').css('display','block');
    }
})
//根据路由加载选中效果
if(location.pathname && location.pathname != '/'){
    var panel_selected = location.pathname.substring(5,location.pathname.length-1);
    if(panel_selected.indexOf('/') == -1){
        $('#'+panel_selected).css({'background-color':'#337AB7','color':'#fff'});
    }
}
