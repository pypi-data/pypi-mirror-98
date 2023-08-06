import json

from pydict_surf.dict_router import DictRouter

jdict = None
with open("template.json", 'r') as file:
    jdict = json.load(file)

iterator = DictRouter(jdict)

# iterator.chdict("ai.models")
# print(iterator.listdict())

iterator.chdict("..")
for i in iterator.walk(max_depth=2):
    print(i)