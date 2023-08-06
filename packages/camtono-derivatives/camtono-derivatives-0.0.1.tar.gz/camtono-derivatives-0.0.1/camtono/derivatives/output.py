def finalize_query(base_ast, transforms, output) -> dict:
    """

    :param base_ast:
    :param transforms:
    :param output:
    :return:
    """
    base_ast['select'] = [{'literal': '{grain}'}]
    return base_ast



