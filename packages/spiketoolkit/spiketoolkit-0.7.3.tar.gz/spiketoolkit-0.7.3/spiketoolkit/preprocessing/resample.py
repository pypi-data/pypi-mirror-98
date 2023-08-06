from spikeextractors import RecordingExtractor
from spikeextractors.extraction_tools import check_get_traces_args
from .basepreprocessorrecording import BasePreprocessorRecordingExtractor
import numpy as np

try:
    from scipy import special, signal

    HAVE_RR = True
except ImportError:
    HAVE_RR = False


class ResampleRecording(BasePreprocessorRecordingExtractor):
    preprocessor_name = 'Resample'
    installed = HAVE_RR  # check at class level if installed or not
    installation_mesg = "To use the ResampleRecording, install scipy: \n\n pip install scipy\n\n"  # err

    def __init__(self, recording, resample_rate):
        assert HAVE_RR, "To use the ResampleRecording, install scipy: \n\n pip install scipy\n\n"
        self._resample_rate = resample_rate
        BasePreprocessorRecordingExtractor.__init__(self, recording)
        self._dtype = recording.get_dtype()
        self._kwargs = {'recording': recording.make_serialized_dict(), 'resample_rate': resample_rate}

    def get_sampling_frequency(self):
        return self._resample_rate

    def get_num_frames(self):
        return int(self._recording.get_num_frames() / self._recording.get_sampling_frequency() * self._resample_rate)

    # avoid filtering one sample
    def get_dtype(self, return_scaled=True):
        return self._dtype

    @check_get_traces_args
    def get_traces(self, channel_ids=None, start_frame=None, end_frame=None, return_scaled=True):
        start_frame_not_sampled = int(start_frame / self.get_sampling_frequency() *
                                      self._recording.get_sampling_frequency())
        start_frame_sampled = start_frame
        end_frame_not_sampled = int(end_frame / self.get_sampling_frequency() *
                                    self._recording.get_sampling_frequency())
        end_frame_sampled = end_frame
        traces = self._recording.get_traces(start_frame=start_frame_not_sampled,
                                            end_frame=end_frame_not_sampled,
                                            channel_ids=channel_ids,
                                            return_scaled=return_scaled)
        traces_resampled = signal.resample(traces, int(end_frame_sampled - start_frame_sampled), axis=1)

        return traces_resampled.astype(self._dtype)


def resample(recording, resample_rate):
    '''
    Resamples the recording extractor traces. If the resampling rate is multiple of the sampling rate, the faster
    scipy decimate function is used.

    Parameters
    ----------
    recording: RecordingExtractor
        The recording extractor to be resampled
    resample_rate: int or float
        The resampling frequency

    Returns
    -------
    resampled_recording: ResampleRecording
        The resample recording extractor

    '''
    return ResampleRecording(
        recording=recording,
        resample_rate=resample_rate
    )
