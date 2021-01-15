import requests


def main():
    i = 0
    while True:
        url = "https://api.biocontainers.pro/ga4gh/trs/v2/tools?limit=1000&offset=" + str(i)
        # print(url)
        resp = requests.get(url)
        if resp.status_code == 204:
            break
        if resp.status_code == 200:
            tools = resp.json()
            if len(tools) == 0:
                break
            for tool in tools:
                if 'tool_tags' not in tool:
                    tool['tool_tags'] = []
                print(tool['id'] + "\t" + str(tool['pulls']) + "\t" + ','.join(tool['tool_tags']))
            i = i + 1000


if __name__ == "__main__":
    main()
