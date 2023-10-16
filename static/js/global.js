document.addEventListener('DOMContentLoaded', function() {
    var array = document.querySelectorAll('switchbutton');
    array.forEach(element => {
        var attributes = element.attributes;
        element.outerHTML = '<label class="switch"' +
            (attributes.onclick ? ' onclick="' + attributes.onclick.value + '"' : '') +
            (attributes.id ? ' id="' + attributes.id.value + '"' : '') +
            (attributes.class ? ' class="' + attributes.class.value + '"' : '') +
            '>' +
            '<input type="checkbox"' +
            (attributes.checked ? ' checked' : '') +
            (attributes.disabled ? ' disabled' : '') +
            (attributes.name ? ' name="' + attributes.name.value + '"' : '') +
            '>' +
            '<span class="slider"></span>' +
            '</label>';
    })
});
