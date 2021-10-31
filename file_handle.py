def get_content(path):
    """
    returns content of file at path
    """
    with open(path, "r") as f:
        content = f.read()

    return content


def save_content(path, content):
    """
    Saves content to path
    """

    with open(path, "w") as f:
        f.write(content)
