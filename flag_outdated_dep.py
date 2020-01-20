import re, sys, json, requests

direct_dep_pattern = re.compile(
    r'\[INFO\]\s[\+\\]\-\s+(?P<group_id>[^\:]+)\:(?P<artifact_id>[^\:]+)\:(?P<package>[^\:]+)\:(?P<version>[^\:]+)(\:.+)?$')

fields = ['group_id', 'artifact_id', 'package', 'version']

search_query = \
    r'https://search.maven.org/solrsearch/select?q=g:{group_id}%20AND%20a:{artifact_id}%20AND%20p:{package}&wt=json'


# Find if we received a multi-line non-escaped file or single line escaped file
def read_lines(data):
    return data.split('\n')


def list_dependencies(source):
    lines = list()
    with open(source, 'r') as f:
        data = f.read()
        lines = read_lines(data)
        lines = [x for x in lines if (x and direct_dep_pattern.match(x))]
        elements = list()
        for line in lines:
            mm = direct_dep_pattern.search(line)
            if mm is not None:
                entry = dict()
                matched = mm.groupdict()
                for field in fields:
                    entry[field] = matched[field]
                uri = search_query.format(**entry)
                result = json.loads(requests.get(uri).content.decode("UTF-8"))
                docs = result['response']['docs']
                if docs:
                    latest_version = docs[0]['latestVersion']
                    elements.append(
                        {
                            "declared": entry,
                            "uri": uri,
                            "latest_version": latest_version,
                            "is_latest": latest_version == entry['version']
                        }
                    )
                else:
                    elements.append(
                        {
                            "declared": entry,
                            "uri": uri,
                            "latest_version": "unknown",
                            "error": "component not found in maven database"
                        }
                    )
    return json.dumps(elements, indent=4)


if __name__ == "__main__":
    print(list_dependencies(sys.argv[1])) if (len(sys.argv) == 2) else sys.exit(
        "Incorrect number of arguments (1 expected)")

