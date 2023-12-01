// import "../JS/jquery";




class messageArea{
    static messageAreas= new Map();
    static maxMessageId=0;

    // init function
    constructor(parentElement,cssAttr={},id=1,description=""){
        if(messageArea.messageAreas.get(id) != undefined){
            throw new Error("ID already exists. Cannot create object.");
        }
        if(messageArea.maxMessageId==0){
            id=messageArea.maxMessageId+1;
        }
        if(id>messageArea.maxMessageId){
            messageArea.maxMessageId=id;
        }
        this.msgId=0;
        let initialCss={
            "position":"absolute",
            "z-index":"10",
            "width":"calc(20% + 10px)",
            "height":"max-content",
            "max-height":"30%",
            "top":"10%",
            "left":"calc(80% - 10px - 0.2vw - 1em)",
            "overflow-y":"scroll",
            "transition":" all 0.5s"
        };
        messageArea.messageAreas.set(id,description);
        this.id=id;
        let element=$("<messageArea messageId="+this.id+"></messageArea>");
        element.css(initialCss);
        element.css(cssAttr);
        element.attr("messageId",id);
        $(parentElement).append(element);        
    }
    //sendmessage
    sendMessage(message,liveTime=5,ElementCSS={}){
        this.msgId+=1;
        let $thisId=this.id;
        let msgId=this.msgId;
        let msg=$("<msg msgId="+msgId+" parentId="+this.id+">"+message+"</msg>");
        $("messageArea[messageId="+$thisId+"]").prepend(msg);
        let $msg=$("msg[msgId="+msgId+"][parentId="+$thisId+"]");
        $($msg).css(ElementCSS);
        if(liveTime<=0){
            $($msg).on("click",function(){
                $(this).addClass("remove");
                $(this).on("animationend",function(){
                    $(this).remove();
                });
            });
        }else{
            setTimeout(() => {
                $($msg).addClass("remove");
                $($msg).on("animationend",function(){
                    $(this).remove();
                });
            }, liveTime*1000);
        }      
    }
}
if((self.frameElement) && (self.frameElement.tagName == "IFRAME")){
    function sendMessage(data={},target="*"){
        let default_data={
            message:"",
            liveTime:5,
            ElementCSS:{}
        };
        let result={...default_data,...data};
        window.parent.postMessage(result,target);
    }
}
function listenMessage(target,messageAreaObject){
    $(target).on('message', function(event) {
        let data = event.originalEvent.data;
        let message=data.message;
        let liveTime=data.liveTime;
        let ElementCSS=data.ElementCSS;

        messageAreaObject.sendMessage(
            message=message,
            liveTime=liveTime,
            ElementCSS=ElementCSS
        );
    });
}