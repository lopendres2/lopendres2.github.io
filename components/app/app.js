import { Router } from "../../utils/router.js";

export class App {
    router = new Router([]);
    template = ``;

    constructor(hostElement) {
        this.hostElement = hostElement;
        this.init();
    }

    async init() {
        // Загружаем данные при инициализации
        const data = await this.fetchData();
        this.render(data);

        // Обновляем данные каждые 5 минут
        setInterval(async () => {
            const newData = await this.fetchData();
            this.render(newData); // Перерисовываем страницу с новыми данными
        }, 300000); // 300000 мс = 5 минут
    }

    // Функция для загрузки данных
    async fetchData() {
        const response = await fetch(
            "https://raw.githubusercontent.com/lopendres2/lopendres2.github.io/main/data/data.json"
        );
        return await response.json();
    }

    render(data) {
        this.hostElement.innerHTML = this.template;

        // Добавляем маршруты
        this.router.add("Home", () => {
            this.hostElement.innerHTML = "";
            import("../home/home.js").then(({ Home }) => {
                new Home(data, this.hostElement).render();
            });
        });

        this.router.add("Category", () => {
            this.hostElement.innerHTML = "";
            import("../category/category.js").then(({ Category }) => {
                new Category(data, this.hostElement).render();
            });
        });

        // Инициализируем роутер
        this.router.onHashChange();
    }
}