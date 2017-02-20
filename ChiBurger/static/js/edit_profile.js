$(function () {
    $("#editGender").click( function() {
    });
    $("#editAddress").click( function() {
        var span_element = $("#address");
        if (span_element.length > 0 ) {
            var old_address = $("#address").text();
            $("#address").remove();
        } else {
            var old_address="";
        }
        $("#editAddress").remove();
        var field_input = $("<div />", {
            id:"input",
            class:"HeadlineField-input Input-wrapper"
        }).appendTo("div.address");
        var input = $("<input />", {
            class:"Input",
            value:old_address,
        }).appendTo(field_input);
        var actions = "<div id='actions' class='HeadlineField-actions'><div class='ButtonGroup HeadlineField-buttonGroup'><button class='Button editProfile' type='button'>保存</button><button class='Button cancle' type='button'>取消</button></div></div>"
        $("div.address").append(actions);
        $("div.address button.cancle").click(function() {
            $("#input").remove();
            $("#actions").remove();
            var new_address = $("<span />", {
                id: "address",
                class:"Field-text",
                text:old_address
            });
            $("div.address").append(new_address);
            var edit_button = "<button id='editAddress' class='Button ModifyButton Field-modify Field-modify-hidden Button--link' type='button'>修改</button>"
            $("div.address").append(edit_button);
        })
        $("div.address button.editProfile").click(function() {
            var data = {};
            var address = $("div.address input.Input").val();
            data['address'] = address;
            console.log(data);
            console.log(user_id);
            $.ajax({
                type:'POST',
                datatype:'json',
                url:$SCRIPT_ROOT + '/profile/edit-profile/' + user_id,
                data:data,
                success: function(data) {
                    console.log(data);
                    console.log(data.address);
                    var new_address = $("<span />", {
                        id: "address",
                        class:"Field-text",
                        text:data.address
                    });
                    $('div.address').append(new_address);
                    var button = "<button id='editAddress' class='Button ModifyButton Field-modify Field-modify-hidden Button--link' type='button'>修改</button>";
                    $('div.address').append(button);
                    $("#input").remove();
                    $("#actions").remove();
                },
                error: function(error) {
                console.log(error);
                }
            });
        });     

    });
})