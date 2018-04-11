const _ = require('lodash');
const jsdoc = require('jsdoc-api');
const yn = require('yn');
const moment = require('moment');

const renderers = require('./renderers');
const actions = require('./actions');

module.exports = bp => {
    Object.keys(renderers).forEach(name => {
        bp.renderers.register(name, renderers[name])
    });

    jsdoc.explain({ files: [__dirname + '/actions.js'] }).then(docs => {
        bp.dialogEngine.setFunctionMetadataProvider(fnName => {
            const meta = docs.find(({ name }) => name === fnName);
            return {
                desciption: meta.description,
                params: (meta.params || [])
                    .filter(({ name }) => name.startsWith('args.'))
                    .map(arg => ({ ...arg, name: arg.name.replace('args.', '') }))
            }
        });
        bp.dialogEngine.registerFunctions(actions);
    });

    if (yn(process.env.DEBUG_INCOMING)) {
        bp.hear(
            () => true,
            (event, next) => {
                bp.logger.debug('Incoming::', require('util').inspect(_.omit(event, ['bp']), { depth: 2, colors: true }));
                next();
            }
        )
    }

    // All events that should be processed by the Flow Manager
    bp.hear({ type: /text|message|quick_reply|image|location|payment/i }, event => {
        bp.dialogEngine.processMessage(event.sessionId || event.user.id, event).then()
    });

    // Listens for a first message (this is a Regex)
    // GET_STARTED is the first message you get on Facebook Messenger
   // bp.hear(/GET_STARTED|hello|hi|test|hey|holla/i, (event, next) => {
   //     event.reply('#welcome');
   // });

    // You can also pass a matcher object to better filter events
   /* bp.hear(
        {
            type: /message|text/i,
            text: /exit|bye|goodbye|quit|done|leave|stop/i
        },
        (event, next) => {
            event.reply('#goodbye', {
                reason: 'unknown'
            })
        }
    ); */
};