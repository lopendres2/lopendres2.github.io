import { Router } from "../../utils/router.js";

export class App {
  router = new Router([]);
  template = ``;
  items = fetch(
    "https://raw.githubusercontent.com/lopendres2/lopendres2.github.io/main/data/data.json"
  )
    .then((data) => {
      return data.json();
    })
    .then((data) => {
      // this.render(data);
    });

  constructor(hostElement) {
    this.hostElement = hostElement;
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
