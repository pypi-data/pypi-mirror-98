from typing import Dict

from narupa.trajectory import FrameData

from narupatools.state.typing import Serializable


def frame_data_to_dictionary(frame_data: FrameData) -> Dict[str, Serializable]:
    frame_dict = {}
    for key in frame_data.values.keys():
        frame_dict[key] = frame_data.values[key]
    for key in frame_data.arrays.keys():
        frame_dict[key] = list(frame_data.arrays[key])
    return frame_dict
