document.body.addEventListener('htmx:afterSwap', function (evt) {
    const newEl = evt.target;
    $(newEl).find('[data-module]').each(function () {
        ckan.module.initializeElement(this);
    });
});

$(document).on('scheming.subfield-group-init', function(e) {
    // Media Widget Fix for repeating fields of ckanext-scheming
    const $media_btns = $(e.target).find('.scheming-subfield-group .media-list-load-btn');
    $media_btns.each(function(){
        htmx.process(this);
    })
});
