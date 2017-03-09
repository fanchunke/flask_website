
// 鼠标悬停时显示修改按钮
$(document).ready(function() {
    var form_field = $("form.Field");
    form_field.each(function() {
        $(this).on('mouseenter mouseleave', function(event) {
            var field = $(this);
            var modify_button = $(field).find("button.ModifyButton");
            var modify_label = $(field).find(".Field-label").text();
            if (event.type=='mouseenter') {
                modify_button.removeClass("Field-modify-hidden");
                modify_button.one('click', function() {
                    editProfile(field, modify_label);
                });
            } else {
                modify_button.addClass("Field-modify-hidden");
            }
        });
    });
    
});

// 修改个人信息的入口函数
function editProfile(field, item) {
    if (item=="居住地") {
        editAddress(field);
    } else if (item=='性别') {
        editGender(field);
    } else if (item=='个人简介') {
        editDiscription(field);
    } else if (item=='昵称') {
        editNickname(field);
    }
};

// 修改昵称
function editNickname(field) {
    var field_content = $(field).find(".Field-content");
    var field_content_children = field_content.children();
    var item_data = field_content.find('.Field-text').text();
    field_content.empty();
    var new_field = $("<div><div class='Field-autoComplete'><div class='Popover'><div class='Field-input Input-wrapper'><input value='' class='Input' placeholder='填写昵称'></div></div></div><div class='ButtonGroup ButtonGroup--right'><button class='Button Button--primary Button--blue' type='button'>保存</button><button class='Button' type='button'>取消</button></div></div>");
    new_field.find('input').text(item_data);
    new_field.appendTo(field_content);

    var submit_button = $(new_field).find("button:first");
    submit_button.on('click', function() {
        var new_item_data = $(new_field).find('input').text();
        var data = {"nickname": new_item_data};
        $.ajax({
            type: 'POST',
            datatype: 'json',
            data: data,
            url: $SCRIPT_ROOT + '/profile/' + username + '/edit',
            success: function(data) {
                if (data.status=='success') {
                    field_content.empty();
                    item_data = data.nickname;
                    field_content_children.appendTo(field_content); 
                }
            },
            error: function(xhr, status, error) {
                console.log(xhr.status);
            }
        });
    });

    var cancle_button = new_field.find("button:last");
    cancle_button.on('click', function() {
        field_content.empty();
        field_content_children.appendTo(field_content);
    });
};


// 修改居住地
function editAddress(field) {
    var field_content = $(field).find(".Field-content");
    var field_content_children = field_content.children();
    var item_data = field_content.find('.Field-text').text();
    field_content.empty();
    var new_field = $("<div><div class='Field-autoComplete'><div class='Popover'><div class='Field-input Input-wrapper'><input value='' class='Input' placeholder='添加居住地'></div></div></div><div class='ButtonGroup ButtonGroup--right'><button class='Button Button--primary Button--blue' type='button'>保存</button><button class='Button' type='button'>取消</button></div></div>");
    new_field.find('input').text(item_data);
    new_field.appendTo(field_content);

    var submit_button = $(new_field).find("button:first");
    submit_button.on('click', function() {
        var new_item_data = $(new_field).find('input').text();
        var data = {"address": new_item_data};
        $.ajax({
            type: 'POST',
            datatype: 'json',
            data: data,
            url: $SCRIPT_ROOT + '/profile/admin/edit',
            success: function(data) {
                if (data.status=='success') {
                    field_content.empty();
                    item_data = data.address;
                    field_content_children.appendTo(field_content); 
                }
            },
            error: function(xhr, status, error) {
                console.log(xhr.status);
            }
        });
    });

    var cancle_button = new_field.find("button:last");
    cancle_button.on('click', function() {
        field_content.empty();
        field_content_children.appendTo(field_content);
    });
};


// 修改性别
function editGender(field) {
    var field_content = $(field).find(".Field-content");
    var field_content_children = field_content.children();
    var item_data = field_content.find('.Field-text').text();
    field_content.empty();
    var new_field = $("<div><input type='radio' value='0' name='gender' />男<input type='radio' value='1' name='gender' style='margin-left: 30px;' />女<div class='ButtonGroup'><button class='Button Button--primary Button--blue' type='button'>保存</button><button class='Button' type='button'>取消</button></div></div>");
    new_field.find('input').text(item_data);
    new_field.appendTo(field_content);

    // 单击单选框时改变checked状态
    var radio1 = $(new_field).find("input[name='gender']")[0];
    $(radio1).val("男");
    var radio2 = $(new_field).find("input[name='gender']")[1];
    $(radio2).val("女");
    $(radio1).on('click', function() {
        $(this).attr("checked",true);
        $(radio2).attr("checked",false);
    });
    $(radio2).on('click', function() {
        $(this).attr("checked",true);
        $(radio1).attr("checked",false);
    })
   
    $("input[name='gender'][value='男']").attr("checked",'checked')

    var submit_button = $(new_field).find("button:first");
    submit_button.on('click', function() {
        var new_item_data = $(new_field).find('input[name="gender"]:checked').text();
        var data = {"gender": new_item_data};
        $.ajax({
            type: 'POST',
            datatype: 'json',
            data: data,
            url: $SCRIPT_ROOT + '/profile/admin/edit',
            success: function(data) {
                if (data.status=='success') {
                    field_content.empty();
                    item_data = data.gender;
                    field_content_children.appendTo(field_content); 
                }
            },
            error: function(xhr, status, error) {
                console.log(xhr.status);
            }
        });
    });

    var cancle_button = new_field.find("button:last");
    cancle_button.on('click', function() {
        field_content.empty();
        field_content_children.appendTo(field_content);
    });
};


// 修改个人简介
function editDiscription(field) {
    var field_content = $(field).find(".Field-content");
    var field_content_children = field_content.children();
    var item_data = field_content.find('.Field-text').text();
    field_content.empty();
    var new_field = $("<div><textarea rows='3' class='DescriptionField-input TextArea' placeholder='请输入个人简介'></textarea><div class='DescriptionField-actions'><div class='ButtonGroup DescriptionField-buttonGroup'><button class='Button Button--primary Button--blue' type='button'>保存</button><button class='Button' type='button'>取消</button></div><span class='MaxLength'></span></div></div>");
    new_field.find('textarea').text(item_data);
    new_field.appendTo(field_content);

    var submit_button = $(new_field).find("button:first");
    submit_button.on('click', function() {
        var new_item_data = $(new_field).find('textarea').text();
        var data = {"discription": new_item_data};
        $.ajax({
            type: 'POST',
            datatype: 'json',
            data: data,
            url: $SCRIPT_ROOT + '/profile/admin/edit',
            success: function(data) {
                if (data.status=='success') {
                    field_content.empty();
                    item_data = data.discription;
                    field_content_children.appendTo(field_content); 
                }
            },
            error: function(xhr, status, error) {
                console.log(xhr.status);
            }
        });
    });

    var cancle_button = new_field.find("button:last");
    cancle_button.on('click', function() {
        field_content.empty();
        field_content_children.appendTo(field_content);
    });
};