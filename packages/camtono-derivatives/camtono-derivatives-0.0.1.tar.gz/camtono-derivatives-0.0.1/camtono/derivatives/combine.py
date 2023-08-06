def generate_derivative(definition: dict, feature_map: dict) -> tuple:
    """Create a derived query ast based on a definition and map of all used features

    :param definition: camtono derivative definition
    :param feature_map:
    :return:
    """
    from camtono.derivatives.filters import flatten_filters, generate_filter_query_sets
    from camtono.derivatives.dependencies import inject_feature_dependencies
    from camtono.derivatives.prune import prune_ast
    flattened_filters = flatten_filters(filters=definition.get('filters', dict()),
                                        default_filters=definition.get('default_filters', []))
    complete_feature = {
        k: inject_feature_dependencies(feature=v, feature_map=feature_map) for k, v in
        feature_map.items()
    }
    query_sets, variables = generate_filter_query_sets(flattened_filters=flattened_filters, features=complete_feature)
    derived_ast = generate_query_skeleton(query_sets=query_sets)
    variables['grain'] = definition['grain']
    return prune_ast(json=derived_ast), variables


def generate_query_skeleton(query_sets):
    base_query = {'with': [], 'from': {}, 'select': [{"value": {"literal": "{grain}"}}]}
    union = []
    # TODO handle default input
    for idx, query_set in enumerate(query_sets):
        name = "sub_filter_{}".format(idx)
        sub_ast = {"select": [{"value": "f" + str(idx) + "t0.{grain}"}], "from": []}
        for query_idx, query in enumerate(query_set):
            from_ = dict(
                value=query,
                name='f{filter_index}t{query_index}'.format(
                    filter_index=idx, query_index=query_idx
                )
            )
            if sub_ast['from']:
                sub_ast['from'].append(dict(join=from_, using='{grain}'))
            else:
                sub_ast['from'].append(from_)
        base_query['with'].append({"value": sub_ast, "name": name})
        union.append({"select": [{"value": {"literal": "{grain}"}}], "from": [dict(name=name, value=name)]})
    base_query['from']['union_distinct'] = union
    return base_query
