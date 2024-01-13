// Assume the cart data is stored in localStorage as an array of objects
let cart = JSON.parse(localStorage.getItem('cart')) || [];

function updateCart() {
    const cartItemsElement = document.getElementById('cart-items');
    const cartTotalElement = document.getElementById('cart-total');

    cartItemsElement.innerHTML = '';

    let total = 0;

    cart.forEach(item => {
        const row = document.createElement('tr');

        row.innerHTML = `
            <td>${item.name}</td>
            <td>$${item.price.toFixed(2)}</td>
            <td><input type="number" value="${item.quantity}" min="1" onchange="updateQuantity('${item.product_id}', this.value)"></td>
            <td><button onclick="removeItem('${item.product_id}')">❌</button></td>
        `;

        cartItemsElement.appendChild(row);
        total += item.price * item.quantity;
    });

    cartTotalElement.textContent = total.toFixed(2);
    saveCartToLocalStorage();
}

function removeItem(productId) {
    cart = cart.filter(item => item.product_id !== productId);
    updateCart();
}

function updateQuantity(productId, newQuantity) {
    const item = cart.find(item => item.product_id === productId);
    if (item) {
        item.quantity = parseInt(newQuantity, 10);
        updateCart();
    }
}

function submitOrder(event) {
    event.preventDefault();

    const phoneNumber = document.getElementById('phoneNumber').value;
    const fullName = document.getElementById('fullName').value;
    const address = document.getElementById('address').value;

    // You can include additional order information as needed
    const orderData = {
        phoneNumber,
        fullName,
        address,
        cart,
    };

    // For demonstration purposes, we'll log the order data
    console.log('Order:', orderData);

    // Clear the cart after checkout
    cart = [];
    updateCart();

    // You can now send the order data to the server for further processing
}

function saveCartToLocalStorage() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

// Initial update when the page loads
document.addEventListener('DOMContentLoaded', updateCart);