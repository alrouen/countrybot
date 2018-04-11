import io
import json

from snips_nlu import SnipsNLUEngine, load_resources

load_resources(u"fr")

with io.open("config_fr.json") as f:
    config = json.load(f)

engine = SnipsNLUEngine(config=config)

with io.open("dataset.json") as f:
    dataset = json.load(f)

engine.fit(dataset)

engine_json = json.dumps(engine.to_dict())
with io.open("trained_engine.json", mode="w") as f:
    f.write(engine_json.decode("utf8"))  # Python 2

# f.write(engine_json)  # Python 3

