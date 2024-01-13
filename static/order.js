let cart = JSON.parse(localStorage.getItem('cart')) || [];
updateCart()
function updateCart() {
    const cartItemsElement = document.getElementById('cart-items');
    const totalElement = document.querySelector('.cart-container .checkout');

    cartItemsElement.innerHTML = '';

    let total = 0;

    cart.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.product_id} - ${item.name} - $${item.price} - Quantity: ${item.quantity}`;
        cartItemsElement.appendChild(li);

        total += item.price * item.quantity;
    });

    totalElement.textContent = `$${total.toFixed(2)}`;
    saveCartToLocalStorage(); // Save cart to localStorage after updating
}

function addToCart(productId, productName, productPrice) {
    // Check if the product is already in the cart
    const existingItem = cart.find(item => item.product_id === productId);

    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            product_id: productId,
            name: productName,
            price: parseFloat(productPrice),
            quantity: 1,
        });
    }

    updateCart();
}

function openCheckout() {
    // Redirect to the checkout page
    window.location.href = 'checkout';
}

function saveCartToLocalStorage() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

function checkout() {
    // Implement the checkout functionality here
    // For demonstration purposes, we'll log the cart items
    console.log('Checkout:', cart);

    // You can perform further actions like sending the cart data to the server for processing
}
