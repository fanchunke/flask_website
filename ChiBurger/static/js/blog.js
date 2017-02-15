$(function() {
    // 添加评论的Ajax
    $("#submitComment").click( function() {
        var data = $('#addComment').serialize()
        $.ajax({
            type:'POST',
            datatype:'json',
            // 此处的Ajax操作的是一个表单，url对应为表单的action
            url:$("#addComment").attr('action'),
            data:data,
            success:function(data) {
                // Ajax的请求成功响应后会得到后台返回的JSON数据
                // Ajax通过选择数据对应的DOM位置进行更新
                $("textarea.comments").val("");
                var comment_item = $('<div />', {
                    id:"comment-" + data.id,
                    class:"comment-item"
                });
                var comment_content = $('<div />', {
                    class:"comment-content"
                }).appendTo(comment_item);
                var comment_user_avatar = $('<div />', {
                    class:"comment-user-avatar"
                }).appendTo(comment_content);
                var user_img = $('<img />', {
                    src: $SCRIPT_ROOT + '/static/anonymous.gif'
                }).appendTo(comment_user_avatar);
                var comment_section = $('<div />', {
                    class:"comment-section"
                }).appendTo(comment_content);
                var comment_user_info = $('<div />', {
                    class:"comment-user-info"
                }).appendTo(comment_section);
                var user_info = $('<span />', {
                    text:"来自 " + data.user_ip + " 的网友 (" + data.user_platform + "/" + data.user_browser + ")"
                }).appendTo(comment_user_info);
                var comment_text = $('<div />', {
                    class:"comment-text"
                }).appendTo(comment_section);
                var comment_handle = $('<div />', {
                    class:"comment-handle comment-handle-btn"
                }).appendTo(comment_section);
                var body = $('<p />', {
                    class:"comment",
                    text:data.body
                }).appendTo(comment_text);
                var  pub_time = $('<span />', {
                    class:"comment-timestamp",
                    // text:data.pub_time
                    text:moment(data.pub_time).fromNow()
                }).appendTo(comment_handle);
                var comment_list_body = $('<div />', {
                    class:"comment-list-body"
                });
                var p_element = $('p.comment.no-comment');
                if (p_element.length>0) {
                    p_element.remove();
                    $("div.comment-area-list").prepend(comment_list_body);
                    comment_list_body.prepend(comment_item);
                } else {
                    $("div.comment-list-body").prepend(comment_item);
                };
                $("#allCommentNum").text("(" + data.comment_num + ")");
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
})