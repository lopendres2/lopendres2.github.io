export class Category {
    constructor(data, hostElement) {
        this.data = data;
        this.hostElement = hostElement;
        this.template = `
            <div class="container">
                <div class="inner"></div>
            </div>
        `;
        this.render();
    }

    render() {
        this.hostElement.innerHTML = this.template;
        this.container = this.hostElement.querySelector(".inner");
        this.renderItems();
    }

    renderItems() {
        // В hash категория закодирована (например %D0%BE%D0%B1%D1%83%D0%B2%D1%8C)
        const category = decodeURIComponent(location.hash.split("/")[1] || "");
        const items = this.data.filter(item => item.category === category);
        if (!items.length) {
            this.container.innerHTML = `<p class="item__text">В категории «${category}» пока нет товаров.</p>`;
            return;
        }
        let text = "";
        items.forEach((item, i) => {
            let itemHtml = `<div class="item">
                <div class="item__img-box">
                    <img src="${(item.img && item.img[0]) || ""}" alt="${item.name}" class="item__img" loading="lazy">
                </div>
                <p class="item__text">${item.name}</p>
                <p class="item__text">${item.description}</p>
                <button class="item__btn" data-item="${item.name}">Узнать цену</button>
            </div>`;
            text = text + itemHtml;
        });
        this.container.innerHTML = text;
        this.applyHandlers();
    }

    applyHandlers() {
        this.container.addEventListener("click", (event) => {
            if (event.target.classList.contains("item__btn")) {
                const itemName = event.target.getAttribute("data-item");
                this.requestPrice(itemName);
            }
        });
    }

    requestPrice(itemName) {
        const tg = window.Telegram.WebApp;
        tg.sendData(JSON.stringify({ action: "request_price", item: itemName }));
        tg.close();
    }
}