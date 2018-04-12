const _ = require('lodash')

module.exports = {
    id: 'choice',
    title: 'Choice Questions',
    renderer: '#choice-question',

    jsonSchema: {
        title: 'Choice Questions',
        description: 'Create a new question with up to 5 choices',
        type: 'object',
        required: ['question', 'answers'],
        properties: {
            question: {
                type: 'string',
                title: 'Question'
            },
            answers: {
                title: 'Answers',
                type: 'array',
                items: {
                    type: 'string',
                    default: ''
                }
            }
        }
    },

    uiSchema: {
        answers: {
            'ui:options': {
                orderable: false
            }
        }
    },

    computeData: formData => {
        const choiceList = formData.answers.map(i => ({ payload: 'ANSWER', text: i }))

        return {
            question: formData.question,
            answers: [...choiceList]
        }
    },

    computePreviewText: formData => 'Question: ' + formData.question,
    computeMetadata: null
};
