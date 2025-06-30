ckan.module("media-copy-text", function ($, _) {
  "use strict";
  return {
    options: {
        text: null,
    },

    initialize: function () {
        $.proxyAll(this, /_on/);
        this.el.on('click', (event) => {
            event.preventDefault();
            navigator.clipboard.writeText(this.options.text);
        });
    },
  };
});
