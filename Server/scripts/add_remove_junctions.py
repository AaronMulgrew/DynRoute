import json

junct_data = open("routes.json").read()
parsed = json.loads(junct_data)
for element in parsed['junctions']:
    print element

print json.dumps(parsed, indent=4, sort_keys=True)