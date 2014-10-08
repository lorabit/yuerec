var stop=true; 
var msnry;
  $(function(){
    $(window).scroll(function(){ 

        totalheight =  parseFloat($(window).scrollTop())+parseFloat($("body").height()); 
        if(totalheight>=parseFloat($(document).height())){
            if(stop==true){
              stop = false;
              loadMore();
            }
        }
        return true;
    });

    $("#pList").on("click",".pItem img",function(){
      $($(this).parent()).css("height","auto");
    });

    $("#pList").on("click",".glyphicon-user",function(){
        uid = $(this).parent().parent().data("uid");
        window.open('http://www.douban.com/group/people/'+uid);
    });

    $("#pList").on("click",".glyphicon-link",function(){
        tid = $(this).parent().parent().data("tid");
        window.open('http://www.douban.com/group/topic/'+tid);
    });


    $("#pList").on("click",".glyphicon-trash",function(){
        pid = $(this).parent().parent().data("pid");
        $(this).parent().parent().hide();
        $.ajax({
          url:'/photo/'+pid+"/delete",
          success:function(){
            $("#pList").masonry('remove',  $(this).parent().parent());
             $("#pList").masonry('layout');
          }
        });
    });

    $("#pList").imagesLoaded(function(){
      // msnry = new Masonry( "#pList",{
      //   itemSelector : '.pItem'
      // } );
      $("#pList").masonry({itemSelector : '.pItem'});
    });

    
  });
  $(document).ready(function(){


  });

  



  function search(){
    if($("#keyword").val()=="")
      $("#keyword").val('杭州');
    window.location = ('/search/'+$("#keyword").val());
  }