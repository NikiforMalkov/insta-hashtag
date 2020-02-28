# TODO: обдумать куда это перенести или сделать менее трудозатратный вариант
def get_url_collection(href: str):
    collection = str(href).split(",")
    trash_collection = [
        "amp;", " 640w", " 480w", " 320w", " 240w", " 150w"
    ]
    for i in range(0, len(collection)):
        for j in range(0, len(trash_collection)):
            collection[i] = str(collection[i]).replace(trash_collection[j], "")
    # print(collection)
    return collection
