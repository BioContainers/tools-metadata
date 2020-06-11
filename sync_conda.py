import os
import urllib

from bioconda_utils import recipe
from ruamel.yaml import YAML
import urllib3
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

### Annotate bioconductor package
for key in file_annotations:
    tool = file_annotations[key]

    bioconda_recipes_path = os.path.split(recipes_path)[0]
    meta_yaml_path = "%s/%s/meta.yaml" % (recipes_path, key)
    try:
        current_recipe = recipe.Recipe.from_file(recipes_path, meta_yaml_path)
        if 'about' in current_recipe.meta:
            if 'summary' in current_recipe.meta['about'] and (
                    tool['description'] is None or len(tool['description']) == 0):
                tool['description'] = current_recipe.meta['about']['summary']
            if 'license' in current_recipe.meta['about'] and (tool['license'] is None or len(tool['license']) == 0):
                tool['license'] = current_recipe.meta['about']['license']
            if 'home' in current_recipe.meta['about'] and (tool['home_url'] is None or len(tool['home_url']) == 0):
                tool['home_url'] = current_recipe.meta['about']['home']
        if 'extra' in current_recipe.meta:
            if 'identifiers' in current_recipe.meta['extra']:
                tool["identifiers"] = current_recipe.meta['extra']["identifiers"]
    except Exception as e:
        try:
            bioconda_recipes_path = os.path.split(recipes_path)[0]
            versions = next(os.walk(bioconda_recipes_path + "/" + key + '/.'))[1]
            version = versions[len(versions) - 1]
            bioconda_recipes_path = bioconda_recipes_path + "/" + key + "/" + version
            meta_yaml_path = bioconda_recipes_path + "/meta.yaml"
            current_recipe = recipe.Recipe.from_file(recipes_path, meta_yaml_path)
            if 'about' in current_recipe.meta:
                if 'summary' in current_recipe.meta['about'] and (tool['description'] is None or len(tool['description']) ==0):
                    tool['description'] = current_recipe.meta['about']['summary']
                if 'license' in current_recipe.meta['about'] and (tool['license'] is None or len(tool['license']) ==0):
                    tool['license'] = current_recipe.meta['about']['license']
                if 'home' in current_recipe.meta['about'] and (tool['home_url'] is None or len(tool['home_url']) ==0):
                    tool['home_url'] = current_recipe.meta['about']['home']
            if 'extra' in current_recipe.meta:
                if 'identifiers' in current_recipe.meta['extra']:
                    tool["identifiers"] = current_recipe.meta['extra']["identifiers"]

        except Exception as e:
            print("Error reading -- " + key + " Error -- " + str(e))

        if 'bioconductor' in key:
            key_bio = key.replace("bioconductor-", "")
            url = "https://www.bioconductor.org/packages/release/bioc/html/" + key_bio + ".html"
            try:
                with urllib.request.urlopen(url) as url:
                    s = url.read()
                    tool['home_url'] = key_bio
                    print(s)

            except Exception as e:
                print("Error reading -- " + key + " Error -- " + str(url))

            print(tool['home_url'])
    tools[key] = tool

# writing missing

yaml.indent(mapping=4, sequence=6, offset=2)
with open('annotations.yaml.previous.previous', 'w') as outfile:
    yaml.dump(tools, outfile)