DOC_URL = ""


class ResponseError(Exception):
    doc_url = None

    type = None

    def __init__(self, message, type, docUrl=""):
        super().__init__(message)
        if len(docUrl) > 0:
            self.doc_url = docUrl
        else:
            self.doc_url = "{}/{}".format(DOC_URL, type)
        self.type = type


class ParameterValidationError(ResponseError, Exception):
    def __init__(self, **error):
        super().__init__(type="parameter-validation-error", **error)
