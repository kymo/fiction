var cur_page = 1;
var cur_sort ='0';//popular
var style = '0';//all
var total = {{total}};

$(document).ready(
    function()
    {
    var datas = ['1', '2', '22', '4', '5', '6', '7', '8', '9', '10', '12',
        '14', '31', '41', '21', '15'];
    for(var i = 0;i < 16;i ++)
    {
        category_add_click_evt(datas[i]);
    }
    
    get_all_category();
    update_newest_catch();
    $('#by_popular').css('color', 'gray');
    $('#by_popular').css('font-weight', 'bold');
    $('#by_popular').click(
        function()
        {
            if(cur_sort == '1')
            {
    
                $('#by_time').css('color', '#b17750');
                $('#by_time').css('font-weight', '');
                $('#by_popular').css('color', 'gray');
                $('#by_popular').css('font-weight', 'bold');
                $('#loading_gif').css('display', ''); 
                cur_page = 1;
                cur_sort = '0';
                set_content(cur_page, cur_sort, style);
                $('#cur_page').html(cur_page);
                $('#loading_gif').css('display', 'none');
            }
        }
    );
    $('#by_time').click(
        function()
        {
            if(cur_sort == '0')
            {
                $('#by_popular').css('color', '#b17750');
                $('#by_popular').css('font-weight', '');
                $('#by_time').css('color', 'gray');
                $('#by_time').css('font-weight', 'bold');
                $('#loading_gif').css('display', ''); 
                cur_page = 1;
                cur_sort = '1';
                set_content(cur_page, cur_sort, style);
                $('#cur_page').html(cur_page);
                $('#loading_gif').css('display', 'none');
            }

        }
    );
$('#previous_page').click(
    function()
    {
        if(cur_page != 1)
        {
            set_content(cur_page - 1, cur_sort, style);        
            cur_page -= 1;
            $('#cur_page').html(cur_page);
        }
    }
);

$('#next_page').click(
    function()
    {
        if(cur_page != total)
        {
            set_content(cur_page + 1, cur_sort, style);        
            cur_page += 1;
            $('#cur_page').html(cur_page);
        }

    }
);
}
);
function update_newest_catch()
{
    $('#newest_tips').css('display','');
    $('<div>').load(
        '/newest_catch/',
        {'csrfmiddlewaretoken' : '{{csrf_token}}'},
        function()
        {
            var data = $(this).html();
            var content = "";
            var data = eval(data);
            for(var i = 0; data[i] != null; i ++)
            {
                content += "<li style='padding-bottom:0px;margin-bottom:0px;'> " +
                       " <div class=\"top-list\" style='height:auto;width:300px'>" + 
                        "<h2 style='margin-top:0px; margin-bottom:0px;'><a href='/fiction/" + data[i].nid +"/'>" + 
                        data[i].title + "</a><span style='font-size:12px;float:right;'>来自起点中文网</span></h2>" +
                        "<p class=\"top-text\">" + data[i].intro + "</p></div></li>"
            }
            $('#newest_catch').html(content);
            $('#newest_tips').css('display','none');
        }
    );
}
function category_add_click_evt(id)
{
    $('#cate-'+ id).click(
        function()
        {
            if(style != id)
            {
                $('#li-' + style).css('background', '');
                $('#li-' + id).css('background', '#efefef');
                style = '' + id;
              //  cur_sort = '0';
                cur_page = 1;
                set_content(cur_page, cur_sort, style);
                $('#cur_page').html(cur_page);
            }
        }
    );
}
function get_all_category()
{
    $('#category_tips').css('display','');
    $('<div>').load(
    '/get_category_number/',
    {'csrfmiddlewaretoken' : '{{csrf_token}}'},
    function()
    {
    
    var datas = ['1', '2', '22', '4', '5', '6', '7', '8', '9', '10', '12',
        '14', '31', '41', '21', '15'];
    var style = {'1' : '奇幻', '2' : '武侠', '22' : '仙侠', '4' : '都市', '5' : '历史', '6' : '军事', '7' : '游戏', '8' : '竞技',
            '9' : '科幻', '10' : '灵异', '12' : '同人', '14' : '图文', '31' : '文学', '41' : '女生', '21' : '玄幻', '15' :  '青春'}; 
    
    var data = $(this).html();
    var data = eval(data);
    var data = data[0];
    for(var i = 0;i < 16; i ++)
    {
        $('#cate-' + datas[i]).html(style[datas[i]] + "(<span id ='all_" + datas[i] +"'>" + data[datas[i]] + "</span>)");
    }
    $('#category_tips').css('display','none');
    });
}
function set_content(page_index, sort_by, category)
{
     $('<div>').load(
            '/category/',
            {'page_index': String(page_index),
            'sort_by':sort_by,
            'category' : category,
            'from' : 'ajax',
            'csrfmiddlewaretoken' : '{{csrf_token}}'},
            function()
            {
                var data = eval($(this).html());
                var content = "";
                var start = 0;
                if(category != '0')
                {
                    total = parseInt($('#all_' + category).html());

                    $('#total_number').html('共' + (parseInt((total - 1) / 10) + 1) + '页');
                    total = parseInt((total - 1) / 10 + 1);
                }
                for(var i = 0;data[i] != null; i ++)
                {
                    content += "<li>" + 
                       " <div class=\"book-intro\">" + 
                         "   <div class=\"cover\"><a href=\"" + "/fiction/" + data[i].nid + "/" + "\"><img src=\"" + 
                         data[i].avatar_url + "\" alt=\"\"></a></div><div class=\"book-meta cate\">" + 
                         "<div class=\"book-title\"><a href=\" " + "/fiction/" + data[i].nid + "/" + "\"> " +
                         data[i].title + "</a></div><p ><span class=\"label\">作者：</span><span class=\"lable-text\"> " +
                         data[i].author + "</span><span class=\"label\">分类：</span><span class=\"lable-text\">" + 
                         "<a href='/category?category=" + data[i].style_id+ "'>" + data[i].style + "</a></span><span class=\"label\">" +
                         "评分：</span><span class=\"lable-text\">" + data[i].score + "</span></p><div class=\"info\">" + 
                         "<p>" + data[i].intros + "</p></div></div></div></li>";
                }
                $('#show_content').html(content);
            });

}

