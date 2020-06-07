import os

from ruamel.yaml import YAML


yaml = YAML()
with open('annotations.yaml', 'r') as read_file:
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
            check = True
            if 'description' in data:
               tool['description'] = data['description']
               check = True
            if 'license' in data:
               tool['license'] = data['license']
               check = True
            if 'home' in data:
                tool['home_url'] = data['home']
                check = True
            if check:
                tool['manually_check'] = True
    tools[key] = tool

# writing missing

yaml.indent(mapping=4, sequence=6, offset=3)
with open('missing_annotations.yaml', 'w') as outfile:
    yaml.dump(tools, outfile)