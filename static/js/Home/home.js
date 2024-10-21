const { Component, xml, onWillStart,useRef, onMounted, useState, loadFile, markup, useEnv } = owl;

export class Root extends Component {
    static template = xml/* xml */ `
        <div>
            <t t-if="promiseResolved">
                <t t-out="templateData" />
            </t>
            <t t-else="">
                Loading...
            </t>
        </div>
    `

    static components = {};

    promiseResolved = false;
    templateData = "";

    setup() {
        this.alert = useState({});

        onWillStart(async () => {
            this.templateData = await loadFile("static/js/Home/home.xml");
            this.templateData = markup(this.templateData);
            this.promiseResolved = true;
        })
    }

}