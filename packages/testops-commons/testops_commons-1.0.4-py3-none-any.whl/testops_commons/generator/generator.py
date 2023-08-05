from os import path
from pathlib import Path

from testops_commons.configuration.configuration import Configuration
from testops_commons.core import constants
from testops_commons.helper import file_helper, helper
from testops_commons.model.models import (Execution, Metadata, TestResults,
                                          TestSuites)


class ReportGenerator:
    def write_execution(self, execution: Execution):
        pass

    def write_test_suites(self, suites: TestSuites):
        pass

    def write_test_results(self, results: TestResults):
        pass

    def write_metadata(self, metadata: Metadata):
        pass

    def write_global_execution_uuid(self, uuid):
        pass

    def clean_report_dir(self):
        pass


class TestOpsReportGenerator(ReportGenerator):

    configuration: Configuration
    output_directory: Path

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.is_parallel = configuration.is_parallel
        report_path = configuration.report_folder
        if self.is_parallel:
            report_path = path.join(configuration.report_folder, helper.current_thread_name())
        self.output_directory = report_path

    def clean_report_dir(self):
        file_helper.clean_dir(self.configuration.report_folder)

    def set_parallel(self, enabled):
        if enabled == self.is_parallel:
            return
        self.is_parallel = enabled
        if enabled:
            self.output_directory = path.join(self.configuration.report_folder, helper.current_thread_name())
        else:
            self.output_directory = self.configuration.report_folder
        file_helper.ensure_directory(self.output_directory)

    def write_execution(self, execution: Execution):
        self.write_to_file(execution, 'execution' + constants.REPORT_FILE_EXTENSION)

    def write_test_suites(self, suites: TestSuites):
        self.write_to_file(suites, 'suites' + constants.REPORT_FILE_EXTENSION)
        pass

    def write_test_results(self, results: TestResults):
        self.write_to_file(results, 'results' + constants.REPORT_FILE_EXTENSION)
        pass

    def write_metadata(self, metadata: Metadata):
        build_label: str = self.configuration.build_label
        build_url: str = self.configuration.build_url
        metadata.buildUrl = build_url
        metadata.buildLabel = build_label
        execution_uuid = self.get_master_execution_uuid()
        if execution_uuid:
            metadata.executionUuid = execution_uuid
        self.write_to_file(metadata, 'metadata' + constants.REPORT_FILE_EXTENSION)

    def write_global_execution_uuid(self, uuid):
        if not Path(self.configuration.report_folder).exists():
            file_helper.ensure_directory(self.configuration.report_folder)
        with open(path.join(self.configuration.report_folder, "execution.uuid"), "w") as f:
            f.write(uuid)

    def write_to_file(self, data, file_name: str):
        if not Path(self.output_directory).exists():
            file_helper.ensure_directory(self.output_directory)
        helper.write_json(data, path.join(self.output_directory, file_name))

    def get_master_execution_uuid(self) -> str:
        try:
            with open(path.join(self.configuration.report_folder, "execution.uuid")) as f:
                return f.read()
        except Exception:
            return None
