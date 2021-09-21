from abc import ABC, abstractclassmethod
from typing import List

from uri import URI

from miqa.learning.nn_classifier import get_model


class EvaluationModel(ABC):
    def __init__(self, uri: URI, expected_outputs: List[str]):
        self.uri = URI(uri)
        self.expected_outputs = expected_outputs
        super().__init__()

    @abstractclassmethod
    def load(self):
        pass


class NNModel(EvaluationModel):
    def load(self):
        return get_model('miqa/learning/models/' + str(self.uri))


available_evaluation_models = {
    'MIQAT1-0': NNModel(
        'miqaT1-val0.pth',
        [
            'overall_quality',
            'signal_noise_ratio',
            'contrast_noise_ratio',
            'normal_variants',
            'lesions',
            'full_brain_coverage',
            'misalignment',
            'swap_wraparound',
            'ghosting_motion',
            'inhomogeneity',
            'susceptibility_metal',
            'flow_artifact',
            'truncation_artifact',
        ],
    ),
    'MIQAT2-0': NNModel('fake_uri', []),
}