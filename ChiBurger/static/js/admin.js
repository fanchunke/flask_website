
// add a modal to display article info
function edit_article(url) {
    $.getJSON(url, function(data) {
        $('#articleTitle').val(data.title);
        $('#articleCategory').val(data.category);
        $('#pubTime').val(data.pub_time);
        $('#editArticleInfo').modal('show');
    });
}

$(function() {
    $.fn.serializeObject = function() {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
    };
    $("#submitArticleInfo").click( function() {
        alert("test success");
        var form = $("#editArticleForm").serializeObject();
        var test = JSON.stringify(form);
        alert(test);
        $.ajax({
            type:'POST',
            datatype:'text',
            url:$(this).attr('action'),
            data:JSON.stringify(form),
            contentType:"application/json",
            success:function(data) {
            }
        });
    });
})