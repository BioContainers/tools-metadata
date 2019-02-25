import os
import requests

BIO_TOOLS_API="https://bio.tools/api/tool/%s&format=json"
BIO_TOOLS_TOOL_API="https://bio.tools/api/tool/%s/?format=yaml"


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
        response = requests.get(tools_url, headers={"Content-Type": "application/json"})
        with open(id + '/descriptor.yaml', 'wb') as f:
            f.write(response.content)
    print("Processing -- " + id)


def main():
    current_page="?page=1"
    tools_url = BIO_TOOLS_API.replace("%s", current_page)
    response = requests.get(tools_url, headers={"Content-Type": "application/json"})

    data = response.json()
    print(len(data['list']))

    while(data['next'] != None):
        for index in range(len(data['list'])):
            sync_tool(data['list'][index])

        tools_url = BIO_TOOLS_API.replace("%s", data['next'])
        response = requests.get(tools_url, headers={"Content-Type": "application/json"})
        data = response.json()
        print(len(data['list']))



if __name__ == "__main__":
    main()