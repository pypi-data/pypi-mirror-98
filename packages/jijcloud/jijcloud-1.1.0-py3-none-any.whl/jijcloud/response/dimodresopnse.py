from .base import BaseResponse
import dimod

class DimodResponse(BaseResponse, dimod.SampleSet):
    @classmethod
    def from_json_obj(cls, json_obj):
        return cls.from_serializable(json_obj)

    @classmethod
    def empty_data(cls):
        return cls.from_samples([], 'BINARY', 0)
