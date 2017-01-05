
// add a modal to display article info
function edit_article(url) {
    // 参数url返回一个JSON格式的数据
    // getJSON函数获得JSON数据，并将
    // 表单对应DOM节点的值JSON数据中的值
    $.getJSON(url, function(data) {
        $('#articleId').val(data.id)
        $('#articleTitle').val(data.title);
        // $('#articleUser').val(data.user);
        $('#articleCategory').val(data.category);
        // $('#pubTime').val(data.pub_time);
        // $('#modTime').val(data.mod_time);
        $('#likeNum').val(data.like_num);
        $('#commentsNum').val(data.comments_num);
        // $('#articleBody').val(data.body)
        $('#editArticleInfo').modal('show');
    });
}

$(function() {
    // 将表单的数据全部序列化
    // 此函数将表单转化为JSON的格式
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
    // 修改文章信息的Ajax
    $("#submitArticleInfo").click( function() {
        var form = $("#editArticleForm").serializeObject();
        $.ajax({
            type:'POST',
            datatype:'text',
            // 此处的Ajax操作的是一个表单，url对应为表单的action
            url:$("#editArticleForm").attr('action'),
            data:JSON.stringify(form),
            // 发送请求的数据格式是JSON
            contentType:"application/json; charset=UTF-8",
            success:function(data) {
                // Ajax的请求成功响应后会得到后台返回的JSON数据
                // Ajax通过选择数据对应的DOM位置进行更新
                var id = data.id;
                $("tr#article" + id + "> th.title").html(data.title);
                $("tr#article" + id + "> th.category").html(data.category);
                $('#editArticleInfo').modal('hide');
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
    // 修改分类信息的Ajax
    $("#submitCategoryInfo").click( function() {
        var form = $("#editCategoryForm").serializeObject();
        $.ajax({
            type:'POST',
            datatype:'text',
            // 此处的Ajax操作的是一个表单，url对应为表单的action
            url:$("#editCategoryForm").attr('action'),
            data:JSON.stringify(form),
            // 发送请求的数据格式是JSON
            contentType:"application/json; charset=UTF-8",
            success:function(data) {
                // Ajax的请求成功响应后会得到后台返回的JSON数据
                // Ajax通过选择数据对应的DOM位置进行更新
                var id = data.id;
                $("tr#category" + id + "> th.name").html(data.name);
                $('#editCategoryInfo').modal('hide');
            },
            error: function(error) {
            }
        });
    });
})


// delete an article
function delete_article(id) {
        // 根据删除按钮的单击事件弹出模态框
        $('#delArticle').modal('show');
        // 根据传入的id发送Ajax请求，后台处理删除操作
        $('#cfmDelArticle').click(function() {
            $.ajax({
            type:'GET',
            datatype:'text',
            url:$SCRIPT_ROOT + '/admin/del_article/' + id,
            success: function(data) {
                if (data.success) {
                    $('#delArticle').modal('hide');
                    $("tr#article" + id).remove();
                }
            }
            });
        });       
}

// add a modal to display article info
function edit_category(url) {
    // 参数url返回一个JSON格式的数据
    // getJSON函数获得JSON数据，并将
    // 表单对应DOM节点的值JSON数据中的值
    $.getJSON(url, function(data) {
        $('#categoryId').val(data.id)
        $('#categoryName').val(data.name);
        $('#acticleNum').val(data.articles_num);
        $('#editCategoryInfo').modal('show');
    });
}

// delete a category
function delete_category(id) {
        // 根据删除按钮的单击事件弹出模态框
        $('#delCategory').modal('show');
        // 根据传入的id发送Ajax请求，后台处理删除操作
        $('#cfmDelCategory').click(function() {
            $.ajax({
            type:'GET',
            datatype:'text',
            url:$SCRIPT_ROOT + '/admin/del_category/' + id,
            success: function(data) {
                if (data.success) {
                    $('#delCategory').modal('hide');
                    $("tr#category" + id).remove();
                }
            }
            });
        });       
}