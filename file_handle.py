def get_content(path: str) -> str:
    """
    returns content of file at path
    """
    with open(path, "r") as f:
        content = f.read()

    return content


def save_content(path: str, content: str) -> None:
    """
    Saves content to path
    """

    with open(path, "w") as f:
        f.write(content)
