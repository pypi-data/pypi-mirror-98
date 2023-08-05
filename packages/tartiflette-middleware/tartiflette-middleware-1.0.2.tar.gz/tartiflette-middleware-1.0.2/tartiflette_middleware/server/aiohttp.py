from aiohttp.web import middleware


def get_hooks_service_middleware(*, context_service):
    """
    params: context_service BaseMiddleware
    """
    @middleware
    async def manager(request, handler):
        context_service.request = request
        context_service.handler = handler
        async with context_service:
            return await handler(request)
    return manager
