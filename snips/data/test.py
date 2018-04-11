import io
import json

from snips_nlu import SnipsNLUEngine, load_resources

load_resources(u"fr")

with io.open("trained_engine.json") as f:
    engine_dict = json.load(f)

loaded_engine = SnipsNLUEngine.from_dict(engine_dict)

parsing = loaded_engine.parse(u"Salut, quelle est la capitale du Mexique ? Merci!")

print(json.dumps(parsing, indent=2))

