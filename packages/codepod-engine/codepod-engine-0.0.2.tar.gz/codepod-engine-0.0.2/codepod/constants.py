"""
This file has all the constants that are used in
codepod.
"""


class SupportedLanguages:
    """
    This contains all the languages that are
    supported by codepod.
    """

    PYTHON = "python"
    JAVA = "java"

    @classmethod
    def as_list(cls):
        return [
            getattr(cls, attr)
            for attr in dir(cls)
            if not callable(getattr(cls, attr)) and not attr.startswith("__")
        ]


class CompilerPaths:
    """
    This contains all the compiler paths of the
    languages that supported by codepod.
    """

    PYTHON = "/usr/bin/python -m py_compile"
    JAVA = "/usr/bin/javac"


class ExecutorPaths:
    """
    This contains all the executor paths of the
    languages that supported by codepod.
    """

    PYTHON = "/usr/bin/python"
    JAVA = "/usr/bin/java"


class ExecuteTypes:
    """
    This contains all the execution types that are
    supported by codepod.
    """

    COMPILE = "compile"
    RUN = "run"


class QueueConstants:
    QUEUE = "QUEUE_NAME"
    DEFAULT_QUEUE = "codepod_engine"
    HOST = "QUEUE_HOST"
    DEFAULT_HOST = "localhost"
    PORT = "QUEUE_PORT"
    DEFAULT_PORT = "5672"
    USERNAME = "QUEUE_USERNAME"
    DEFAULT_USERNAME = "guest"
    PASSWORD = "QUEUE_PASSWORD"
    DEFAULT_PASSWORD = "guest"


class CodePodEngineStatus:
    """
    This contains all the status that are available in the
    codepod engine.
    """

    COMPILATION_FAIED = "COMPILATION_FAIED"
    RUN_FAILED = "EXECUTION_FAILED"
    SUCCESS = "COMPLETED"
    NOT_PROCESSED = "NOT_PROCESSED"
    ERROR = "INTERNAL_ENGINE_ERROR"
    VALIDATION_FAILED = "INCORRECT_PAYLOAD"
    TIMEOUT = "TIME_LIMIT_EXCEDEED"


LANGUAGE_FILE_EXTENSIONS = {
    SupportedLanguages.PYTHON: "py",
    SupportedLanguages.JAVA: "java",
}
