const { mount, App, loadFile, xml } = owl;
import { Root } from "./home.js";
import { createStore } from "./store.js";

// -------------------------------------------------------------------------
// Setup
// -------------------------------------------------------------------------

const env = {
    store: createStore(),
};

async function setup() {
    console.log(Root.template);

    const translateFn = (str) => str;
    const app = new App(Root, { dev: true, env, translateFn, translatableAttributes: ["placeholder"] });
    app.mount(document.body);
}

setup();
