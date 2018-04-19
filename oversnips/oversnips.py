#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, abort
from flask_restful import Resource, Api
import signal
import sys
import threading
import argparse
from org.oversnips import TrainerWorker, NLUTrainer, NLUEngine

app = Flask(__name__)


@app.before_request
def only_json():
    if not request.is_json and request.method == 'POST':
        abort(400, "expecting json body")  # or any custom BadRequest message

class Status(Resource):
    def __init__(self, **kwargs):
        self.__trainer = kwargs['trainer']

    def get(self):
        training_ongoing = self.__trainer.ongoing_training
        return {
            'training_ongoing': training_ongoing
        }


class Train(Resource):
    def __init__(self, **kwargs):
        self.__dataset = kwargs['dataset']
        self.__model = kwargs['model']
        self.__trainer_worker = kwargs['trainer_worker']

    def get(self):
        self.__trainer_worker.ask_training(self.__dataset, self.__model)
        return { 'ok': True }


class Parse(Resource):
    def __init__(self, **kwargs):
        self.__engine = kwargs['engine']

    def post(self):

        #args = parseArgs.parse_args()

        json = request.get_json()
        query = json['query'] if "query" in json else None

        # TODO: secure intents attribute parsing (string or list)
        filter_intents = json['intents'] if "intents" in json else []
        if query is not None:
            if not filter_intents:
                intent = self.__engine.parse(json['query'])
                return intent
            else:
                intent = self.__engine.filtered_parse(json['query'], filter_intents)
                return intent

        else:
            abort(400, "invalid query")


def main():
    parser = argparse.ArgumentParser('oversnips', add_help=False)
    parser.add_argument('--help', action='help', help='show this help message and exit')
    parser.add_argument('-c', help='snips NLU configuration file', type=str, dest='snips_config_file')
    parser.add_argument('-d', help='NLU dataset', type=str, dest='dataset_file')
    parser.add_argument('-m', help='NLU model', type=str, dest='model_file')
    parser.add_argument('-l', help='NLU engine language', type=str, dest='language')
    parser.add_argument('-p', help='NLU engine port', type=int, dest='port')

    parser.set_defaults(snips_config_file="/Users/alain/Dev/smile/countrybot/snips/configs/config_fr.json")
    parser.set_defaults(dataset_file="/Users/alain/Dev/smile/countrybot/snips/data/dataset.json")
    parser.set_defaults(model_file="/Users/alain/Dev/smile/countrybot/snips/models/model.json")
    parser.set_defaults(language=u"fr")
    parser.set_defaults(port=9000)
    args = parser.parse_args()

    print("starting engine with {0} language and with this model: {1}".format(args.language, args.model_file))

    trainer = NLUTrainer(args.language, args.snips_config_file)
    engine = NLUEngine(args.language, args.model_file)
    trainer_worker = TrainerWorker(trainer, engine)
    t_trainer_worker = threading.Thread(target=trainer_worker.task)
    t_trainer_worker.setDaemon(True)
    t_trainer_worker.start()

    def on_stop(*args):
        print("Killed! Stopping worker...")
        trainer_worker.stop_worker()
        t_trainer_worker.join()
        sys.exit()

    signal.signal(signal.SIGINT, on_stop)
    signal.signal(signal.SIGTERM, on_stop)

    api = Api(app)
    api.add_resource(Status, '/status', resource_class_kwargs={'trainer': trainer})
    api.add_resource(Train, '/train', resource_class_kwargs={'trainer_worker': trainer_worker, 'dataset': args.dataset_file, 'model': args.model_file})
    api.add_resource(Parse, '/parse', resource_class_kwargs={'engine': engine})

    app.run(host='0.0.0.0', port=args.port)


if __name__ == '__main__':
    main()



#parseArgs = reqparse.RequestParser()
#parseArgs.add_argument('model', type=str, required=False)



"""

1) Train

GET /train?model=xyz

2) Status

GET /status

3) Parse

POST /parse?model=xyz

Input :

{
    "query": "Salut, quelle est la capitale du Mexique ? Merci!",
}

{
   "query": "Salut, quelle est la capitale du Mexique ? Merci!",
   "intents": ["sayYes", "sayNo"]
}

Output :

{
  "input": "Salut, quelle est la capitale du Mexique ? Merci!", 
  "slots": [
    {
      "slotName": "country", 
      "range": {
        "start": 33, 
        "end": 40
      }, 
      "rawValue": "Mexique", 
      "value": {
        "kind": "Custom", 
        "value": "Mexique"
      }, 
      "entity": "country_fr"
    }
  ], 
  "intent": {
    "intentName": "searchCountryCapital", 
    "probability": 0.8044335710487955
  }
}


"""