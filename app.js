let tg = window.Telegram.WebApp;

tg.expand();

tg.MainButton.textColor = '#FFFFFF';
tg.MainButton.color = '#0f53e6';

let cart = [];

const container = document.querySelector('.inner')


container.addEventListener("click", onClick);

function onClick(event){
    const current = event.target;

    if(!current.classList.contains('btn')){
        return ;
    }

    handleButtonClick('Товар' + ' ' + current.id)

}

function addToCart(item) {
    cart.push(item);
    updateCart();
}

function updateCart() {
    // Дополнительные действия при обновлении корзины, если нужны
    // Например, обновление отображения на странице
}

function showCart() {
    tg.MainButton.setText(`В корзине: ${cart.length} товаров`);
    tg.MainButton.show();
}

function hideCart() {
    tg.MainButton.hide();
}

function handleButtonClick(itemText) {
    addToCart(itemText);
    showCart();
}


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
