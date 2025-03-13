import { Router } from "../../utils/router.js";

export class App {
    router = new Router([]);
    template = ``;

    constructor(hostElement) {
        this.hostElement = hostElement;
        this.init();
    }

    async init() {
        const data = await fetch(
            "https://raw.githubusercontent.com/lopendres2/lopendres2.github.io/main/data/data.json"
        ).then((response) => response.json());

        this.render(data);
    }

    render(data) {
        this.hostElement.innerHTML = this.template;

        this.router.add("Home", () => {
            this.hostElement.innerHTML = "";
            import("../home/home.js").then(({ Home }) => {
                new Home(data, this.hostElement).render();
            });
        });

        this.router.add("About", () => {
            this.hostElement.innerHTML = "";
            import("../about/about.js").then(({ About }) => {
                new About(data, this.hostElement).render();
            });
        });

        this.router.onHashChange();
    }
}