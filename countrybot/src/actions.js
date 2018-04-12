const _ = require('lodash');
const axios = require('axios');
const moment = require('moment');
const oversnips = require('./oversnips');
const countryDB = require('./countryDB');


//const moment = require('moment');
//const ms = require('ms');

axios.defaults.headers.post['Content-Type'] = "application/json";

moment.locale('fr');

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

        if(!!intentFilter) {
            return await oversnips.getFilteredIntent(event.text, intentFilter.split(',')).then((intent) => {
                return { ...state, intent: intent };
            });
        } else {
            return await oversnips.getIntent(event.text).then((intent) => {
                return { ...state, intent: intent };
            });
        }
    },

    searchCountryCapital: async (state, event) => {
      if(state.intent.found && state.intent.name === "searchCountryCapital") {

          let countrySlot = state.intent.slotByName("country");
          if(countrySlot) {
              let country = countryDB.countryByName(countrySlot.value);
              return { ...state, searchCountryCapitalResponse: country }
          } else {
              return _.omit(state, ["searchCountryCapitalResponse"]);
          }
      }
    },

    computeTime: (state, event) => {
        return { ...state, now: moment().format('HH:mm:ss')};
    },

    computeDayOfWeek: (state, event) => {

        let dateSlot = state.intent.slotByName("date");
        let d = moment(dateSlot.value, "YYYY-MM-DD HH:mm:ss +-HH:mm");

        return { ...state, dayOfWeekResponse: {date: d.format("DD MMMM YYYY"), weekDay: moment.weekdays(d.weekday()+1)} };
    },

    debug: (state, event) => {
        console.log(state);
        return {...state};
    }

};
