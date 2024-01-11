let tg = window.Telegram.WebApp;

tg.expand();

tg.MainButton.textColor = '#FFFFFF';
tg.MainButton.color = '#0f53e6';

let cart = [];

let btn1 = document.getElementById("btn1");
let btn2 = document.getElementById("btn2");
let btn3 = document.getElementById("btn3");
let btn4 = document.getElementById("btn4");
let btn5 = document.getElementById("btn5");
let btn6 = document.getElementById("btn6");

function addToCart(item) {
    cart.push(item);
    updateCart();
}

function updateCart() {
    // Дополнительные действия при обновлении корзины, если нужны
    // Например, обновление отображения на странице
}

function showCart() {
    tg.MainButton.setText(`В корзине: ${cart.join(", ")}`);
    tg.MainButton.show();
}

function hideCart() {
    tg.MainButton.hide();
}

function handleButtonClick(itemText) {
    addToCart(itemText);
    showCart();
}

btn1.addEventListener("click", function() {
    handleButtonClick("Товар 1");
});

btn2.addEventListener("click", function() {
    handleButtonClick("Товар 2");
});

btn3.addEventListener("click", function() {
    handleButtonClick("Товар 3");
});

btn4.addEventListener("click", function() {
    handleButtonClick("Товар 4");
});

btn5.addEventListener("click", function() {
    handleButtonClick("Товар 5");
});

btn6.addEventListener("click", function() {
    handleButtonClick("Товар 6");
});

Telegram.WebApp.onEvent("mainButtonClicked", function() {
    // Дополнительные действия при нажатии на главную кнопку, если нужны
    // Например, отправка данных из корзины
    tg.sendData(cart);
    hideCart();
});

let usercard = document.getElementById("usercard");

let p = document.createElement("p");

p.innerText = `${tg.initDataUnsafe.user.first_name} ${tg.initDataUnsafe.user.last_name}`;

usercard.appendChild(p);
