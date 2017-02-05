

swagger_config = {
    "swagger_version": "2.0",
    "title": "Warehouse",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        ('Access-Control-Allow-Credentials', "true"),
    ],
    "specs": [
        {
            "version": "0.0.1",
            "title": "Api v1",
            "endpoint": 'v1_spec',
            "description": 'This is the version 1 of our API',
            "route": '/api/doc',
            # rule_filter is optional
            # it is a callable to filter the views to extract
            "rule_filter": lambda rule: rule.endpoint.startswith(
                'should_be_v1_only'
            )
        }
    ]
}