
var index = [0,0,0,0];
$(document).ready(
    function()
    {
        $('#input01').focus(
            function()
            {
                $('#input01-tip').css('display','none');
            }
        );
        $('#input02').focus(
            function()
            {
               // alert('#input02-tip');
                $('#input02-tip').css('display','none');
            }
        );
        $('#input03').focus(
            function()
            {
                //alert('#input03-tip');
                $('#input03-tip').css('display','none');
            }
        );
        $('#input04').click(
            function()
            {
                if($('#input_ok').attr("checked") == "checked")
                {
                    index[3] = 1;
                }
                else
                {
                    index[3] = 0;
                }
                
            }
        );
        $('#submit-button').click(
            function()
            {
                var tag = false;
                for(var j = 0; j <= 3 ;j ++)
                {
                    if(index[j] == 0)
                    {
                        $('#input0' + (j + 1)).css('border', '1px solid red');
                        $('#show_alert').css('display', '');
                        tag = true;
                    }
                }
                if(! tag)
                    $('#reg-form').submit(); 
            }
        );
        $('#input01').blur(
            function()
            {
                //check user id
                if($('#input01').val() == "")
                {
                    $('#input01-tip').css('display', '');
                    $('#input01-tip').css('color' ,'green');
                    $('#input01-tip').html('用户名不可为空');
                    index[0] = 0;

                }
                else
                {
                $('<div>').load(
                    '/check_id/',
                    {'name' : $('#input01').val(),
                    'csrfmiddlewaretoken' : '{{csrf_token}}'},
                    function()
                    {
                        //#无此用户
                        if($(this).html() == 'NO')
                        {
                            //alert('no');
                            $('#input01-tip').css('display', '');
                            $('#input01-tip').css('color' ,'green');
                            $('#input01-tip').html('此ID可以使用');
                            index[0] = 1;
                        }
                        else if($(this).html() == 'YES')
                        {
                            index[0] = 0;
                            $('#input01-tip').css('display', '');
                            $('#input01-tip').css('color', 'red');
                            $('#input01-tip').html('已注册.');
                        }
                    }
                );
                }
            }
        );
        $('#input02').blur(
            function()
            {
                var password = $('#input02').val();
                if(password.length < 6 || password.length > 20)
                {
                    index[1] = 0;
                    $('#input02-tip').css('display', '');
                    $('#input02-tip').css('color', 'red');
                    $('#input02-tip').html('密码长度6-20位哦.');
                }
                else
                {
                    index[1] = 1;
                    var security_note = password.length / 20.0;
                    $('#input02-tip').css('display', '');
                    if(security_note < 0.4)
                        $('#input02-tip').css('color', '#f03c42');
                    else if(security_note < 0.6)
                        $('#input02-tip').css('color', '#ef611d');
                    else if(security_note < 0.8)
                        $('#input02-tip').css('color', 'blue');
                    else
                        $('#input02-tip').css('color', 'green');
                   $('#input02-tip').html('安全指数' + String(security_note)); 
                }
            }
        );
        $('#input03').blur(
            function()
            {
                var password1 = $('#input02').val();
                var password2 = $('#input03').val();
                if(password1 == password2)
                {
                    index[2] = 1;
                    $('#input03-tip').css('display', '');
                    $('#input03-tip').css('color', 'blue');
                    $('#input03-tip').html('密码正确');
                    
                }
                else
                {
                    index[2] = 0;
                    $('#input03-tip').css('display', '');
                    $('#input03-tip').css('color', 'red');
                    $('#input03-tip').html('密码不匹配哦');
                }

            }
        );
        /*
        $('#input04').blur(
            function()
            {
                $('<div>').load(
                '/check_email/',
                {'csrfmiddlewaretoken' : '{{ csrf_token }}',
                'email' : $('#input04').val()},
                function()
                {
                    if($(this).html() == 'NO')
                    {
                            
                        index[3] = 1;
                        $('#input03-tip').css('display', '');
                        $('#input03-tip').css('color', 'blue');
                        $('#input03-tip').html('');
                    }
                    else
                    {
                        index[3] = 0;
                        $('#input03-tip').css('display', '');
                        $('#input03-tip').css('color', 'red');
                        $('#input03-tip').html('此邮箱');
                    }
                });
            }
        );
        */
    }
);
