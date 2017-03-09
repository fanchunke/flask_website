$(document).ready(function() {

    var profileHeader_info = $('div.profileHeader-info');
    var profileHeader_detail = $('div.profileHeader-detail');

    var expandButton = $('button.Button.ProfileHeader-expandButton');
    expandButton.on('click', function() {
        if (profileHeader_detail.is(":hidden")) {
            $(expandButton).text("收起详细资料");
        } else if (profileHeader_detail.is(":visible")) {
            $(expandButton).text("查看详细资料");
        }
        profileHeader_detail.toggle('fast');
        profileHeader_info.toggle('fast');
           
    });

    // 上传头像
    var useravatar_editor_mask = $('div.Mask.UserAvatarEditor-mask');
    var useravatar_input = $('div.UserAvatar input');
    $('div.UserAvatar').on('mouseenter mouseleave', function(e) {
        if (e.type=='mouseenter') {
            useravatar_editor_mask.removeClass('Mask-hidden');
        } else {
            useravatar_editor_mask.addClass('Mask-hidden');
        }
    });

    useravatar_editor_mask.on('click', function() {
        return useravatar_input.click();
    });

    useravatar_input.on('change', function() {
        var file = $(this).get(0).files[0];
        var limit_size = 2 * 1024 * 1024;
        if ( !file.type.match('image/*')) {
            alert('请上传图片');
            return
        }
        if (file.size > limit_size) {
            alert('图片不能超过2M，请重新上传！');
            return
        }

        // 显示模态框
        var modal = $('div.Modal-wrapper');
        modal.show();

        // 图片预览
        var reader = new FileReader();
        //将文件以Data URL形式读入页面  
        reader.readAsDataURL(file);  
        reader.onload=function(e){ 
            var avatar_container=$("div.UserAvatarEditor-container");  
            //显示文件  
            var img=$('<span><img width="200"  src="' + e.target.result + '" alt="" /></span>'); 
            img.appendTo(avatar_container);
        };
        
        // 关闭模态框
        $('button.Modal-closeButton').on('click', function() {
            modal.hide();
        })

        // ajax提交图片并保存
        $('div.ModalButtonGroup button').on('click', function() {

            $('div.UserAvatar form').ajaxSubmit({
                type:'POST',
                url: $('div.UserAvatar form').attr('action'),
                dataType: 'json',
                success: function(data) {
                    console.log(data);
                    // $('div.UserAvatar img').attr('src', $SCRIPT_ROOT + '/static/img/' + data.filename);
                    $('div.UserAvatar img').attr('src', data.url);
                    modal.hide();
                },
                error: function(xhr, status, error) {
                    alert(status, error);
                }
            });
        });
    });

    // 上传封面
    var usercover_button = $('div.UserCoverEditor button:first');
    var usercover_input = $('div.UserCoverEditor input');

    usercover_button.on('click', function() {
        usercover_input.click();
    });

    usercover_input.on('change', function() {
        // 图片验证
        var file = $(this).get(0).files[0];
        var limit_size = 2 * 1024 * 1024;
        if ( !file.type.match('image/*')) {
            alert('请上传图片');
            return
        }
        if (file.size > limit_size) {
            alert('图片不能超过2M，请重新上传！');
            return
        }

        // 图片预览
        var reader = new FileReader();
        reader.readAsDataURL(file);  
        reader.onload=function(e){ 
            var img = $("div.UserCover img"); 
            img.attr('src', e.target.result);
            $('div.UserCoverEditor-action').show();
        };

        $('div.UserCoverEditor-action button:first').on('click', function() {
            $('div.UserCoverEditor form').ajaxSubmit({
                type: 'POST',
                dataType: 'json',
                url:  $(this).attr('action'),
                success: function(data) {
                    $("div.UserCover img").attr('src', data.url);
                    $('div.UserCoverEditor-action').hide();
                },
                error: function(xhr, status, error) {
                    console(error);
                }
            });
        });

        $('div.UserCoverEditor-action button:last').on('click', function() {
            $('div.UserCoverEditor-action').hide();
        })
    });


    // 修改个人信息
    var profileEditorForm = $("<form id='profileEditorForm' method='post'><div id='profile-editor' class='editormd'></div><div class='ButtonGroup'><button class='Button Button--primary Button--blue' type='button' name='submit'>保存</button><button class='Button' type='button' name='cancle'>取消</button></div></form>");


    $('button#about').on('click', function() {

        $("div.EmptyState").hide();
        $("#profile").append(profileEditorForm);

        profileEditor = editormd("profile-editor", {
            width: '100%',
            height: '600px',
            syncScrolling: "single",
            path   : "/static/editormd/lib/",
            saveHTMLToTextarea : true
        });

        $("#profileEditorForm button:first").on('click', function() {
            var profile_about = $('#profileEditorForm .editormd-html-textarea').text();
            var profile_about_md = $('#profileEditorForm .editormd-markdown-textarea').text();
            console.log(profile_about);
            var data = {'about':profile_about, 'about_md':profile_about_md};
            console.log(data);
            $.ajax({
                type: 'POST',
                dataType: 'json',
                url: $SCRIPT_ROOT + '/profile/' + username + '/edit',
                data: data,
                success: function(data) {
                    console.log(data.data.about);
                    console.log(data)
                    $("#profileEditorForm").remove();
                    var list_item = "<div class='List-item'>" + data.data.about + "</div>"
                    $(profile).append(list_item)
                },
                error: function(xhr, status, error) {
                    console.log(error);
                }
            })  
        });

        $("#profileEditorForm button:last").on('click', function() {
            $("div.EmptyState").show();
            $("#profileEditorForm").remove();  
        });
    });

    $("button#edit-about").on('click', function() {

        $.ajax({
            type: 'GET',
            url: $SCRIPT_ROOT + '/profile/' + username + '/profile-detail',
            dataType: 'json',
            success: function(data) {
                if (data.status=='success') {
                    var profile_about = data.profile.about
                    var profile_about_md = data.profile.about_md;
                    $('div.List-item').hide();
                    $("#profile").append(profileEditorForm);
                    profileEditor = editormd("profile-editor", {
                        width: '100%',
                        height: '600px',
                        syncScrolling: "single",
                        path   : "/static/editormd/lib/",
                        saveHTMLToTextarea : true
                    });
                    $('#profileEditorForm .editormd-markdown-textarea').text(profile_about_md);
                    $('#profileEditorForm .editormd-html-textarea').text(profile_about);

                    $("#profileEditorForm button:first").on('click', function() {
                        var profile_about = $('#profileEditorForm .editormd-html-textarea').text();
                        var profile_about_md = $('#profileEditorForm .editormd-markdown-textarea').text();
                        console.log(profile_about);
                        var data = {'about':profile_about, 'about_md':profile_about_md};
                        console.log(data);
                        $.ajax({
                            type: 'POST',
                            dataType: 'json',
                            url: $SCRIPT_ROOT + '/profile/' + username + '/edit',
                            data: data,
                            success: function(data) {
                                if (data.status=='success') {
                                    $("#profileEditorForm").remove();
                                    $("div.List-item").html(data.data.about);
                                    $("div.List-item").show();
                                };
                            },
                            error: function(xhr, status, error) {
                                console.log(error);
                            }
                        });  
                    });

                    $("#profileEditorForm button:last").on('click', function() {
                        $("div.List-item").show();
                        $("#profileEditorForm").remove();  
                    });
                };
            },

            error: function(xhr, status, error) {
                console.log(error);
            }
        });

    });


    // 发布动态
    $("#submitActivity").on('click', function() {
        
        var activity_empty_state = $("#activity div.EmptyState");
        var activity_item = $('<div class="Activity-item"><div class="activity-content"><div class="activity-user-avatar"><img src=""></div><div class="activity-section"><div class="activity-user-info"></div><div class="activity-text"><p class="comment"></p></div><div class="activity-handle activity-handle-btn"><span class="comment-timestamp"></span></div></div></div></div>');

        $('form#addActivity').ajaxSubmit({
            type: "POST",
            dataType: "json",
            url: $(this).attr("action"),
            success: function(data) {
                if (data.status=='success') {
                    if (activity_empty_state.length > 0) {
                        activity_empty_state.remove();
                        var activity_div = '<div class="Activity-list"></div>';
                        $("#activity").append(activity_div);
                    }
                    var activity_list = $("#activity div.Activity-list");
                    if (!data.user.avatar) {
                        $(activity_item).find('img').attr('src', "$SCRIPT_ROOT + '/static/anonymous.gif'");
                    } else {
                        $(activity_item).find('img').attr('src', data.user.avatar);
                    }
                    if (!data.profile.nickname) {
                        $(activity_item).find('div.activity-user-info').text(data.user.username);
                    } else {
                        $(activity_item).find('div.activity-user-info').text(data.profile.nickname);
                    }
                    activity_item.find('div.activity-text p').html(data.message.body);
                    $(activity_item).find('div.activity-handle span').text(moment(data.message.pub_time).fromNow());

                    $(activity_list).prepend(activity_item);
                    $("#addActivity textarea").val('');
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }

        });
        
    });
});