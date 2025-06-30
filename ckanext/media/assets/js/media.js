document.body.addEventListener('htmx:afterSwap', function (evt) {
    const newEl = evt.target;
    $(newEl).find('[data-module]').each(function () {
        ckan.module.initializeElement(this);
    });
});
