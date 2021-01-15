import requests


def main():
    offset = 0
    while True:
        limit = 1000
        url = "https://api.biocontainers.pro/ga4gh/trs/v2/tools?limit=" + str(limit) + "&offset=" + str(offset)
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
            offset = offset + limit


if __name__ == "__main__":
    main()
