const _ = require('lodash');
const moment = require('moment');

module.exports = {
    text: data => {
        const text = _.sample([data.text, ...(data.variations || [])]);
        return {text: text, typing: !!data.typing};
    },

    choice: data => ({
        text: data.text,
        quick_replies: data.choices.map(button => `<${button.payload}> ${button.text}`)
    }),

    '#welcome': data => [
        {
            typing: true,
            text: _.sample(['Hey there!', 'Hello {{user.first_name}}', 'Good day :)'])
        },
        {
            text: "This is just a regular Hello World, I don't do anything ;)",
            typing: '2s'
        },
        {
            text: "Make sure to check out the 'index.js' file to see how I work",
            typing: true
        },
        {
            wait: '5s'
        },
        {
            text: 'You can say goodbye now',
            typing: '1s'
        }
    ],

    '#goodbye': data => [
        {
            text: 'You are leaving because of reason {{reason}}',
            typing: true
        },
        'Hope to see you back again soon! :)' // if no other properties, you can just send a string
    ]
};