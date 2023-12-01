$(".topTab").on("click",function(){
    url=$(this).attr("href");
    title=$(this).attr("title");
    $("#mainFrame")[0].src=url;
    $("#mainFrame")[0].title=title;
    $(".selectedTab").removeClass("selectedTab");
    $(this).addClass("selectedTab")
});

if (self.frameElement && self.frameElement.tagName == "IFRAME"){
    top.window.location.reload(); 
}