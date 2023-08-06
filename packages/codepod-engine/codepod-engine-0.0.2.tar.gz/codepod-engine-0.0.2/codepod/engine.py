"""
This file has the main engine that is the heart of this
project.
"""

import os
import shutil
import subprocess
import uuid

from codepod.constants import (
    CodePodEngineStatus,
    SupportedLanguages,
    LANGUAGE_FILE_EXTENSIONS,
)
from codepod.exceptions import CompilationException, RunException, ValidationException
from codepod.handlers import get_handler_instance
from codepod.managers import SingleSourceManager


class CodePodEngine:
    """
    CodePodEngine is used to compile and execute the source program that is
    given to it with the help of specific manager and handler classes.
    """

    def __init__(self, data: dict, single_source=True):
        self.code_pod_engine_path = os.path.join(".codepod", uuid.uuid4().hex)
        self.data = data
        self.data["status"] = CodePodEngineStatus.NOT_PROCESSED
        self.single_source = single_source

        self.__create_code_pod_engine_path()

    def __create_code_pod_engine_path(self):
        """
        Confirms if the directory to create the source and input files
        doesn't exists and creates a new one.
        """
        if os.path.exists(self.code_pod_engine_path):
            self.__clean_code_pod_engine_path()

        os.makedirs(self.code_pod_engine_path)

    def __clean_code_pod_engine_path(self):
        """
        Checks and removes the code pod engine directory if it
        exists.
        """
        if not os.path.exists(self.code_pod_engine_path):
            shutil.rmtree(self.code_pod_engine_path)

    def __validate_single_source_data(self):
        fields_required = ["input", "source", "language"]

        # check if all the required fields are present in the data payload.
        for field in fields_required:
            if self.data.get(field) is None:
                raise ValidationException(
                    f"argument ({field}) is missing in the payload"
                )

        # if the engine is running in a specific language, then only that language
        # should be passed in the payload.
        engine_language = os.getenv("LANGUAGE")
        if engine_language and engine_language != self.data.get("language"):
            raise Exception(
                f"only ({engine_language}) language is supported in this codepod engine"
            )

        # check if the language is supported in the code engine.
        if self.data.get("language") not in SupportedLanguages.as_list():
            raise Exception(f"language ({engine_language}) is currently not supported")

    def __run_with_single_source_manager(self):
        # validate the data given to the engine, proceed only if its valid
        try:
            self.__validate_single_source_data()
        except ValidationException as vex:
            self.data["status"] = CodePodEngineStatus.VALIDATION_FAILED
            self.data["error_message"] = vex.error_message
            return

        manager = SingleSourceManager(self.code_pod_engine_path)

        # create the input file
        manager.create_input_file(self.data.get("input"))

        # get the source file extension for the given language
        source_file_extension = LANGUAGE_FILE_EXTENSIONS.get(
            self.data.get("language"), "txt"
        )

        # create the source file
        manager.create_source_file(self.data.get("source"), source_file_extension)

        # get the handler instance for the language
        handler = get_handler_instance(self.data.get("language"))

        # set the time limit if present in the data
        time_limit = self.data.get("time_limit")
        if time_limit:
            handler.set_time_limit(self.data.get("time_limit"))

        # compile the source file
        try:
            handler.compile(manager)

            # run the executable after compilation
            handler.run(manager)
            self.data["status"] = CodePodEngineStatus.SUCCESS
        except CompilationException:
            self.data["status"] = CodePodEngineStatus.COMPILATION_FAIED
        except RunException:
            self.data["status"] = CodePodEngineStatus.RUN_FAILED
        except subprocess.TimeoutExpired:
            self.data["status"] = CodePodEngineStatus.TIMEOUT

        # read the error log and store it in the logs if the status is not success
        if self.data.get("status") != CodePodEngineStatus.SUCCESS:
            with open(manager.error_file, "r") as efp:
                self.data["error_log"] = efp.read()
        else:
            with open(manager.output_file, "r") as efp:
                self.data["output"] = efp.read()

    def run(self) -> dict:
        """
        Invokes the respective source manager based on the single_source
        args that is passed on object creation.
        """
        if self.single_source:
            self.__run_with_single_source_manager()

        # clean the code pod engine path the instance
        self.__clean_code_pod_engine_path()

        return self.data
