import io
import json
import time
from snips_nlu import SnipsNLUEngine, load_resources
from queue import Queue


class TrainerWorker:
    def __init__(self, trainer, engine):
        self.__queue = Queue()
        self.__engine = engine
        self.__trainer = trainer

    def ask_training(self, json_dataset_file, trained_engine_file):
        task = (json_dataset_file, trained_engine_file)
        self.__queue.put(task)
        return

    def stop_worker(self):
        self.__queue.put(None)
        return

    def task(self):
        while True:
            task = self.__queue.get()

            if task is not None:

                while self.__trainer.ongoing_training:
                    print("training already in progress. Waiting 5s...")
                    time.sleep(5)

                (json_dataset, trained_engine_file) = task
                print("training...")
                start_time = time.time()
                self.__trainer.train(json_dataset, trained_engine_file)
                elapsed_time = time.time() - start_time
                print("training done in {0:.2f}s".format(elapsed_time))
                print("force engine to reload model...")
                self.__engine.reload_engine()
                print("engine refreshed!")
                self.__queue.task_done()
            else:
                break


class NLUTrainer:
    def __init__(self, lang, config_file):
        self.__lang = lang
        self.__config_file = config_file
        self.__ongoing_training = False

        load_resources(self.__lang)

        with io.open(self.__config_file) as f:
            self.__config = json.load(f)

        self.__engine = SnipsNLUEngine(config=self.__config)

    @property
    def ongoing_training(self):
        return self.__ongoing_training

    def train(self, json_dataset, trained_engine_file):
        self.__ongoing_training = True
        with io.open(json_dataset) as f:
            dataset = json.load(f)

        self.__engine.fit(dataset)

        engine_json = json.dumps(self.__engine.to_dict())
        with io.open(trained_engine_file, mode="w") as f:
            f.write(engine_json)

        self.__ongoing_training = False
        return


# TODO: lazy loading of model file, to avoid chicken-egg problem (model not yet trained....)
class NLUEngine:
    def __init__(self, lang, trained_engine_file):
        self.__lang = lang
        self.__trained_engine_file = trained_engine_file

        load_resources(self.__lang)

        with io.open(self.__trained_engine_file) as f:
            engine_dict = json.load(f)

        self.__loaded_engine = SnipsNLUEngine.from_dict(engine_dict)

    def reload_engine(self):
        with io.open(self.__trained_engine_file) as f:
            engine_dict = json.load(f)

        self.__loaded_engine = SnipsNLUEngine.from_dict(engine_dict)
        return

    def parse(self, text):
        return self.__loaded_engine.parse(text)

    def filtered_parse(self, text, intents):
        return self.__loaded_engine.parse(text, intents)
