class RequestContextHooks:
    def __init__(self, context_manager, server_middleware):
        """
        :param BaseRequestContextHooks Your custom hook
        :param package Middleware from the middleware package
        """
        self._service = context_manager
        self._middleware = server_middleware.get_hooks_service_middleware(
            context_service=self.service,
        )

    @property
    def service(self):
        return self._service

    @property
    def middleware(self):
        return self._middleware
