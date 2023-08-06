import json
import os

filedir = os.path.dirname(__file__)
global_shapes = json.load(open(os.path.join(filedir, "global_shapes.json")))
sqs_structures = json.load(open(os.path.join(filedir, "sqs-2012-11-05.normal.json")))

sqs_top_level_shape_names = [op["output"]["shape"] for op in sqs_structures["operations"].values() if "output" in op]
sqs_top_level_shape_names += [op.replace("Result", "Response") for op in sqs_top_level_shape_names]

def get_service(tag):
    if tag in sqs_top_level_shape_names:
        return "sqs"
    return "global"

def get_shape(tag, service):
    if service == "sqs":
        return sqs_structures["shapes"].get(tag) or global_shapes.get(tag)
    return global_shapes.get(tag)