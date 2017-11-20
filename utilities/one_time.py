""" Couple of functions for one-time usage e.g. debugging
"""


def print_qml_tree(root):
    """ Prints the structure of qml

    Uses depth-first search
    """

    parameters = root.objectName()
    print("Object: {} , object name: {}".format(root, parameters))
    for child in root.children():
        print_qml_tree(child)