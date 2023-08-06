"""Abstract the structure of the model information in our TOML files."""
from dataclasses import dataclass
from typing import List, Union, Mapping


@dataclass
class InputFeatures:
    type: str
    processing: str
    max_input: float
    min_input: float
    step_length_min: int
    step_length_max: int
    sigma: float


@dataclass
class StoredModel:
    checkpoints: List[str]
    type: List[str]
    task: List[str]
    framework: List[str]
    error_length: int
    number_of_features: int
    number_of_outputs: int
    output_columns: List[str]
    output_type: str
    sequence_length: int
    columns: Mapping[str, InputFeatures]
    output_processing: str = None
    max_output: float = None
    min_output: float = None
    output_categories: List[Union[str, float]] = None
