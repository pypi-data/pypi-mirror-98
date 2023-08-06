"""Mock is a service providing REST API configurable by REST API."""


class MockException(Exception):
    """Exception from Mock service."""


class RouteConfigurationError(MockException, ValueError):
    """Raised when route could not be configured because of value error."""


class AuthenticationError(MockException):
    """Exception raised when user could not be authenticated."""
