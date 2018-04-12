from flask import Flask, request, abort
from flask_restful import Resource, Api, reqparse
import signal
import threading
from json import dumps, loads
# from flask.ext.jsonpify import jsonify

from org.oversnips import TrainerWorker, NLUTrainer, NLUEngine

lang = u"fr"
config = "/Users/alain/Dev/smile/countrybot/snips/configs/config_fr.json"
dataset = "/Users/alain/Dev/smile/countrybot/snips/data/dataset.json"
model = "/Users/alain/Dev/smile/countrybot/snips/models/model.json"

trainer = NLUTrainer(lang, config)
engine = NLUEngine(lang, model)
trainerWorker = TrainerWorker(trainer, engine)
t_trainerWorker = threading.Thread(target=trainerWorker.task)
t_trainerWorker.setDaemon(True)
t_trainerWorker.start()

def on_stop():
    print("Killed! Stopping worker...")
    trainerWorker.stop_worker()
    t_trainerWorker.join()
    return


signal.signal(signal.SIGINT, on_stop)


class Status(Resource):
    def get(self):
        training_ongoing = trainer.ongoing_training
        return {
            'training_ongoing': training_ongoing
        }


class Train(Resource):
    def get(self):
        trainerWorker.ask_training(dataset, model)
        return { 'ok': True }


parseArgs = reqparse.RequestParser()
parseArgs.add_argument('model', type=str, required=False)


class Parse(Resource):
    def post(self):

        args = parseArgs.parse_args()

        json = request.get_json()
        query = json['query'] if "query" in json else None

        # TODO: secure intents attribute parsing (string or list)
        filter_intents = json['intents'] if "intents" in json else []
        if query is not None:
            if not filter_intents:
                intent = engine.parse(json['query'])
                return intent
            else:
                intent = engine.filtered_parse(json['query'], filter_intents)
                return intent

        else:
            abort(400, "invalid query")


# engine = SnipsNLUEngine(u"fr", )

app = Flask(__name__)
api = Api(app)
api.add_resource(Status, '/status')
api.add_resource(Train, '/train')
api.add_resource(Parse, '/parse')


@app.before_request
def only_json():
    if not request.is_json and request.method == 'POST':
        abort(400, "expecting json body")  # or any custom BadRequest message


if __name__ == '__main__':
    app.run(port=10000)

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