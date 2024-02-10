$(document).on('click', '.add-products-action-button', function (event) {
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: cartUpdateData.addProductUrl,
        data: {
            'product_id': $(this).data('product-id'),
            'quantity': $('input[name="quantity"]').val(),
            'csrfmiddlewaretoken': cartUpdateData.csrfToken,
        },
        success: function (json) {
            document.getElementById("total_cart_quantity").textContent = json.total_cart_quantity;
            $('input[name="quantity"]').val('1');
        },
        error: function (xhr, errmsg, err) {}
    });
})
