$(function(){
    $('#user_name').blur(function(){
        check_username($(this))
    })

    $('#pwd').blur(function(){
        check_pwd($(this))
        if ($('#cpwd').val() != ""){
            check_twopwd()
        }
    })

    $('#cpwd').blur(function(){
        if (check_pwd($(this))){
            check_twopwd()
        }
    })

    $("#email").blur(function(){
        check_email($(this));
    })

    $("#reg_form").submit(function(){
        var a = check_username($("#user_name"));
        var b =check_pwd($("#pwd"));
        var c =check_twopwd()
        var d =check_email($("#email"));
        var e = check_allow("#allow");
        if (a && b && c && d && e){
            return true;
        }
        else{
            return false;
        }
    })

    $("#allow").click(function(){
        check_allow($(this));
    })


    function check_username(iobj){
        var nametext = iobj.val();
        var regText = /^(\w){4,12}$/;
        if (regText.test(nametext)){            
            $.ajax({
                url:'/user/register_name_handle/',
                data:{'username':nametext},
                dataType:'JSON',
                type:'POST',
                success:function(data){
                    if (data.res == "0")
                    {
                        iobj.next().html('恭喜你，此名称可以使用').show();
                        return true;
                    }
                    else if(data.res == "1")
                    {
                        iobj.next().html('抱歉，已经注册过的名称,请换一个试试').show();
                        return false;
                    }
                },
                error:function(){
                        iobj.next().html('网络错误,请稍后重试...').show();
                        return false;
                }
            })
        }
        else{
            iobj.next().html('请输入由字母、数字、下划线组成的4到12位的名称').show();
            return false;
        }
    }

    function check_pwd(iobj){
        iobj.next().show();
        var pwdText = iobj.val();
        var regText = /^\w{8,16}$/;
        if (regText.test(pwdText)){
            iobj.next().html('恭喜，你的密码可以使用');
            return true;
        }
        else{
            iobj.next().html('只允许使用数字、字母、下划线的8到16位的密码');
            return false;
        }
    }

    function check_twopwd(){
        var pwd = $("#pwd").val()
        var cpwd = $("#cpwd").val()
        if (cpwd != pwd){
            $("#cpwd").next().html('两次密码不一致').show();
            return false;
        }
        else{
              $("#cpwd").next().hide();
              return true;
        }
    }

    function check_email(iobj){
        var email = iobj.val();
        regText = /^[0-9a-z]{1,10}@[a-z0-9]{1,6}(.[a-z]{2,5}){1,2}$/
        if (regText.test(email)){
            iobj.next().html("恭喜邮箱格式正确");
            return true;
        }
        else{
            iobj.next().html("邮箱格式错误，请正确对待");
            return false;
        }
        iobj.next().show();
    }

    function check_allow(iobj){
        if (iobj.is(':checked')){
            iobj.next().hide();
            return true;
        }
        else{
            iobj.next().html("勾选确认协议");
            iobj.next().show();
            return false;
        }
    }

})