var cur_id = '0';
var rec_content = "";
var click_content = "";

function clean_log()
{
    //delete cookie
    $.cookie('read_log', null);
    //clean are
    //
    $('#show_hisotry').css('background', '#eee');
    $('#show_history').html('');
}

function show_history(token, frm)
{
    $('#loading_gif').fadeOut(200);
   var content = "";
   var cookies = $.cookie('read_log');
    var fiction_name = "";
    $('<div>').load(
        '/get_fiction_and_newest_chapter/',
        {'csrfmiddlewaretoken' : token,
        'data' : cookies},
        function()
        {

            var data = $(this).html();
            datas = eval(data);
            var total = "";
            if(datas[0] != null && data != 'error')
            {
                if(frm == 'index')
                    total = "<h2><div style='border-bottom:0px solid #b17750;width:90%;font-weight:bold;font-family:微软雅黑;'>临时书架<a style='margin-left:10px;font-size:12px;' href='javascript:void(0);' onclick='clean_log();'>清空书架</a></div> </h2>";
                $('#history_div').css('border-bottom', '1px solid #ddd');
            
            for(var j = 0;datas[j] != null; j ++)
            { 
                           
                var content = "<tr>";
                if(datas[j].chapter_title == '')
                {
                    content += '<td><span class="inside_table">' + datas[j].time + ': <a href = "/fiction/' + 
                    datas[j].fiction_nid + '">' + datas[j].fiction_title + '</a> 最新章节: ' + datas[j].fiction_chapter;
                    
                }
                else
                {
                    content += '<td><span class="inside_table">' + datas[j].time + ': <a href = "/fiction/' + 
                    datas[j].fiction_nid + '">' + datas[j].fiction_title + '</a> 阅读到 <a href = "' + datas[j].url + '">' + datas[j].chapter_title.substr(0,10) + '..</a>';
                }
                content += '</td></span>';
                j += 1;
                if(datas[j] == null)
                {
                    content += '</tr>';
                    $('#show_history').append(content);
                    total += content;
                    break;
                }
                if(datas[j].chapter_title == '')
                {
                    content += '<td><span class="inside_table">' + datas[j].time + ': <a href = "/fiction/' + 
                    datas[j].fiction_nid + '">' + datas[j].fiction_title + '</a> 最新章节: ' + datas[j].fiction_chapter;
                }
                else
                {
                    content += '<td><span class="inside_table">' + datas[j].time + ': <a href = "/fiction/' + 
                    datas[j].fiction_nid + '">' + datas[j].fiction_title + '</a> 阅读到 <a href = "' + datas[j].url + '">' + datas[j].chapter_title.substr(0,10) + '..</a>';
                }
                content += '</td></span>';
                content += "</tr>";
                total += content;
                    //$('#loading_gif').css('display', 'none');
                    //$('#show_history').append(content);
                }
                $('#show_history').css('display', 'none');
                $('#show_history').html("<table style='table-layout:fixed;'>" + total + "</table>");
                $('#show_history').fadeIn(400);
                }
         });
        }

    function chapter_character(url,_nid, nid, token)
    {
        //save cookie
        save_read_log(url, _nid, nid);
        $('<div>').load(
        '/add_click_time_chapter/',
        {'nid' : _nid,
        'csrfmiddlewaretoken' :token},
        function()
        {
        }
        );
    }


    Date.prototype.format = function(format) {  
        /* 
         * eg:format="yyyy-MM-dd hh:mm:ss"; 
         */  
        var o = {  
            "M+" : this.getMonth() + 1, // month  
            "d+" : this.getDate(), // day  
            "h+" : this.getHours(), // hour  
            "m+" : this.getMinutes(), // minute  
            "s+" : this.getSeconds(), // second  
            "q+" : Math.floor((this.getMonth() + 3) / 3), // quarter  
            "S" : this.getMilliseconds()  
            // millisecond  
        }  
      
        if (/(y+)/.test(format)) {  
            format = format.replace(RegExp.$1, (this.getFullYear() + "").substr(4  
                            - RegExp.$1.length));  
        }  
      
        for (var k in o) {  
            if (new RegExp("(" + k + ")").test(format)) {  
                format = format.replace(RegExp.$1, RegExp.$1.length == 1  
                                ? o[k]  
                                : ("00" + o[k]).substr(("" + o[k]).length));  
            }  
        }  
        return format;  
    }  

    function character(url, nid, _nid, token)
    {
        save_read_log(url, nid, _nid);
        $('<div>').load(
        '/add_click_time_fiction/',
        {'nid' : _nid,
        'csrfmiddlewaretoken' :token},
        function()
        {
            
        }
        );
    }

    function save_read_log(url, chapter_id, fiction_nid)
    {
        var read_log = $.cookie('read_log');
        var time = new Date().format("yyyy-MM-dd hh:mm:ss");
        if(read_log == null)
        {
            new_read_log = '{"tag":"1","chapter_id":"' + chapter_id + 	'","fiction_nid":"' + fiction_nid + '","url":"' + url +'","time":"' + time + '"}';
            $.cookie('read_log', new_read_log, {'expires' : 7, 'path' : '/'});
        }
        else
        {
            var is_change = false;
            var logs = eval('[' + $.cookie('read_log') + ']');
            var new_log = "";
            
            for(var j = 0; logs[j] != null; j ++)
            {
                if(fiction_nid == logs[j].fiction_nid)
                {
                    new_log += '{"tag":"1","chapter_id":"' + chapter_id + '","fiction_nid":"' + fiction_nid + '","url":"' + url + '","time":"' + time + '"}';
                    is_change = true;
                }
                else
                {
                    new_log += '{"tag":"1","chapter_id":"' + logs[j].chapter_id + '","fiction_nid":"' + logs[j].fiction_nid + '","url":"' + logs[j].url + '","time":"' + logs[j].time + '"}';
                }
                if(logs[j + 1] != null)
                    new_log += ',';
            }
            if(! is_change)
            {
                new_log += ',';
                new_log += '{"tag":"1","chapter_id":"' + chapter_id + '","fiction_nid":"' + fiction_nid + '","url":"'+ url +'","time":"' + time + '"}';
            }
            $.cookie('read_log', new_log, {'expires' : 7, 'path' : '/'});
        }
    }

    function load_list(csrf_token, type_code, url, div_id)
    {
            $('<div>').load(
                url,
                {'csrfmiddlewaretoken' : csrf_token,
                'type' : type_code},
                function()
                {
                    var content = "";
                    var data = eval($(this).html());
                    if(data[0] == null)
                    {
                        $('#show_rec_ranking').html("暂无.");
                        return;
                    }
                        content += "<li style=''><div class='cover' style='float:left;width:50px;padding:5px;background:#e0e0e0;'><a href=\"/fiction/"+ data[0]['nid'] + "\"><img style='width:50px;height:60px;' src='" + data[0]['avatar'] + 
                        "' alt=''></a></div><div class='top-list'style='float:left;width:auto;height:auto;'><h2 style='font-size:13px;line-height:10px;'><span style='font-size:14px;' class='nub'>" + 
                        (1) + ". </span><a href='/fiction/"+ data[0]['nid'] + "'>"+ data[0]['title'] +
                        "</a></h2><p class='top-text'>"+ 
                        data[0]['intro'] +"<a href='/fiction/"+ data[0]['nid'] + "'>......</a>" +
                          
                        "<span style='font-size:12px;font-weight:bold;color:#555;'>" + data[0]['author'] + "著</span>" + 
                        "<span style = 'margin-right:5px;font-size:12px;color:#555;'>收录于" + data[0]['source'] + "</span></p></div></li>"
                  
                    for(var i = 1; data[i] != null; i ++)
                    {
                        content += "<li style='height:auto;'><div class='top-list' style='height:auto;width:auto'><font style='font-size:13px;line-height:10px;'><span style='font-size:14px;' class='nub'>" + 
                    (i + 1) + ". </span><a href='/fiction/"+ data[i]['nid'] +"'>"+ data[i]['title'] +
                    "</a></font><font style='margin:0px 0px 0px 0px;margin-left:4px;'class='top-text'>"+ 
                    data[i]['intro'] +"<a href='/fiction/"+ data[i]['nid'] + "'>....</a></font>" + 
                    
                    "<span style='font-weight:bold;font-size:12px;color:#555;'>" + data[i]['author'] + "著</span>" + 
                    "<span style = 'margin-right:5px;font-size:12px;color:#555;'>收录于"+ data[i]['source'] +"</span></div></li>";
                    }
                $('#show_rec_ranking').html(content);
            }
        );
}
function change_content_show(id, type_code, token)
{
   if(id != cur_id)
    {
        $('#show_rec_ranking').html("<div style = 'padding:20px;font-family:微软雅黑,黑体;'><img src = '/site_media/image/loading.gif'></div>") 
        $('#menu_' + cur_id).css('border-bottom', '0px');
        $('#menu_' + id).css('border-bottom', '2px solid #b17750');
        $('#menu_' + cur_id + ' a').css('color', '#000');
        $('#menu_' + id + ' a').css('color', '#b17750');
        cur_id = id;
        load_list(token, type_code, '/type_ranking_list/', '#show_rec_ranking');
   }
}
