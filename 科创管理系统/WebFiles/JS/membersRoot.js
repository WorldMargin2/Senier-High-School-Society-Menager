
function init(){
$(".PageChanger").on("click",function(){
    $(".url-select").removeClass("url-select");
    $(this).addClass("url-select");
    $("#PageFrame")[0].src=$(this).attr("url");
});

$(".PageChangers").dblclick(function () {
    $(this).css("transition","all 0.5s");
    $(this).css("position","absolute");
    $(this).css("top",0);
    $(this).css("left",0);
});


function drag(object){
    $(object).on("mousedown",function(event){
        if(event.which!=1){
            return(false);
        }
        $(this).css("transition","none");
        var ElementSelf=$(this);
        var ElementParent=ElementSelf.parent();
        ElementSelf.css('position', 'absolute');
        var x=event.clientX,y=event.clientY;

        $(document).on("mousemove",function(event){
            cursorX=event.clientX;
            cursorY=event.clientY;
            ElementSelf.css('left', '+=' + (cursorX - x));
            ElementSelf.css('top', '+=' + (cursorY - y));
            x=cursorX;
            y=cursorY;
            return(false);
        });

        $(document).on("mouseup",function(){
            selfWidth = ElementSelf.width();
            selfHeight = ElementSelf.height();
            parentWidth = ElementParent.width();
            parentHeight = ElementParent.height();
            position = ElementSelf.position();
            selfLeft = position.left;
            selfTop = position.top;

            selfPaddingR=2*parseInt(ElementSelf.css("padding-right"));
            selfPaddingB=2*parseInt(ElementSelf.css("padding-bottom"));
            selfBorder  =2*parseInt(ElementSelf.css("border"));

            if(selfLeft<0){
                ElementSelf.css('left',0);
            }
            if(selfTop<0){
                ElementSelf.css('top',0);
            }
            if((selfTop+selfHeight)>parentHeight){
                ElementSelf.css('top',(parentHeight-(selfHeight+selfPaddingB+selfBorder)));
            }
            if((selfLeft+selfWidth+selfPaddingR+selfBorder)>parentWidth){
                ElementSelf.css('left',(parentWidth-(selfWidth+selfPaddingR+selfBorder)));
            }
            $(document).off("mousemove");
        });
    });
}



drag(".PageChangers");




}