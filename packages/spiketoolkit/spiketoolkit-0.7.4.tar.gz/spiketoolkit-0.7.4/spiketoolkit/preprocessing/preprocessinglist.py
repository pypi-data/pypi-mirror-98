from .highpass_filter import highpass_filter, HighpassFilterRecording
from .bandpass_filter import bandpass_filter, BandpassFilterRecording
from .notch_filter import notch_filter, NotchFilterRecording
from .whiten import whiten, WhitenRecording
from .common_reference import common_reference, CommonReferenceRecording
from .resample import resample, ResampleRecording
from .rectify import rectify, RectifyRecording
from .remove_artifacts import remove_artifacts, RemoveArtifactsRecording
from .transform import transform, TransformRecording
from .remove_bad_channels import remove_bad_channels, RemoveBadChannelsRecording
from .normalize_by_quantile import normalize_by_quantile, NormalizeByQuantileRecording
from .clip import clip, ClipRecording
from .blank_saturation import blank_saturation, BlankSaturationRecording
from .center import center, CenterRecording
from .mask import mask, MaskRecording

preprocessers_full_list = [
    HighpassFilterRecording,
    BandpassFilterRecording,
    NotchFilterRecording,
    WhitenRecording,
    CommonReferenceRecording,
    ResampleRecording,
    RectifyRecording,
    RemoveArtifactsRecording,
    RemoveBadChannelsRecording,
    TransformRecording,
    NormalizeByQuantileRecording,
    ClipRecording,
    BlankSaturationRecording,
    CenterRecording,
    MaskRecording
]

installed_preprocessers_list = [pp for pp in preprocessers_full_list if pp.installed]
preprocesser_dict = {pp_class.preprocessor_name: pp_class for pp_class in preprocessers_full_list}
