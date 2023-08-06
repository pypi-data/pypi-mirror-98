from spikeextractors import RecordingExtractor
from spikeextractors.extraction_tools import check_get_traces_args
from .basepreprocessorrecording import BasePreprocessorRecordingExtractor


class ClipRecording(BasePreprocessorRecordingExtractor):
    preprocessor_name = 'Clip'
    installed = True  # check at class level if installed or not
    installation_mesg = ""  # err

    def __init__(self, recording, a_min=None, a_max=None):
        if not isinstance(recording, RecordingExtractor):
            raise ValueError("'recording' must be a RecordingExtractor")
        self._a_min = a_min
        self._a_max = a_max
        BasePreprocessorRecordingExtractor.__init__(self, recording)
        self.has_unscaled = False
        self._kwargs = {'recording': recording.make_serialized_dict(), 'a_min': a_min, 'a_max': a_max}

    @check_get_traces_args
    def get_traces(self, channel_ids=None, start_frame=None, end_frame=None, return_scaled=True):
        assert return_scaled, "'clip' only supports return_scaled=True"

        traces = self._recording.get_traces(channel_ids=channel_ids,
                                            start_frame=start_frame,
                                            end_frame=end_frame,
                                            return_scaled=return_scaled)
        if self._a_min is not None:
            traces[traces < self._a_min] = self._a_min
        if self._a_max is not None:
            traces[traces > self._a_max] = self._a_max
        return traces


def clip(recording, a_min=None, a_max=None):
    '''
    Limit the values of the data between a_min and a_max. Values exceeding the
    range will be set to the minimum or maximum, respectively.
    
    Parameters
    ----------
    recording: RecordingExtractor
        The recording extractor to be transformed
    a_min: float or `None` (default `None`)
        Minimum value. If `None`, clipping is not performed on lower
        interval edge.
    a_max: float or `None` (default `None`)
        Maximum value. If `None`, clipping is not performed on upper
        interval edge.

    Returns
    -------
    rescaled_traces: ClipTracesRecording
        The clipped traces recording extractor object
    '''
    return ClipRecording(
        recording=recording, a_min=a_min, a_max=a_max
    )
