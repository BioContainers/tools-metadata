from ruamel.yaml import YAML
from urlextract import URLExtract
import urllib

import re
from collections import OrderedDict

"""
This script tries to detect keywords in the tool urls. 
"""


def doi_from_text(text, words):
    results = []
    for word in words:
        if word.lower() in text:
            results.append(word)
    return results

def retrieve_doi(url, words):
    with urllib.request.urlopen(url) as url:
        s = url.read().decode('utf-8').lower()
    return doi_from_text(s, words)

yaml = YAML()
yaml_recipe = YAML(typ="rt")  # pylint: disable=invalid-name
with open('../annotations.yaml', 'r') as read_file:
    file_annotations = yaml.load(read_file)

tools = {}

words = ['Clustering', 'Cluster Analysis', 'Proteomics', 'Genomics', 'Peptides', 'Mass spectra', 'Mass spectrometry', 'Metabolomics', 'Metaproteomics', 'Metagenomics', 'Whole genome sequencing', 'RNA-Seq', 'Data visualisation', 'Molecular Dynamics',
         'Transcriptomics', 'Functional genomics', 'Phylogenetics', 'Gene Expression', 'Sequence Alignment', 'Genetics', 'Genetic variation', 'Metagenome', 'Gene Expression', 'Markov Chains', 'Protein Structure', 'Transcription Factors', 'Transcriptome', 'Molecular Imaging']

### Annotate bioconductor package
for key in file_annotations:
    tool = file_annotations[key]
    url = tool['home_url']
    keywords = tool['keywords']
    try:
        dois = retrieve_doi(url, words)
        for a in dois:
            keywords.append(a)
        keywords = list(dict.fromkeys(keywords))
        print(keywords)
    except Exception:
        print(key + " --- error")

    tool['keywords'] = keywords
    tools[key] = tool


yaml.indent(mapping=4, sequence=6, offset=2)
with open('missing_annotations.yaml', 'w') as outfile:
    yaml.dump(tools, outfile)
