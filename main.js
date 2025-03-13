import { App } from "./components/app/app.js";
import { Telegram } from "./components/telegram/telegram.js";

const appElement = document.querySelector(".app");
const Application = new App(appElement);
const tg = new Telegram();