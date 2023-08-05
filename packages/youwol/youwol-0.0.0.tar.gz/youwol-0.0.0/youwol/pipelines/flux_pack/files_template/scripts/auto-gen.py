import json
import base64


def parse_package(filepath):
    r = {}
    with open(filepath, 'r') as package_file:
        json_data = json.load(package_file)
        r["version"] = json_data['version']

        r["id"] = json_data["name"].split("/")[-1]
        r["fullname"] = json_data["name"]
        r["name"] = json_data["name"].split("/")[-1]

        if '/' in json_data["name"]:
            namespace = json_data["name"].split("/")[0]
            namespace = namespace[1:] if namespace[0] == '@' else namespace
            r["namespace"] = namespace

        if "displayName" in json_data:
            r["displayName"] = json_data["displayName"]
        else:
            r["displayName"] = json_data["name"]

        r["description"] = json_data["description"]
        r["author"] = json_data["author"]
        r["tags"] = json_data["keywords"]
    return r


parsed = parse_package("./package.json")
fullname = str(parsed["fullname"])
asset_raw_id = base64.urlsafe_b64encode(str.encode(fullname)).decode()

with open('src/auto-generated.ts', 'w') as file:
    file.write("// This file is auto-generated: do not edit \n")
    file.write("export const ID = '{}' \n".format(asset_raw_id))
    file.write("export const NAME = '{}' \n".format(parsed["name"]))
    file.write("export const DISPLAY_NAME = '{}' \n".format(parsed["displayName"]))
    file.write("export const VERSION = '{}' \n".format(parsed["version"]))
    file.write("export const DESCRIPTION = '{}' \n".format(parsed["description"]))
