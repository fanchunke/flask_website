// add a modal to display article info
function edit_article(url) {
    $.getJSON(url, function(data) {
        // alert("Json data:" + data.title);
        // $('#articleTitle').val(data.title);
        // $('#articleCategory').val(data.category);
        // $('#pubTime').val(data.pub_time);
        // alert("success");
        $('#editArticleInfo').modal('show');
    });
}