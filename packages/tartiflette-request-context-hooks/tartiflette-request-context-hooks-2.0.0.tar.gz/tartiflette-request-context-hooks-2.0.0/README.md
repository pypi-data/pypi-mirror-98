# Tartiflette Request Context Hooks

DEPRECATED, MOVED TO [tartiflette-middleware](https://github.com/daveoconnor/tartiflette-middleware/).

Framework to facilitate the creation of per-request context data for your
resolvers using simple python context managers. 

Allows for processing of request/response headers, dependent on the
http server you're using.

Deprecated only because that name suits better.

## Installation

```bash
pip install tartiflette-request-context-hooks
```

## Usage
This requires:
1. Creation of your hooks.
1. Configuration of your hooks in your application.
1. Update your resolvers to access your data.

### 1 - Creation of your hooks
Create a context manager to run on each request.

Example:

```python
from tartiflette_request_contexts_hooks import BaseRequestContextHooks

class MyContextHooks(BaseRequestContextHooks):
    # required short arbitrary unique hook label
    label = 'MyHk'
    
    def __init__(self, my_hook_params):
        BaseRequestContextHooks.__init__(self)
        # do things necessary for repeated use across all of the requests, e.g.
        # configure factories

    async def __aenter__(self):
        # provide the data or method to be used in all queries for a single
        # request. 
        your_method_or_data = ...
        # store the data/method to be reused for this request
        await self.store_request_data(your_method_or_data)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # optional: for if you need to do something when the request is
        # completed
        data = await self.get_request_data()
        data.close_or_whatever()
```

There are more examples in the examples directory including one with access to
AIOHTTP request headers.

### 2 - Configuration of your hooks in your app

Currently only AIOHTTP is supported but the library is extensible if others
would like to submit a pull request to support other servers that Tartiflette
supports.

Limited AIOHTTP setup example, imports and configuration kept to hook specific
details:

```python
from tartiflette_request_context_hooks.middleware import aiohttp
from tartiflette_request_context_hooks import RequestContextHooks
import MyContextHooks # your hook

my_hook = RequestContextHooks(
     context_manager=MyContextHooks(
          my_hooks_params={},
     ),
     server_middleware=aiohttp    
)

app = web.Application(middlewares=[
    my_hook.middleware
])
ctx = {
    'my_session_service': my_hook.service,
}
web.run_app(
    register_graphql_handlers(
        # your configuration
        executor_context=ctx,
    )
)
```

### 3 - Access data in your resolvers' context

Works in queries, mutations, and subscriptions.

```python
@Resolver('Query.whatever')
async def resolve_query_user_login(parent, args, ctx, info):
    my_data = await ctx['my_session_service']()
```
