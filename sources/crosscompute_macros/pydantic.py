def get_schema_dictionary(schema):
    return schema.model_dump(mode='json', exclude_defaults=True)
