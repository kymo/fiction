!function ($) {

    "use strict"; // jshint ;_;


    /* BUTTON PUBLIC CLASS DEFINITION
  * ============================== */
    var Button = function (element, options) {
        this.$element = $(element)
        this.options = $.extend({}, $.fn.button.defaults, options)
    }

    Button.prototype.setState = function (state) {
        var d = 'disabled'
        , $el = this.$element
        , data = $el.data()
        , val = $el.is('input') ? 'val' : 'html'//å¦‚æžœæ˜¯buttonæ ‡ç­¾ï¼Œä½¿ç”¨htmlæ–¹æ³•

        state = state + 'Text'
        //å¦‚æžœæ˜¯resetï¼Œåˆ™å˜æˆresetTextä¿ç•™èµ·æ¥ï¼Œæ¢è¨€ä¹‹resetå¯¹æ¡†æž¶è€Œè¨€æ˜¯ä¸ªä¿ç•™å­—
        data.resetText || $el.data('resetText', $el[val]())
        //åˆ‡æ¢æ–‡æœ¬
        $el[val](data[state] || this.options[state])
        //å¦‚æžœæ˜¯loadingï¼Œé‚£ä¹ˆå®ƒå°±æ·»åŠ ä¸€ä¸ªdisabledç±»åä¸Ždisabledå±žæ€§ï¼Œæ¢è¨€ä¹‹resetå¯¹æ¡†æž¶è€Œè¨€æ˜¯ä¸ªä¿ç•™å­—
        setTimeout(function () {
            state == 'loadingText' ?
            $el.addClass(d).attr(d, d) :
            $el.removeClass(d).removeAttr(d)
        }, 0)
    }
    //è¿™ä¸ªç”¨äºŽæŒ‰é’®ç»„ï¼Œé€šè¿‡$().button('toggle')è°ƒç”¨
    Button.prototype.toggle = function () {
        var $parent = this.$element.closest('[data-toggle="buttons-radio"]')
        //radioå…·æœ‰æŽ’ä»–æ€§ï¼Œåªæœ‰ä¸€ä¸ªæŒ‰é’®ç»„åªæœ‰ä¸€ä¸ªæŒ‰é’®å­˜åœ¨æ¿€æ´»çŠ¶æ€
        $parent && $parent
        .find('.active')
        .removeClass('active')
      
        this.$element.toggleClass('active')
    }


    var old = $.fn.button

    /* BUTTON PLUGIN DEFINITION
  * ======================== */
    $.fn.button = function (option) {
        return this.each(function () {
            var $this = $(this)
            , data = $this.data('button')
            , options = typeof option == 'object' && option
            //é‡å¤åˆ©ç”¨ä¹‹å‰çš„å®žä¾‹
            if (!data) $this.data('button', (data = new Button(this, options)))
            if (option == 'toggle') data.toggle()
            else if (option) data.setState(option)
        })
    }

    $.fn.button.defaults = {
        loadingText: 'loading...'
    }

    $.fn.button.Constructor = Button

    /* BUTTON NO CONFLICT
  * ================== */
    $.fn.button.noConflict = function () {
        $.fn.button = old
        return this
    }

    /* BUTTON DATA-API
  * =============== */
 //ä¸ºå­˜åœ¨data-toggleå±žæ€§ï¼Œå¹¶ä¸”å…¶å€¼ä»¥buttonå¼€å¤´çš„æŒ‰é’®ç»‘å®šç‚¹å‡»äº‹ä»¶
    $(document).on('click.button.data-api', '[data-toggle^=button]', function (e) {
        var $btn = $(e.target)
        if (!$btn.hasClass('btn')) $btn = $btn.closest('.btn')
        $btn.button('toggle')
    })

}(window.jQuery);