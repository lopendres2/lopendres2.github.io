export class Cart {
    constructor(){
        this.data = [];
        this.tg = window.Telegram.WebApp;
        this.applyHandler();
    }

    applyHandler(){
        Telegram.WebApp.onEvent("mainButtonClicked", function() {
            // Дополнительные действия при нажатии на главную кнопку, если нужны
            // Например, отправка данных из корзины
            tg.sendData(cart);
            hideCart();
        });
    }
    
    showCart() {
        this.tg.MainButton.setText(`В корзине: ${this.data.length} товаров`);
        this.tg.MainButton.show();
    }
    
    hideCart() {
        this.tg.MainButton.hide();
    }
    
    handleButtonClick(itemText) {
        addToCart(itemText);
        showCart();
    }
    addToCart(item) {
        cart.push(item);
        updateCart();
    }
    
    updateCart() {
        // Дополнительные действия при обновлении корзины, если нужны
        // Например, обновление отображения на странице
    }
}