ckan.module("media-widget-copy", function ($, _) {
  "use strict";
  return {
    options: {
        text: null,
    },

    initialize: function () {
        $.proxyAll(this, /_on/);
        this.el.on('click', (event) => {
            event.preventDefault();
            const modal_content = $(this.el).closest('.media-modal-content').first();

            if (modal_content.attr('data-target')) {
              $('#' + modal_content.attr('data-target')).val(this.options.text);
            } else {
              navigator.clipboard.writeText(this.options.text);
            }

            if (modal_content.attr('data-modal-id')) {
              $('#' + modal_content.attr('data-modal-id')).modal('hide');
            }
        });
    },
  };
});
