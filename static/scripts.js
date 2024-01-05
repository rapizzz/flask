document.addEventListener('DOMContentLoaded', function () {
    const productItems = document.querySelectorAll('.product-item');
    const cartInfo = document.querySelector('.cart-info');
    const totalElement = document.querySelector('.total');
    const checkoutButton = document.querySelector('.checkout');
    const detailsPopup = document.querySelector('.product-details-popup');
    const closePopupButton = detailsPopup.querySelector('.close-popup');

    let cartTotal = 0;
    let cartItems = [];

    productItems.forEach(item => {
        const addToCartButton = item.querySelector('.add-to-cart');
        const quantityElement = item.querySelector('.quantity');

        addToCartButton.addEventListener('click', function () {
            const productId = item.dataset.productId;
            const productPrice = parseFloat(item.querySelector('.product-price').innerText.replace('$', ''));
            const quantity = parseInt(quantityElement.innerText);

            const cartItem = {
                productId: productId,
                price: productPrice,
                quantity: quantity
            };

            const existingItemIndex = cartItems.findIndex(item => item.productId === productId);

            if (existingItemIndex !== -1) {
                cartItems[existingItemIndex].quantity += quantity;
            } else {
                cartItems.push(cartItem);
            }

            cartTotal += productPrice * quantity;
            updateCartInfo();
        });

        item.querySelector('.quantity-btn.minus').addEventListener('click', function () {
            const currentQuantity = parseInt(quantityElement.innerText);
            if (currentQuantity > 1) {
                quantityElement.innerText = (currentQuantity - 1).toString();
            }
        });

        item.querySelector('.quantity-btn.plus').addEventListener('click', function () {
            const currentQuantity = parseInt(quantityElement.innerText);
            quantityElement.innerText = (currentQuantity + 1).toString();
        });

        item.querySelector('.show-details').addEventListener('click', function () {
            // Add logic to show details popup with slider and description
            detailsPopup.style.display = 'block';
        });
    });

    closePopupButton.addEventListener('click', function () {
        detailsPopup.style.display = 'none';
    });

    function updateCartInfo() {
        totalElement.innerText = `Total: $${cartTotal.toFixed(2)}`;
        checkoutButton.disabled = cartTotal === 0;
    }

    checkoutButton.addEventListener('click', function () {
        // Add logic for handling checkout (redirect to checkout page, etc.)
        console.log('Checkout clicked');
    });
});
