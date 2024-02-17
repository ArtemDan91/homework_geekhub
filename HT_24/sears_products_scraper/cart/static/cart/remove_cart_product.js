    $(document).on('click', '.remove-product-action-button', function (event) {
        event.preventDefault();
        var product_id = $(this).data('product-id');

        $.ajax({
            type: 'POST',
            url: cartUpdateData.operations.removeCartProduct.url,

            data: {
                'product_id': product_id,
                'csrfmiddlewaretoken': cartUpdateData.csrfToken,
            },
            success: function (json) {
                document.getElementById("total_cart_quantity").textContent = json.total_cart_quantity;
                if (json.total_cart_quantity === 0) {
                    $('#cart-data').remove();
                    $('#empty-cart').show();

                } else {
                    document.getElementById("cart_total_amount").textContent = "$" + json.cart_total_amount;
                    document.getElementById("cart_total_amount").style.fontWeight = "bold";

                    $(".product-item[data-product-id='" + product_id + "']").remove();
                }
                },
            error: function (xhr, errmsg, err) {}
        });
    })