//import "jquery";

function is_inArray(array=[],object){
    if(array.indexOf(object)!=-1){
        return(true);
    }
    return(false);
}

let deleteMembersList = [];
let test = true;
let returnFalse=true;


$(".del").on("click",function(){
    parentS=$(this).closest("tr")
    userid=parentS.attr("id");
    userid=parseInt(userid);
    if(is_inArray(deleteMembersList,userid)){
        sendMessage({
            message:"请等待服务器处理 编号："+userid,
            liveTime:2,
            ElementCSS:{"color":"red"}
        });
        return 0;
    }else{
        deleteMembersList.push(userid);
        parentS.css("filter","blur(5px)");
    }
    $.ajax({
        url: "/deleteMember",
        data: { userid : userid ,test : test , returnFalse : returnFalse},
        type: "POST",
        success: function (data) {
            if(data.stat){
                deleteMembersList.pop(userid);
                parentS.css("opcity","0");
                setTimeout(function(){
                    parentS.remove();
                },500);
            }else{
                sendMessage({
                    message:"请刷新页面后重试 编号："+userid,
                    liveTime:2,
                    ElementCSS:{"color":"red"}
                });
                
                parentS.css("filter","none");
                deleteMembersList.pop(userid);
            }
        },
        error:function(){
            parentS.css("filter","none");
            deleteMembersList.pop(userid);
        }
    });
});

$(".config").on("click",function(){
    let userid=$(this).closest("tr").attr("id");
    location.href="/Members/edit/"+userid;
});

