const axios = require('axios');

axios.defaults.headers.post['Content-Type'] = "application/json";

const probabilityThreshold = 0.6;

class Intent {
    constructor(snipsResponse) {

        if(snipsResponse.intent) {

            if(snipsResponse.intent.probability >= probabilityThreshold) {
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
            console.log("Oops...");
            console.log(error);
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
            console.log("Oops...");
            console.log(error);
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