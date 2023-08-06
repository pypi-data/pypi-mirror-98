import os


class SingleSourceManager:
    """
    This class is responsible from holding all the details that are needed to
    compile, run and get the output of a single source file program.
    """

    def __init__(self, source_path):
        self.source_path = source_path
        self.error_file = os.path.join(self.source_path, "error.log")
        self.output_file = os.path.join(self.source_path, "output.txt")

    def create_input_file(self, content: str):
        """
        Creates the input file with the given content.
        """
        self.input_file = os.path.join(self.source_path, "input.txt")

        with open(self.input_file, "w") as fp:
            fp.write(content)

    def create_source_file(self, content: str, extension: str):
        """
        Creates the source file with the given content.
        """
        self.source_file_name = f"Solution.{extension}"
        self.source_file = os.path.join(self.source_path, self.source_file_name)

        with open(self.source_file, "w") as fp:
            fp.write(content)
