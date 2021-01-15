import requests


def main():
    offset = 0
    limit = 1000
    tool_version_url = "https://api.biocontainers.pro/ga4gh/trs/v2/tools/{tool_id}/versions"
    while True:
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
                tool_version_url = tool_version_url.format(tool_id=tool['id'])
                vresp = requests.get(tool_version_url)
                tool_versions = vresp.json()
                for tool_version in tool_versions:
                    for image in tool_version['images']:
                        if 'downloads' not in image:
                            image['downloads'] = 0
                        print(tool['id'] + "\t" + tool_version['id'] + "\t" + image['image_type'] + "\t" +
                              image['image_name'] + "\t" + str(image['downloads']))

            offset = offset + limit


if __name__ == "__main__":
    main()
