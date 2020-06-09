import os

from bioconda_utils import recipe
from ruamel.yaml import YAML

from bioconda_utils.recipe import (
    Recipe,
    EmptyRecipe, MissingMetaYaml, RenderFailure, DuplicateKey, MissingKey
)

yaml = YAML()
yaml_recipe = YAML(typ="rt")  # pylint: disable=invalid-name
with open('annotations.yaml', 'r') as read_file:
    file_annotations = yaml.load(read_file)

recipes_path = "../bioconda-recipes/recipes/"
tools = {}


def read_template(conda_file):
    # data = {}
    # for cnt, line in enumerate(conda_file):
    #     print("Line {}: {}".format(cnt, line))
    #     if 'summary:' in line:
    #         data['description'] = line.replace("summary:", "").strip()
    #     if 'license:' in line:
    #         data['license'] = line.replace("license:", "").strip()
    #     if 'home:' in line:
    #         line = line.replace("home:", "")
    #         data['home'] = line.strip()

    return data


for key in file_annotations:
    tool = file_annotations[key]

    bioconda_recipes_path = os.path.split(recipes_path)[0]
    meta_yaml_path = "%s/%s/meta.yaml" % (recipes_path, key)
    try:
        current_recipe = recipe.Recipe.from_file(recipes_path, meta_yaml_path)
        if 'about' in current_recipe.meta:
            if 'summary' in current_recipe.meta['about']:
                tool['description'] = current_recipe.meta['about']['summary']
            if 'license' in current_recipe.meta['about']:
                tool['license'] = current_recipe.meta['about']['license']
            if 'home' in current_recipe.meta['about']:
                tool['home_url'] = current_recipe.meta['about']['home']
        if 'extra' in current_recipe.meta:
            if 'identifiers' in current_recipe.meta['extra']:
                tool["identifiers"] = current_recipe.meta['extra']["identifiers"]
        tools[key] = tool
    except Exception as e:
        try:
            bioconda_recipes_path = os.path.split(recipes_path)[0]
            versions = next(os.walk(bioconda_recipes_path + "/" + key + '/.'))[1]
            version = versions[len(versions) - 1]
            bioconda_recipes_path = bioconda_recipes_path + "/" + key + "/" + version
            meta_yaml_path = bioconda_recipes_path + "/meta.yaml"
            current_recipe = recipe.Recipe.from_file(recipes_path, meta_yaml_path)
            if 'about' in current_recipe.meta:
                if 'summary' in current_recipe.meta['about']:
                    tool['description'] = current_recipe.meta['about']['summary']
                if 'license' in current_recipe.meta['about']:
                    tool['license'] = current_recipe.meta['about']['license']
                if 'home' in current_recipe.meta['about']:
                    tool['home_url'] = current_recipe.meta['about']['home']
            if 'extra' in current_recipe.meta:
                if 'identifiers' in current_recipe.meta['extra']:
                    tool["identifiers"] = current_recipe.meta['extra']["identifiers"]
                tools[key] = tool
        except Exception as e:
            print("Error reading -- " + key + " Error -- " + str(e))





# writing missing

yaml.indent(mapping=4, sequence=6, offset=3)
with open('missing_annotations.yaml', 'w') as outfile:
    yaml.dump(tools, outfile)