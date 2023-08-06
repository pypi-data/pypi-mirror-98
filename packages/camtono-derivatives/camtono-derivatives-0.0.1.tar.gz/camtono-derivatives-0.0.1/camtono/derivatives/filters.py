def flatten_filters(filters: dict, default_filters: dict) -> tuple:
    """

    :param filters:
    :param default_filters:
    :return:
    """
    new_filters = filters
    if default_filters:
        new_filters = dict(filters=[filters, default_filters], item='and')
    flattened_filters = flatten_filter(filters=new_filters)
    return flattened_filters


def flatten_filter(filters, list_string='filters', operator_string='item'):
    """Flattens nested pyparser syntax into a single layer

    :param filters:
    :param list_string:
    :param operator_string: string key of the pyparser operator
    :return: flatted list of lists of base operators
    """
    flattened_filter = list()
    operator = filters[operator_string].lower()
    for idx, i in enumerate(filters[list_string]):
        new_filters = i
        if isinstance(i.get(list_string), list):
            new_filters = flatten_filter(filters=i, list_string=list_string, operator_string=operator_string)
        flattened_filter = unify_sets(existing=flattened_filter, new=new_filters, operator=operator)
    return flattened_filter


def unify_sets(existing, new, operator):
    """Join two sets of statements based on boolean operator

    :param existing: List of existing statements
    :param new: New statements to add to the set
    :param operator: boolean operator and, or, not
    :return: combined set of sets based on boolean operation
    """
    import itertools
    unified = []
    if isinstance(new, dict):
        new = [new]
    if not isinstance(new[0], list):
        new = [new]
    if not existing and operator in ['and', 'or']:
        unified = new
    elif operator == 'or':
        unified = existing + new
    elif operator == 'and':
        if existing:
            for a, b in itertools.product(existing, new):
                unified.append([*a, *b])
        else:
            unified.append(new)
    elif operator == 'not':
        for s in new:
            subset = []
            for x in s:
                x['not'] = bool(-x.get('not', False))
                subset = unify_sets(existing=subset, new=x, operator='or')
            unified = unify_sets(existing=unified, new=subset, operator='and')
    return unified


def generate_filter_query_sets(flattened_filters, features):
    from camtono.derivatives.prune import trim_feature_input
    query_sets, variables = [], dict()
    for idx, filter_set in enumerate(flattened_filters):
        set_features, skip = define_set_features(filter_set=filter_set)
        query_set = []
        for feature, filters in features.items():
            ast, feature_variables = trim_feature_input(
                feature=features[feature], variables=set_features[feature],
                prefix='s{}'.format(idx), default_variables=dict(grain='a')
            )
            query_set.append(ast)
            variables.update(feature_variables)
        if not skip:
            query_sets.append(query_set)
    return query_sets, variables


def define_set_features(filter_set):
    features = dict()
    skip = False
    for f in filter_set:
        if skip:
            continue
        if f['feature'] not in features.keys():
            features[f['feature']] = dict()
        if f['attribute'] not in features[f['feature']].keys():
            features[f['feature']][f['attribute']] = {'not': f.get('not', False), 'value': f['value']}
    return features, skip
