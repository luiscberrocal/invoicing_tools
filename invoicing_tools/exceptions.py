class InvoicingToolsException(Exception):
    pass


class ConfigurationError(InvoicingToolsException):
    pass


class UploadError(Exception):
    pass

class ConversionError(InvoicingToolsException):
    pass
