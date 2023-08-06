def inject_feature_dependencies(feature, feature_map) -> dict:
    """

    :param feature:
    :param feature_map:
    :return:
    """
    from camtono.derivatives.prune import set_tree_value

    for dependency in feature.get('dependencies', []):
        feature['query_ast'] = set_tree_value(json=feature['query_ast'], locations=dependency['locations'],
                                              val=feature_map[dependency['id']]['query_ast'])
        # TODO update inputs location
        feature['inputs'] += dependency['inputs']
    return feature
