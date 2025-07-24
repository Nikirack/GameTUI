import re

def parse_vdf(content):
    def parse_block(lines):
        result = {}
        key = None

        while lines:
            line = lines.pop(0).strip()

            if not line or line.startswith("//"):
                continue

            matches = re.findall(r'"(.*?)"', line)

            if line == "{":
                if key is None:
                    raise ValueError("Block opened without key")
                result[key] = parse_block(lines)
                key = None

            elif line == "}":
                return result

            elif len(matches) == 1:
                key = matches[0]

            elif len(matches) == 2:
                k, v = matches
                result[k] = v
                key = None

            else:
                continue

        return result

    return parse_block(content.splitlines())
