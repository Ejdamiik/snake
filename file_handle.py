def get_content(path):

    with open(path, "r") as f:
        content = f.read()

    return content


def save_content(path, content):

    with open(path, "w") as f:
        f.write(content)
