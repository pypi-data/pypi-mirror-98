"""Create, save and load a stored model."""
import toml
from dataclasses import asdict
from typing import List, Union, Mapping

from aidkit.core.stored_model import StoredModel, InputFeatures


def load_stored_model(path: str) -> StoredModel:
    """
    Load a stored model.

    :param path: path to the TOML file that contains the model information
    """
    stored_model_dict = toml.load(path)
    stored_model = StoredModel(**stored_model_dict)
    return stored_model


def save_stored_model(stored_model: StoredModel, path: str):
    """
    Save the information about a model in a TOML file.

    :param stored_model: StoredModel dataclass with the model information
    :param path: path where the TOML file is saved
    """
    stored_model_dict = asdict(stored_model)
    with open(path, 'w') as f:
        toml.dump(stored_model_dict, f)


def create_stored_model(checkpoints: List[str],
                        type: List[str],
                        task: List[str],
                        framework: List[str],
                        error_length: int,
                        number_of_features: int,
                        number_of_outputs: int,
                        output_columns: List[str],
                        output_type: str,
                        output_processing: str,
                        max_output: float,
                        min_output: float,
                        output_categories: List[Union[str, float]],
                        sequence_length: int,
                        columns: Mapping[str, InputFeatures]) -> StoredModel:
    """
    Create a StoredModel instance with all the information needed to perform
    an analysis.

    :param checkpoints: list of checkpoints
    :param type: feedforward or recurrent
    :param task: classification or regression
    :param framework: keras or scikit
    :param error_length: length of the error
    :param number_of_features: number of features of the model
    :param number_of_outputs: number of outputs of the model
    :param output_columns: name of the output columns containing the
        label information (e.g: MAX, LABEL)
    :param output_type: quantitative or categorical
    :param output_processing: name of the function to be used for
        output processing (e.g: min_max)
    :param max_output: maximum value of the output
    :param min_output: minimum value of the output
    :param output_categories: list of output categories
    :param sequence_length: length of the sequence
    :param columns: dictionary where each key is the name of a column and
        each value is an InputFeatures dataclass:
        max_input: maximum input value of the column
        min_input: minimum input value of the column
        step_length_min: minimum step length of the column
        step_length_max: maximum step length of the column
        sigma: variance of the values of the column
    """
    stored_model = StoredModel(checkpoints=checkpoints,
                               type=type,
                               task=task,
                               framework=framework,
                               error_length=error_length,
                               number_of_features=number_of_features,
                               number_of_outputs=number_of_outputs,
                               output_columns=output_columns,
                               output_type=output_type,
                               output_processing=output_processing,
                               max_output=max_output,
                               min_output=min_output,
                               output_categories=output_categories,
                               sequence_length=sequence_length,
                               columns=columns)
    return stored_model
