import os
import requests
from ratelimit import limits, sleep_and_retry
# import ruamel.yaml
import json
import yaml


BIO_TOOLS_API="https://bio.tools/api/tool/%s&format=json"
BIO_TOOLS_TOOL_API="https://bio.tools/api/tool/%s/?format=json"


FIFTEEN_MINUTES = 60


@sleep_and_retry
@limits(calls=1000, period=FIFTEEN_MINUTES)
def call_api(url):
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    return response


class MyDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


def sync_tool(tool):
    """
    This function allows to download the specific content for a tool.
    :param tool: tool
    :return:
    """
    id = tool['biotoolsID']
    if id is not None:
        if not os.path.exists(id):
            os.mkdir(id)
        tools_url = BIO_TOOLS_TOOL_API.replace("%s", id)
        try:
            response = call_api(tools_url)
            with open(id + '/descriptor.yaml', 'w') as stream:
               json_data = json.loads(response.content.decode('utf-8'))
               yaml.dump(json_data, stream, Dumper=MyDumper, default_flow_style=False)
               print("Processing -- " + id)
        except Exception:
            print("Error processing -- " + id)


def main():
    """
    This function enable to loop over all tools in bio.tools and write into a file ach representation.
    """
    current_page="?page=1"
    tools_url = BIO_TOOLS_API.replace("%s", current_page)
    response = requests.get(tools_url, headers={"Content-Type": "application/json"})

    data = response.json()
    count = 0; 

    while(data['next'] != None):
        for index in range(len(data['list'])):
            sync_tool(data['list'][index])
        count = count + len(data['list'])
        print("Number of tools processed -- " + str(count))

        tools_url = BIO_TOOLS_API.replace("%s", data['next'])
        response = call_api(tools_url)
        data = response.json()
        

if __name__ == "__main__":
    main()