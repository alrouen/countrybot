const _ = require('lodash');
const axios = require('axios');

axios.defaults.headers.post['Content-Type'] = "application/json";

class Intent {
    constructor(snipsResponse) {

        if(snipsResponse.intent) {

            this._intent = {
                'found': true,
                'name': snipsResponse.intent.intentName,
                'probability': snipsResponse.intent.probability
            }

        } else {
            this._intent = {
                'found': false,
                'name': "",
                'probability': 0.0
            }
        }

        if(snipsResponse.slots) {

            this._slots = snipsResponse.slots.map(slot => ({
                value: slot.value.value,
                kind: slot.value.kind,
                rawValue: slot.rawValue,
                slotName: slot.slotName
            }));
        } else {
            this._slots = [];
        }

        console.debug(`intent: "${this._intent.name}" with probability: ${this._intent.probability}`);
        console.debug(`slots: ${this._slots.length}`);
        this._slots.forEach((slot) => { console.debug(` * ${slot.slotName} - ${slot.value}`) });
    }

    get found() {
        return this._intent.found;
    }

    get name() {
        return this._intent.name;
    }

    get probability() {
        return this._intent.probability;
    }

    get slots() {
        return this._slots;
    }

    slotByName(name) {
        return _.find(this._slots, {"slotName": name});
    }

}

module.exports = {

    Intent,

    getIntent: async (rawText) => {
        return axios.post(
            'http://localhost:10000/parse',
            {
                "query":rawText
            }
        ).then(function (response) {
            return new Intent(response.data);
        }).catch(function (error) {
            console.debug("Oops...");
            console.debug(error);
            return new Intent({
                input:rawText
            })
        });
    },

    getFilteredIntent: async (rawText, intentFilter) => {
        return axios.post(
            'http://localhost:10000/parse',
            {
                "query":rawText,
                "intents": intentFilter
            }
        ).then(function (response) {
            return new Intent(response.data);
        }).catch(function (error) {
            console.debug("Oops...");
            console.debug(error);
            return new Intent({
                input:rawText
            })
        });
    }

};

/*

{
    "input": "Mais enfin, quelle est la capitale de l'Allemagne ?",
    "intent": {
        "intentName": "searchCountryCapital",
        "probability": 0.7962090089294452
    },
    "slots": [
        {
            "entity": "country_fr",
            "range": {
                "end": 59,
                "start": 50
            },
            "rawValue": "Allemagne",
            "slotName": "country",
            "value": {
                "kind": "Custom",
                "value": "Allemagne"
            }
        }
    ]
}

----

{
	"input": "...."
	"intent":null
	"slots":null
}

 */