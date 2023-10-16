document.addEventListener('DOMContentLoaded', function() {
    var array = document.querySelectorAll('switchbutton');
    array.forEach(element => {
        var attributes = element.attributes;
        element.outerHTML = '<label class="switch"' +
            (attributes.onclick ? ' onclick="' + attributes.onclick.value + '"' : '') +
            (attributes.id ? ' id="' + attributes.id.value + '"' : '') +
            (attributes.class ? ' class="' + attributes.class.value + '"' : '') +
            (attributes.name ? ' name="' + attributes.name.value + '"' : '') +
            '>' +
            '<input type="checkbox"' +
            (attributes.checked ? ' checked' : '') +
            (attributes.disabled ? ' disabled' : '') +
            '>' +
            '<span class="slider"></span>' +
            '</label>';
    })
});
