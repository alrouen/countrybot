from flask import Flask, request, abort
from flask_restful import Resource, Api
import signal
import threading
from json import dumps, loads
# from flask.ext.jsonpify import jsonify

from org.oversnips import TrainerWorker, NLUTrainer, NLUEngine

lang = u"fr"
config = "/Users/alain/Dev/smile/countrybot/snips/data/config_fr.json"
dataset = "/Users/alain/Dev/smile/countrybot/snips/data/dataset.json"
model = "/Users/alain/Dev/smile/countrybot/snips/data/model.json"

trainer = NLUTrainer(lang, config)
engine = NLUEngine(lang, model)
trainerWorker = TrainerWorker(trainer)
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


class Parse(Resource):
    def post(self):
        json = request.get_json()
        if json['query'] is not None:
            intent = engine.parse(json['query'])
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
    "model": "xxxx"
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