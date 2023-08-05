# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['starlette_graphene3']
install_requires = \
['graphene>=3.0b6', 'starlette>=0.14.1,<0.15.0']

setup_kwargs = {
    'name': 'starlette-graphene3',
    'version': '0.3.0',
    'description': 'Use Graphene v3 on Starlette',
    'long_description': '# starlette-graphene3\n\nA Simple ASGI app for using [Graphene](https://github.com/graphql-python/graphene) v3 with [Starlette](https://github.com/encode/starlette).\n\n![Test](https://github.com/ciscorn/starlette-graphene3/actions/workflows/test.yml/badge.svg?branch=master)\n[![codecov](https://codecov.io/gh/ciscorn/starlette-graphene3/branch/master/graph/badge.svg)](https://codecov.io/gh/ciscorn/starlette-graphene3)\n\nIt supports:\n\n- Queries and Mutations (over HTTP or WebSocket)\n- Subscriptions (over WebSocket)\n- File uploading (https://github.com/jaydenseric/graphql-multipart-request-spec)\n- GraphQL Playground\n\n\n## Installation\n\n```bash\npip3 install -U starlette-graphene3\n```\n\n\n## Example\n\n```python\nimport asyncio\n\nimport graphene\nfrom graphene_file_upload.scalars import Upload\n\nfrom starlette.applications import Starlette\nfrom starlette_graphene3 import GraphQLApp\n\n\nclass User(graphene.ObjectType):\n    id = graphene.ID()\n    name = graphene.String()\n\n\nclass Query(graphene.ObjectType):\n    me = graphene.Field(User)\n\n    def resolve_me(root, info):\n        return {"id": "john", "name": "John"}\n\n\nclass FileUploadMutation(graphene.Mutation):\n    class Arguments:\n        file = Upload(required=True)\n\n    ok = graphene.Boolean()\n\n    def mutate(self, info, file, **kwargs):\n        return FileUploadMutation(ok=True)\n\n\nclass Mutation(graphene.ObjectType):\n    upload_file = FileUploadMutation.Field()\n\n\nclass Subscription(graphene.ObjectType):\n    count = graphene.Int(upto=graphene.Int())\n\n    async def subscribe_count(root, info, upto=3):\n        for i in range(upto):\n            yield i\n            await asyncio.sleep(1)\n\n\napp = Starlette()\nschema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)\napp.mount("/", GraphQLApp(schema, playground=True))\n```\n',
    'author': 'Taku Fukada',
    'author_email': 'naninunenor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ciscorn/starlette-graphene3',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
