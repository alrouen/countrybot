const _ = require('lodash');
const moment = require('moment');
const axios = require('axios');
//const Promise = require('bluebird');
const ms = require('ms');
const oversnips = require('./oversnips');

axios.defaults.headers.post['Content-Type'] = "application/json";

/**
 * @param {string} args.name - Name of the tag.
 * @param {string} args.value - Value of the tag.
 */
const setUserTag = async (state, event, { name, value }) => {
    await event.bp.db.kvs.set(`${event.user.id}::${name}`, value);
    return { ...state }
};


module.exports = {
    setUserTag,

    /**
     * @param {string} args.name - Name of the tag.
     * @param {string} args.into - Name of the state field to keep the value.
     */
    getUserTag: async (state, event, { name, into }) => {
        const value = await event.bp.db.kvs.get(`${event.user.id}::${name}`);
        return { ...state, [into]: value }
    },

    removeStateVariable: async (state, event, { name }) => {
        return _.omit(state, [name])
    },

    renderElement: async (state, event, { element }) => {
        await event.reply(element, { state })
    },

    /**
     * Persists the user's response into the state
     * @param {string} args.into - Variable in the state to hold the response
     */
    rememberInput: async (state, event, { into, path = 'text' } = {}) => {
        return { ...state, [into]: _.get(event, path) }
    },

    resolveIntent: async (state, event, { intentFilter } ) => {

        event.reply('text', { typing: true });

        // console.log(`intent: ${snipsResponse.intent.intentName}: ${snipsResponse.intent.probability}`);

        if(!!intentFilter) {
            return await oversnips.getFilteredIntent(event.text, intentFilter.split(',')).then((intent) => {
                console.log(`intent: ${intent.name}: ${intent.probability}`);
                console.log("slots:");
                console.log(intent.slots);
                return { ...state, intent: intent };
            });
        } else {
            return await oversnips.getIntent(event.text).then((intent) => {
                console.log(`intent: ${intent.name}: ${intent.probability}`);
                console.log("slots:");
                console.log(intent.slots);
                return { ...state, intent: intent };
            });
        }
    },

    debug: (state, event) => {
        console.log(state);
        return {...state};
    }

};
