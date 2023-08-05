"""Abstract our toml and structure its components."""
from typing import List

from backend.data_access.data_access_interface.data import DataInterface


class RequestModel:
    """Toml abstraction."""

    def __init__(self, config: dict):
        """
        :param config: came of the config in the config folder.
        """
        self._config = config
        self._verify_model()
        self._verify_data()
        self._verify_analyses()

    @property
    def dict(self) -> dict:
        """Get configuration dict."""
        return self._config

    @property
    def model(self) -> dict:
        """Obtain the model dict."""
        return self.dict.get('model')

    @property
    def data(self) -> str:
        """Obtain list of data strings"""
        return self.dict.get('data')

    @property
    def analyses(self) -> dict:
        """Obtain dict of analyses"""
        return self.dict.get('analyses')

    def _verify_model(self):
        """Check if model is correctly implemented."""
        assert 'model' in self.dict, "Config needs model attribute."

        parameters = {
            "checkpoints", "task", "type", "error_length", "number_of_features", "number_of_outputs",
            "output_type", "output_columns", "sequence_length", "columns"
        }
        model_parameters = set(self.model.keys())
        assert parameters <= model_parameters, \
            f"Model is missing the {parameters - model_parameters} keys."

        if isinstance(self.model["checkpoints"], str):
            self.model["checkpoints"] = [self.model["checkpoints"]]

        assert len(self.model["checkpoints"]) == 1, "Only support one checkpoint."
        self.model["checkpoints"] = self.model["checkpoints"][0]

        columns = self.model['columns']

        if self.model['task'] == 'regression':
            assert len(self.model['output_columns']) == self.model['number_of_outputs'], \
                "The length of output columns and the number of outputs must match."

        self._verify_columns(columns)

        for column in columns:
            column_dict = columns[column]
            drop_col = column_dict.get('drop', False)
            continuous_col = 'max_input' in column_dict and 'min_input' in column_dict
            categorical_col = 'categories' in column_dict
            assert drop_col or continuous_col or categorical_col, \
                "You must specify the range of a column or provide categories for the data or " \
                "drop the column."

    def _verify_columns(self, columns):
        column_counter = 0
        for k, v in columns.items():
            drop = v.get('drop', False)
            categories = v.get('categories', ['no categories'])
            if drop:
                continue
            if categories:
                column_counter += len(categories)

        assert column_counter == self.model['number_of_features'], \
            f"The length of columns and the number of features must " \
            f"match. {column_counter} != {self.model['number_of_features']}"

    def _verify_data(self):
        """Check if data is correctly specified."""
        assert 'data' in self.dict, "Config needs data attribute."
        assert self.data, "Please specify a dataset."

        if isinstance(self.data, str):
            self._config["data"] = [self._config["data"]]
        assert len(self.data) == 1, "We only support one dataset right now"
        self._config["data"] = self.data[0]

        known_data = DataInterface.read_all()
        assert self.data in known_data, \
            f"Unknown dataset {self.data}, only know {known_data}."

    def _verify_analyses(self):
        """Check if analyses are specified correctely."""
        assert "analyses" in self.dict, "Config needs analyses attribute."

        formatted_analyses = dict()
        for analysis in self.analyses:
            formatted_analyses[name2key(analysis)] = self.analyses[analysis]

        self._config["analyses"] = formatted_analyses


def split_multi_parameters(request: RequestModel, analysis_name: str) -> List[RequestModel]:
    """
    In toml files it is possible to specify a list of dicts. This is
    practical when thinking about wanting to execute one analysis for
    multiple parameter settings. This function takes a request model and
    an analysis name.
    Depending on how much parameters settings are specified for this
    analysis, this function returns a list of single parameter settings,
    for only this analysis, all other analyses are ignored.
    """
    assert analysis_name in request.analyses, \
        f"Unknown analysis {analysis_name} in {request.analyses}."

    requests = list()

    parameters = request.analyses[analysis_name] or {}
    if isinstance(parameters, dict):
        parameters = [parameters]

    for parameter in parameters:
        new_config = request.dict.copy()
        new_config["analyses"] = {analysis_name: parameter}
        sub_request = RequestModel(config=new_config)
        requests.append(sub_request)

    return requests


def name2key(name: str):
    """Converts a analysis name to according toml keys."""
    return name.lower().replace(" ", "_").replace("_/", "")
