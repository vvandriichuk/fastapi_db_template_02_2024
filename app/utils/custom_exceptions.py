class ConfigValidationError(Exception):
    """Exception raised when configuration validation fails."""
    def __init__(self, message: str):
        super().__init__(message)