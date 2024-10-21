const { useState, reactive } = owl;


class Store {
    updateLang(newLang) {        
        this.lang = newLang;
        document.documentElement.lang = this.lang;
    }
}


export function createStore() {
    return reactive(new Store());
}
