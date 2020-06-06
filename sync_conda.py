import os

from ruamel.yaml import YAML
from jinja2 import Environment


yaml = YAML(typ='safe')
with open('annotations.yaml', 'r') as read_file:
    file_annotations = yaml.load(read_file)

recipes_path = "../bioconda-recipes/recipes/"
tools = {}
for key in file_annotations:
    tool = file_annotations[key]
    if(os.path.exists(recipes_path + key + "/meta.yaml")) and 'manually_check' not in tool:
        print("Conda -- " + key)
        with open(recipes_path + key + "/meta.yaml", 'r') as conda_file:
            try:
                yaml_content = yaml.load(Environment().from_string(conda_file.read()).render())
                if tool['description'] is None or len(tool['description']) == 0:
                    tool['description'] = yaml_content['about']['summary']
            except:
                print("Error reading conda definition of tool -- " + key)
    tools[key] = tool

# writing missing

yaml.indent(mapping=4, sequence=6, offset=3)
with open('missing_annotations.yaml', 'w') as outfile:
    yaml.dump(tools, outfile)