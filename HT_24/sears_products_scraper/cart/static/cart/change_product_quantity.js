    $(document).on('click', '.change-quantity-action-button', function (event) {
        event.preventDefault();
        var product_id = $(this).data('product-id');
        var action_value = $(this).val();
        $.ajax({
            type: 'POST',
            url: cartUpdateData.operations.changeProductQuantity.url,

            data: {
                'product_id': product_id,
                'action': action_value,
                'csrfmiddlewaretoken': cartUpdateData.csrfToken,
            },
            success: function (json) {
                document.getElementById("total_cart_quantity").textContent = json.total_cart_quantity;
                document.getElementById("product-quantity-" + product_id).textContent = json.product_quantity;

                document.getElementById("product-cost-" + product_id).textContent = "$"+json.products_total_cost;
                document.getElementById("product-cost-" + product_id).style.fontWeight = "bold";

                document.getElementById("cart_total_amount").textContent = "$"+json.cart_total_amount;
                document.getElementById("cart_total_amount").style.fontWeight = "bold";

            },
            error: function (xhr, errmsg, err) {}
        });
    })