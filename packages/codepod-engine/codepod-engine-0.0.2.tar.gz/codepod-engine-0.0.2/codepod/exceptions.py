class CompilationException(Exception):
    message = "Failed to compile the solution. see error_log for more details."

    def __init__(self, log_path):
        self.error_log = log_path
        super(CompilationException, self).__init__(self.message)


class RunException(Exception):
    message = "Failed to run the solution. see error_log for more details."

    def __init__(self, log_path):
        self.error_log = log_path
        super(RunException, self).__init__(self.message)


class ValidationException(Exception):
    message = "Failed to validate the data. see errror_message for more details."

    def __init__(self, error_message):
        self.error_message = error_message
        super(ValidationException, self).__init__(self.message)
