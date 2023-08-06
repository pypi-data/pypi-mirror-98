def prune_ast(json, parent=None):
    """

    :param json:
    :param parent:
    :return:
    """
    pruned = type(json)()
    if isinstance(json, dict):
        for k, v in json.items():
            child = prune_ast(json=v, parent=k)
            if child:
                pruned[k] = child
        pruned = validate_tree(k=parent, json=pruned)
    elif isinstance(json, list):
        for v in json:
            child = prune_ast(json=v, parent=None)
            if child:
                pruned.append(child)
        pruned = validate_tree(k=parent, json=pruned)
    else:
        if json is not None:
            pruned = json
    return pruned


def validate_tree(k, json):
    """

    :param k:
    :param json:
    :return:
    """
    from camtono.parser.parse import min_keys
    if k is None or len(json) >= min_keys.get(k, 1):
        return json
    else:
        return None


def set_tree_value(json, locations, val=None, replace_func=None):
    if locations:
        for k, v in locations.items():
            if k.isdigit():
                k = int(k)
            json[k] = set_tree_value(json=json[k], locations=v, val=val, replace_func=replace_func)
        return json
    else:
        if replace_func is not None:
            return replace_func(json=json)
        else:
            return val


def trim_feature_input(feature: dict, variables: dict, default_variables: dict, prefix: str = None) -> tuple:
    """Remove all unnecessary query input from the query_ast

    :param feature: feature dict
    :param variables: dict of variables used for string formatting
    :return: feature dict with cleaned query_ast
    """
    import functools
    from copy import deepcopy
    clean_variables = dict()
    ast = deepcopy(feature['query_ast'])

    for query_input in feature['inputs']:
        if query_input['name'] not in variables.keys() and query_input['name'] not in default_variables:
            ast = set_tree_value(json=ast, locations=query_input['locations'],
                                 val=None)
        elif query_input['name'] not in default_variables:
            new_variable_name = query_input['name'] if not prefix else prefix + query_input['name']
            replace_func = functools.partial(
                    replace_input_string, old_string=query_input['name'],
                    new_string=new_variable_name
                )
            ast = set_tree_value(
                json=ast, locations=query_input['locations'],
                replace_func=replace_func
            )
            clean_variables[new_variable_name] = variables[query_input['name']]['value']
        else:
            clean_variables[query_input['name']] = default_variables[query_input['name']]
    return ast, clean_variables


def replace_input_string(json, old_string, new_string):
    return json.replace(old_string, new_string)
