export class Cart {
    constructor() {
        this.data = [];
        this.tg = window.Telegram.WebApp;
        this.applyHandler();
    }

    applyHandler() {
        this.tg.MainButton.onClick(() => {
            this.tg.sendData(JSON.stringify(this.data)); // Отправляем данные корзины
            this.hideCart();
        });
    }

    showCart() {
        this.tg.MainButton.setText(`В корзине: ${this.data.length} товаров`);
        this.tg.MainButton.show();
    }

    hideCart() {
        this.tg.MainButton.hide();
    }

    addToCart(item) {
        this.data.push(item);
        this.updateCart();
    }

    updateCart() {
        if (this.data.length > 0) {
            this.showCart();
        } else {
            this.hideCart();
        }
    }
}