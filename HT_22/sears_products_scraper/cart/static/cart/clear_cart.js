    $(document).on('click', '.clear-cart-action-button', function (event) {
        event.preventDefault();

        $.ajax({
            type: 'POST',
            url: cartUpdateData.operations.clearCart.url,

            data: {
                'csrfmiddlewaretoken': cartUpdateData.csrfToken,
            },
            success: function (json) {
                if (json.total_cart_quantity === 0) {
                    document.getElementById("total_cart_quantity").textContent = json.total_cart_quantity;
                    $('#cart-data').remove();
                    $('#empty-cart').show();

                }
                },
            error: function (xhr, errmsg, err) {}
        });
    })