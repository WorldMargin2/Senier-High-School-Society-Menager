// import "../JS/clipboard"
$(".search>.searchInput,.search>.searchSelect").on("input change", function () {
    let text = $(".search .searchInput").val();
    let tp = $(".search .searchselect").val();
    $("table tbody tr").hide();
    $("table tbody tr td" + "[tp='" + tp + "']")
        .filter(":contains('" + text + "')")
        .closest("tr").show();
});

function copyTextFunction() {
    let copyText = "";
    // 筛选数据
    $("tbody tr td[tp='" + $(".search .searchselect").val() + "']")
        .filter(":contains('" + $(".search .searchInput").val() + "')")
        .each(function () {
            $(this)
                .closest("tr")
                .children("td:not([tp='controler'])")
                .each(function () {
                    copyText += $(this).text();
                    copyText += "\t";
                });
            copyText += "\n";
        });
    // 操作剪切板
    let clipboard = new ClipboardJS('.copybtn', {
        text: function () {
            return (copyText);
        }
    });
    clipboard.on("success", function () {
        clipboard.destroy();
    });
    sendMessage({
        message: "复制成功！",
        liveTime: 2,
        elementCSS: {}
    });
}

$(".search .copybtn").on("click", copyTextFunction);