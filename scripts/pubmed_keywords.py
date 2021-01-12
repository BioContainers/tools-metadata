from metapub import PubMedFetcher
from metapub.convert import doi2pmid
from ruamel.yaml import YAML
top_words = ['Algorithms', 'Software']

"""
The following script will read doi accessions in the identifiers section of the tool and find the pubmed accession of corresponding to it. 
Finally, if the pubmed accession is found, the script will look for mesh keywords associated with the publications and added to the tool_tags. 
"""

yaml = YAML()
yaml_recipe = YAML(typ="rt")  # pylint: disable=invalid-name
with open('../annotations.yaml', 'r') as read_file:
    file_annotations = yaml.load(read_file)

tools = {}

for key in file_annotations:
    tool = file_annotations[key]

    if 'identifiers' in tool and ('keywords' not in tool or len(tool['keywords'])==0) :
        identifiers = tool['identifiers']
        for identifier in identifiers:
            try:
                if 'doi' in identifier:
                    doi = identifier.replace('doi:', '')
                    pubmedid = doi2pmid(doi)
                    print('doi: ' + doi + ' --> ' + 'pmid: ' + pubmedid)
                    if pubmedid is not None:
                        fetch = PubMedFetcher()
                        article = fetch.article_by_pmid(pubmedid)
                        if article.mesh is not None:
                            keywords = []
                            if 'keywords' in tools:
                                keywords = tool['keywords']
                            for keyword_key in article.mesh:
                                keyword = article.mesh[keyword_key]
                                if keyword['descriptor_name'] not in top_words:
                                    keywords.append(keyword['descriptor_name'])
                            keywords = list(dict.fromkeys(keywords))
                            tool['keywords'] = keywords
                        print(article.mesh)
            except Exception as e:
                print('Error doi --' + doi)

    tools[key] = tool

yaml.indent(mapping=4, sequence=6, offset=2)
with open('missing_annotations.yaml', 'w') as outfile:
    yaml.dump(tools, outfile)