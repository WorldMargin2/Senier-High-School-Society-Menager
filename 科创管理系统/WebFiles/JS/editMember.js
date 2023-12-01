
if((!self.frameElement) || self.frameElement.tagName != "IFRAME"){
    $('<link rel="stylesheet" href="../CSS/message.css"><link>').appendTo("head");
    var msgArea=new messageArea("body");
    function sendMessage(data){
        let default_data={
            message:"",
            liveTime:5,
            ElementCSS:{}
        };
        let result={...default_data,...data};
        let message=result.message;
        let liveTime=result.liveTime;
        let ElementCSS=result.ElementCSS;
        msgArea.sendMessage(
            message=message,
            liveTime=liveTime,
            ElementCSS=ElementCSS
        );
    }
}


$("input,textarea").on("change input",function(){
    console.log($(this).val());
    $(this).val();
});