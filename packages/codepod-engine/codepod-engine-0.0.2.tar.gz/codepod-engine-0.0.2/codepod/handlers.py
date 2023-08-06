"""
Handlers are used to perform the operations that can
be done with the given source files for a particular language.
"""
import os
import shlex
import subprocess

from abc import ABC, abstractmethod
from class_registry import ClassRegistry, RegistryKeyError

from codepod.constants import (
    SupportedLanguages,
    CompilerPaths,
    ExecuteTypes,
    ExecutorPaths,
    LANGUAGE_FILE_EXTENSIONS,
)
from codepod.exceptions import CompilationException, RunException
from codepod.managers import SingleSourceManager


LanguageHandlers = ClassRegistry()


def get_handler_instance(language: str):
    """
    Method that gives the registered handler of the given language.

    Args:
        language: tells the language for which the handler is needed.

    Returns:
        The respective handler instance of the language passed.

    Raises:
        NotImplementedError: raises if a handler is not registered for the
        language.
    """

    try:
        return LanguageHandlers.get(language)
    except RegistryKeyError:
        raise NotImplementedError(
            f"Handler for the language {language} is not registered"
        )


class AbstractHandler(ABC):
    """
    This class is the abstract handler for all the other
    handlers that are available for the supported languages.
    """

    COMPILER = None
    EXECUTOR = None
    TIMEOUT = 60  # the default timeout is 60sec

    def __init__(self):
        if not self.COMPILER:
            raise NameError(
                f"self.COMPILER is not defined in {self.__class__.__name__}"
            )

        if not self.EXECUTOR:
            raise NameError(
                f"self.EXECUTOR is not defined in {self.__class__.__name__}"
            )

    def _execute(
        self,
        command: str,
        manager: SingleSourceManager,
        c_type=ExecuteTypes.COMPILE,
    ):
        """
        Method that execute the given command in the given
        path.

        Args:
            command: command to compile or run the solution.
            manager: SingleSourceManager object that has all the source code details.
            timeout: once the timeout is reached the process will be killed.
            c_type: tells whether the execution type is compilation or run.

        Raises:
            subprocess.TimeoutExpired: raises if the given timeout limit is crossed.
            CompilationException: raises if the solution failes to compile.
            RunException: raises if the solution solution failes to run.
        """
        error_file = open(manager.error_file, "w")

        if c_type == ExecuteTypes.RUN:
            input_file = open(manager.input_file, "w")
            output_file = open(manager.output_file, "w")

            # execute the command passed with the timeout of given time_limit + 2
            subprocess.run(
                shlex.split(command),
                cwd=manager.source_path,
                stdin=input_file,
                stdout=output_file,
                stderr=error_file,
                timeout=self.TIMEOUT + 2,
            )
        else:
            subprocess.run(
                shlex.split(command),
                cwd=manager.source_path,
                stderr=error_file,
                timeout=120,  # 2mins of timeout for compilation
            )

        error_file_stat = os.stat(manager.error_file)

        # if the size of the error file is > 0 it means the program execution failed.
        if error_file_stat.st_size > 0:
            # if the c_type is run its a run exception else its a compile exception.
            if c_type == ExecuteTypes.RUN:
                raise RunException(manager.error_file)
            else:
                raise CompilationException(manager.error_file)

    def set_time_limit(self, time_limit: int):
        """
        This method is to set the timout for the execution of the source code
        binary.

        Args:
            time_limit: the time after which the execution should be killed in
            seconds.
        """
        self.TIMEOUT = time_limit

    @abstractmethod
    def compile(self, manager: SingleSourceManager):
        """
        This method when invoked needs to compile the given source
        code.
        """
        pass

    @abstractmethod
    def run(self, manager: SingleSourceManager):
        """
        This method when invoked needs to run the compiled source code.
        """
        pass


@LanguageHandlers.register(SupportedLanguages.PYTHON)
class PythonHandler(AbstractHandler):
    """
    This is the handler that gets registered for the python
    language.
    """

    COMPILER = CompilerPaths.PYTHON
    EXECUTOR = ExecutorPaths.PYTHON

    def compile(self, manager: SingleSourceManager):
        self._execute(f"{self.COMPILER} {manager.source_file_name}", manager)

    def run(self, manager: SingleSourceManager):
        self._execute(
            f"{self.EXECUTOR} {manager.source_file_name}",
            manager,
            c_type=ExecuteTypes.RUN,
        )


@LanguageHandlers.register(SupportedLanguages.JAVA)
class JavaHandler(AbstractHandler):
    """
    This is the handler that gets registered for the java
    language.
    """

    COMPILER = CompilerPaths.JAVA
    EXECUTOR = ExecutorPaths.JAVA

    def compile(self, manager: SingleSourceManager):
        self._execute(f"{self.COMPILER} {manager.source_file_name}", manager)

    def run(self, manager: SingleSourceManager):
        # strip the file extension from the source file
        java_file_extension = LANGUAGE_FILE_EXTENSIONS.get(SupportedLanguages.JAVA)
        source_file_name = manager.source_file_name.replace(
            f".{java_file_extension}", ""
        )

        self._execute(
            f"{self.EXECUTOR} {source_file_name}",
            manager,
            c_type=ExecuteTypes.RUN,
        )
