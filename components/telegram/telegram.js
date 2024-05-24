export class Telegram {
    constructor(){
        this.tg = window.Telegram.WebApp;
        this.render();
        this.applyHandler();
    }
    render(){
        this.tg.expand();
        this.tg.MainButton.textColor = '#FFFFFF';
        this.tg.MainButton.color = '#0f53e6'; 
        console.log('work')
    }
    applyHandler(){
        this.tg.onEvent("mainButtonClicked", function() {
            // Дополнительные действия при нажатии на главную кнопку, если нужны
            // Например, отправка данных из корзины
            this.tg.sendData(cart);
            hideCart();
        });
    }
    showCart() {
        this.tg.MainButton.setText(`В корзине: ${cart.length} товаров`);
        this.tg.MainButton.show();
    }
}