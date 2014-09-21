!function ($) {

    "use strict"; // jshint ;_;


    /* MODAL CLASS DEFINITION
  * ====================== */

    var Modal = function (element, options) {
        this.options = options
        this.$element = $(element) //ç»‘å®šå…³é—­äº‹ä»¶ï¼Œå…³é—­æŒ‰é’®è¦æ±‚æœ‰[data-dismiss="modal"]å±žæ€§
        .delegate('[data-dismiss="modal"]', 'click.dismiss.modal', $.proxy(this.hide, this))
        this.options.remote && this.$element.find('.modal-body').load(this.options.remote)
    }

    Modal.prototype = {

        constructor: Modal

        , 
        toggle: function () {
            return this[!this.isShown ? 'show' : 'hide']()
        }

        , 
        show: function () {
            var that = this
            , e = $.Event('show')
            //è§¦å‘showäº‹ä»¶
            this.$element.trigger(e)

            if (this.isShown || e.isDefaultPrevented()) return

            this.isShown = true

            this.escape();//ç»‘å®šæˆ–ç§»é™¤é”®ç›˜äº‹ä»¶

            this.backdrop(function () {
                var transition = $.support.transition && that.$element.hasClass('fade')

                if (!that.$element.parent().length) {
                    that.$element.appendTo(document.body) //don't move modals dom position
                }

                that.$element
                .show()

                if (transition) {
                    that.$element[0].offsetWidth // force reflow
                }

                that.$element
                .addClass('in')
                .attr('aria-hidden', false)

                that.enforceFocus()

                transition ?
                that.$element.one($.support.transition.end, function () {
                    that.$element.focus().trigger('shown')
                }) :
                that.$element.focus().trigger('shown')

            })
        }

        , 
        hide: function (e) {
            e && e.preventDefault()

            e = $.Event('hide')

            this.$element.trigger(e)

            if (!this.isShown || e.isDefaultPrevented()) return

            this.isShown = false

            this.escape()

            $(document).off('focusin.modal')

            this.$element
            .removeClass('in')
            .attr('aria-hidden', true)

            $.support.transition && this.$element.hasClass('fade') ?
            this.hideWithTransition() :
            this.hideModal()
        }

        , 
        //è®©æ¨¡æ€å¯¹è¯æ¡†èŽ·å¾—ç„¦ç‚¹
        enforceFocus: function () {
            var that = this
            $(document).on('focusin.modal', function (e) {
                if (that.$element[0] !== e.target && !that.$element.has(e.target).length) {
                    that.$element.focus()
                }
            })
        }

        , 
        //è¿™æ˜¯ä¸ªå¤±è´¥çš„è®¾è®¡
        escape: function () {
            var that = this
            //å¦‚æžœå·²ç»å¤„äºŽæ˜¾ç¤ºçŠ¶æ€ï¼Œå¹¶ä¸”å¯ä»¥ä½¿ç”¨é”®ç›˜å…³é—­ï¼Œé‚£ä¹ˆç»‘å®šé”®ç›˜äº‹ä»¶
            if (this.isShown && this.options.keyboard) {
                this.$element.on('keyup.dismiss.modal', function ( e ) {
                    e.which == 27 && that.hide()//å›žè½¦å…³é—­
                })
            } else if (!this.isShown) {
                this.$element.off('keyup.dismiss.modal')//ç§»é™¤äº‹ä»¶
            }
        }

        , 
        hideWithTransition: function () {
            var that = this
            //å¼ºåˆ¶ç»‘å®šç§»é™¤äº‹ä»¶
            , timeout = setTimeout(function () {
                that.$element.off($.support.transition.end)
                that.hideModal()
            }, 500)
            
            this.$element.one($.support.transition.end, function () {
                clearTimeout(timeout)
                that.hideModal()
            })
        }

        , 
        hideModal: function (that) {
            this.$element
            .hide()
            .trigger('hidden')
            //è§¦å‘éšè—å›žè°ƒ
            this.backdrop()//ç§»é™¤é®ç½©å±‚
        }

        , 
        removeBackdrop: function () {
            this.$backdrop.remove()
            this.$backdrop = null
        }

        , 
        backdrop: function (callback) {
            var that = this
            , animate = this.$element.hasClass('fade') ? 'fade' : ''

            if (this.isShown && this.options.backdrop) {
                var doAnimate = $.support.transition && animate
                //æ·»åŠ é®ç½©å±‚
                this.$backdrop = $('<div class="modal-backdrop ' + animate + '" />')
                .appendTo(document.body)

                this.$backdrop.click(
                    this.options.backdrop == 'static' ?
                    $.proxy(this.$element[0].focus, this.$element[0])
                    : $.proxy(this.hide, this)
                    )

                if (doAnimate) this.$backdrop[0].offsetWidth // force reflow
                //æ˜¾ç¤ºé®ç½©å±‚
                this.$backdrop.addClass('in')

                doAnimate ?
                this.$backdrop.one($.support.transition.end, callback) :
                callback()

            } else if (!this.isShown && this.$backdrop) {
                this.$backdrop.removeClass('in')

                $.support.transition && this.$element.hasClass('fade')?
                this.$backdrop.one($.support.transition.end, $.proxy(this.removeBackdrop, this)) :
                this.removeBackdrop()

            } else if (callback) {
                callback()
            }
        }
    }


    /* MODAL PLUGIN DEFINITION
  * ======================= */

    var old = $.fn.modal

    $.fn.modal = function (option) {
        return this.each(function () {
            var $this = $(this)
            , data = $this.data('modal')
            , options = $.extend({}, $.fn.modal.defaults, $this.data(), typeof option == 'object' && option)
            if (!data) $this.data('modal', (data = new Modal(this, options)))
            if (typeof option == 'string') data[option]()//show hide toggle
            else if (options.show) data.show()//å¦‚æžœåœ¨å‚æ•°æŒ‡æ˜Žè¦æ˜¾ç¤º
        })
    }

    $.fn.modal.defaults = {
        backdrop: true, 
        keyboard: true, 
        show: true
    }

    $.fn.modal.Constructor = Modal


    /* MODAL NO CONFLICT
  * ================= */

    $.fn.modal.noConflict = function () {
        $.fn.modal = old
        return this
    }


    /* MODAL DATA-API
  * ============== */

    $(document).on('click.modal.data-api', '[data-toggle="modal"]', function (e) {
        var $this = $(this)
        , href = $this.attr('href')
        , $target = $($this.attr('data-target') || (href && href.replace(/.*(?=#[^\s]+$)/, ''))) //strip for ie7
        , option = $target.data('modal') ? 'toggle' : $.extend({
            remote:!/#/.test(href) && href
        }, $target.data(), $this.data())

        e.preventDefault()

        $target
        .modal(option)
        .one('hide', function () {
            $this.focus()
        })
    })

}(window.jQuery);