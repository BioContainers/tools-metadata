import os

from ruamel.yaml import YAML


yaml = YAML()
with open('annotations.yaml.072020', 'r') as read_file:
    file_annotations = yaml.load(read_file)

recipes_path = "../bioconda-recipes/recipes/"
tools = {}


def read_template(conda_file):
    data = {}
    for cnt, line in enumerate(conda_file):
        print("Line {}: {}".format(cnt, line))
        if 'summary:' in line:
            data['description'] = line.replace("summary:", "").strip()
        if 'license:' in line:
            data['license'] = line.replace("license:", "").strip()
        if 'home:' in line:
            line = line.replace("home:", "")
            data['home'] = line.strip()
    return data


for key in file_annotations:
    tool = file_annotations[key]
    if(os.path.exists(recipes_path + key + "/meta.yaml")) and 'manually_check' not in tool:
        print("Conda -- " + key)
        with open(recipes_path + key + "/meta.yaml", 'r') as conda_file:
            data = read_template(conda_file)
            if 'description' in data and (tool['description'] is None or len(tool['description']) == 0):
               tool['description'] = data['description']
               check = True
            if 'license' in data and (tool['license'] is None or len(tool['license']) == 0):
               tool['license'] = data['license']
            if 'home' in data and (tool['home_url'] is None or len(tool['home_url']) == 0):
                tool['home_url'] = data['home']

    tools[key] = tool

# writing missing

yaml.indent(mapping=4, sequence=6, offset=3)
with open('missing_annotations.yaml', 'w') as outfile:
    yaml.dump(tools, outfile)