var stop=true; 
  $(function(){
    $("#pList").scroll(function(){ 
        totalheight =  parseFloat($("#pList").scrollTop())+parseFloat($("#pList").height()); 
        if(totalheight>=parseFloat($("#pContainer").height())){
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
  });

  



  function search(){
    if($("#keyword").val()=="")
      $("#keyword").val('杭州');
    window.location = ('/search/'+$("#keyword").val());
  }