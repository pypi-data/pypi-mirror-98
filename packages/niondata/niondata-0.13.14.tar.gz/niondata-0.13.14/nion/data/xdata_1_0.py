"""
Includes functions necessary for processing operations, functions making it easier to
handle various data types such as RGB, functions for creating custom classes used as
arguments, functions that represent pixel by pixel operations where calibration should
be maintained, and other utility functions.

It does not include functions which can be readily implemented via numpy.
"""


# standard libraries
import datetime
import functools
import numpy
import scipy.stats
import typing

from nion.data import Core
from nion.data import Calibration
from nion.data import DataAndMetadata
from nion.data import RGB
from nion.utils import Geometry


# functions changing size or type of array

def astype(data_and_metadata: DataAndMetadata.DataAndMetadata, type: numpy.dtype) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_array(Core.astype, data_and_metadata, type)

def concatenate(data_and_metadata_list: typing.Sequence[DataAndMetadata.DataAndMetadata], axis: int=0) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_concatenate(data_and_metadata_list, axis)

def hstack(data_and_metadata_list: typing.Sequence[DataAndMetadata.DataAndMetadata]) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_hstack(data_and_metadata_list)

def vstack(data_and_metadata_list: typing.Sequence[DataAndMetadata.DataAndMetadata]) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_vstack(data_and_metadata_list)

def moveaxis(data_and_metadata: DataAndMetadata.DataAndMetadata, src_axis: int, dst_axis: int) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_moveaxis(data_and_metadata, src_axis, dst_axis)

def reshape(data_and_metadata: DataAndMetadata.DataAndMetadata, shape: DataAndMetadata.ShapeType) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_reshape(data_and_metadata, shape)

def squeeze(data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_squeeze(data_and_metadata)

def redimension(data_and_metadata: DataAndMetadata.DataAndMetadata, data_descriptor: DataAndMetadata.DataDescriptor) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_redimension(data_and_metadata, data_descriptor)

def rescale(data_and_metadata: DataAndMetadata.DataAndMetadata, data_range: Core.DataRangeType=None) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_rescale(data_and_metadata, data_range)

def resize(data_and_metadata: DataAndMetadata.DataAndMetadata, shape: DataAndMetadata.ShapeType, mode=None) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_resize(data_and_metadata, shape, mode)

def data_slice(data_and_metadata: DataAndMetadata.DataAndMetadata, key) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return DataAndMetadata.function_data_slice(data_and_metadata, key)

def crop(data_and_metadata: DataAndMetadata.DataAndMetadata, bounds: Core.NormRectangleType) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_crop(data_and_metadata, bounds)

def crop_rotated(data_and_metadata: DataAndMetadata.DataAndMetadata, bounds: Core.NormRectangleType, angle: float) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_crop_rotated(data_and_metadata, bounds, angle)

def crop_interval(data_and_metadata: DataAndMetadata.DataAndMetadata, interval: Core.NormIntervalType) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_crop_interval(data_and_metadata, interval)

def slice_sum(data_and_metadata: DataAndMetadata.DataAndMetadata, slice_center: int, slice_width: int) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_slice_sum(data_and_metadata, slice_center, slice_width)

def pick(data_and_metadata: DataAndMetadata.DataAndMetadata, position: DataAndMetadata.PositionType) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_pick(data_and_metadata, position)

def sum(data_and_metadata: DataAndMetadata.DataAndMetadata, axis: typing.Union[int, typing.Sequence[int]]=None, keepdims: bool=False) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_sum(data_and_metadata, axis, keepdims=keepdims)

def mean(data_and_metadata: DataAndMetadata.DataAndMetadata, axis: typing.Union[int, typing.Sequence[int]]=None, keepdims: bool=False) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_mean(data_and_metadata, axis, keepdims=keepdims)

def sum_region(data_and_metadata: DataAndMetadata.DataAndMetadata, mask_data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_sum_region(data_and_metadata, mask_data_and_metadata)

def average_region(data_and_metadata: DataAndMetadata.DataAndMetadata, mask_data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_average_region(data_and_metadata, mask_data_and_metadata)

def rebin_image(data_and_metadata: DataAndMetadata.DataAndMetadata, shape: DataAndMetadata.ShapeType) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_rebin_2d(data_and_metadata, shape)

def resample_image(data_and_metadata: DataAndMetadata.DataAndMetadata, shape: DataAndMetadata.ShapeType) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_resample_2d(data_and_metadata, shape)

def warp(data_and_metadata: DataAndMetadata.DataAndMetadata, coordinates: typing.Sequence[DataAndMetadata.DataAndMetadata], order: int=1) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_warp(data_and_metadata, coordinates)

def affine_transform(data_and_metadata: DataAndMetadata.DataAndMetadata, transformation_matrix: numpy.ndarray, order: int=1) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_affine_transform(data_and_metadata, transformation_matrix, order=order)

# functions generating ndarrays
# TODO: move these bodies to Core once Core usage has been migrated

def column(shape: DataAndMetadata.Shape2dType, start: int=None, stop: int=None) -> DataAndMetadata.DataAndMetadata:
    start_0 = start if start is not None else 0
    stop_0 = stop if stop is not None else shape[0]
    start_1 = start if start is not None else 0
    stop_1 = stop if stop is not None else shape[1]
    data = numpy.meshgrid(numpy.linspace(start_1, stop_1, shape[1]), numpy.linspace(start_0, stop_0, shape[0]))[0]
    return DataAndMetadata.new_data_and_metadata(data)

def row(shape: DataAndMetadata.Shape2dType, start: int=None, stop: int=None) -> DataAndMetadata.DataAndMetadata:
    start_0 = start if start is not None else 0
    stop_0 = stop if stop is not None else shape[0]
    start_1 = start if start is not None else 0
    stop_1 = stop if stop is not None else shape[1]
    data = numpy.meshgrid(numpy.linspace(start_1, stop_1, shape[1]), numpy.linspace(start_0, stop_0, shape[0]))[1]
    return DataAndMetadata.new_data_and_metadata(data)

def radius(shape: DataAndMetadata.Shape2dType, normalize: bool=True) -> DataAndMetadata.DataAndMetadata:
    start_0 = -1 if normalize else -shape[0] * 0.5
    stop_0 = -start_0
    start_1 = -1 if normalize else -shape[1] * 0.5
    stop_1 = -start_1
    icol, irow = numpy.meshgrid(numpy.linspace(start_1, stop_1, shape[1]), numpy.linspace(start_0, stop_0, shape[0]), sparse=True)
    data = numpy.sqrt(icol * icol + irow * irow)
    return DataAndMetadata.new_data_and_metadata(data)

def gammapdf(data_and_metadata: DataAndMetadata.DataAndMetadata, a: float, mean: float, stddev: float) -> DataAndMetadata.DataAndMetadata:
    # pdf: probability density function
    return Core.apply_dist(data_and_metadata, mean, stddev, functools.partial(scipy.stats.gamma, a), 'pdf')

def gammalogpdf(data_and_metadata: DataAndMetadata.DataAndMetadata, a: float, mean: float, stddev: float) -> DataAndMetadata.DataAndMetadata:
    # pdf: probability density function
    return Core.apply_dist(data_and_metadata, mean, stddev, functools.partial(scipy.stats.gamma, a), 'logpdf')

def gammacdf(data_and_metadata: DataAndMetadata.DataAndMetadata, a: float, mean: float, stddev: float) -> DataAndMetadata.DataAndMetadata:
    # cdf: cumulative density function
    return Core.apply_dist(data_and_metadata, mean, stddev, functools.partial(scipy.stats.gamma, a), 'cdf')

def gammalogcdf(data_and_metadata: DataAndMetadata.DataAndMetadata, a: float, mean: float, stddev: float) -> DataAndMetadata.DataAndMetadata:
    # cdf: cumulative density function
    return Core.apply_dist(data_and_metadata, mean, stddev, functools.partial(scipy.stats.gamma, a), 'logcdf')

def normpdf(data_and_metadata: DataAndMetadata.DataAndMetadata, a: float, mean: float, stddev: float) -> DataAndMetadata.DataAndMetadata:
    # pdf: probability density function
    return Core.apply_dist(data_and_metadata, mean, stddev, scipy.stats.norm, 'pdf')

def normlogpdf(data_and_metadata: DataAndMetadata.DataAndMetadata, a: float, mean: float, stddev: float) -> DataAndMetadata.DataAndMetadata:
    # pdf: probability density function
    return Core.apply_dist(data_and_metadata, mean, stddev, scipy.stats.norm, 'logpdf')

def normcdf(data_and_metadata: DataAndMetadata.DataAndMetadata, a: float, mean: float, stddev: float) -> DataAndMetadata.DataAndMetadata:
    # cdf: cumulative density function
    return Core.apply_dist(data_and_metadata, mean, stddev, scipy.stats.norm, 'cdf')

def normlogcdf(data_and_metadata: DataAndMetadata.DataAndMetadata, a: float, mean: float, stddev: float) -> DataAndMetadata.DataAndMetadata:
    # cdf: cumulative density function
    return Core.apply_dist(data_and_metadata, mean, stddev, scipy.stats.norm, 'logcdf')

# complex

def absolute(data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_array(numpy.absolute, data_and_metadata)

def angle(data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_array(numpy.angle, data_and_metadata)

def real(data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_array(numpy.real, data_and_metadata)

def imag(data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_array(numpy.imag, data_and_metadata)

def conj(data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_array(numpy.conj, data_and_metadata)

def real_if_close(data_and_metadata: DataAndMetadata.DataAndMetadata, tol=100) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_array(numpy.real_if_close, data_and_metadata, tol)

# rgb

def red(data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return RGB.function_rgb_channel(data_and_metadata, 2)

def green(data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return RGB.function_rgb_channel(data_and_metadata, 1)

def blue(data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return RGB.function_rgb_channel(data_and_metadata, 0)

def alpha(data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return RGB.function_rgb_channel(data_and_metadata, 3)

def luminance(data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return RGB.function_rgb_linear_combine(data_and_metadata, 0.2126, 0.7152, 0.0722)

def rgb(red_data_and_metadata: DataAndMetadata.DataAndMetadata, green_data_and_metadata: DataAndMetadata.DataAndMetadata,
        blue_data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return RGB.function_rgb(red_data_and_metadata, green_data_and_metadata, blue_data_and_metadata)

def rgba(red_data_and_metadata: DataAndMetadata.DataAndMetadata, green_data_and_metadata: DataAndMetadata.DataAndMetadata,
         blue_data_and_metadata: DataAndMetadata.DataAndMetadata, alpha_data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return RGB.function_rgba(red_data_and_metadata, green_data_and_metadata, blue_data_and_metadata, alpha_data_and_metadata)

# ffts

def fft(data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_fft(data_and_metadata)

def ifft(data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_ifft(data_and_metadata)

def autocorrelate(data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_autocorrelate(data_and_metadata)

def crosscorrelate(data_and_metadata1: DataAndMetadata.DataAndMetadata, data_and_metadata2: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_crosscorrelate(data_and_metadata1, data_and_metadata2)

def fourier_mask(data_and_metadata: DataAndMetadata.DataAndMetadata, mask_data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_fourier_mask(data_and_metadata, mask_data_and_metadata)

# filters

def sobel(data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_sobel(data_and_metadata)

def laplace(data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_laplace(data_and_metadata)

def gaussian_blur(data_and_metadata: DataAndMetadata.DataAndMetadata, sigma: float) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_gaussian_blur(data_and_metadata, sigma)

def median_filter(data_and_metadata: DataAndMetadata.DataAndMetadata, size: int) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_median_filter(data_and_metadata, size)

def uniform_filter(data_and_metadata: DataAndMetadata.DataAndMetadata, size: int) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_uniform_filter(data_and_metadata, size)

def transpose_flip(data_and_metadata: DataAndMetadata.DataAndMetadata, transpose: bool=False, flip_v: bool=False, flip_h: bool=False) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_transpose_flip(data_and_metadata, transpose, flip_v, flip_h)

# miscellaneous

def histogram(data_and_metadata: DataAndMetadata.DataAndMetadata, bins: int) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_histogram(data_and_metadata, bins)

def line_profile(data_and_metadata: DataAndMetadata.DataAndMetadata, vector: Core.NormVectorType,
                 integration_width: float) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_line_profile(data_and_metadata, vector, integration_width)

def invert(data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_invert(data_and_metadata)

# sequences: registration, shifting, alignment, integrate, trim, insert, concat, extract

def register_translation(xdata1: DataAndMetadata.DataAndMetadata, xdata2: DataAndMetadata.DataAndMetadata, upsample_factor: int = 1, subtract_means: bool = True) -> typing.Tuple[float, ...]:
    return Core.function_register(xdata1, xdata2, upsample_factor, subtract_means)

def match_template(image_xdata: DataAndMetadata.DataAndMetadata, template_xdata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_match_template(image_xdata, template_xdata)

def register_template(image_xdata: DataAndMetadata.DataAndMetadata, template_xdata: DataAndMetadata.DataAndMetadata) -> typing.Tuple[float, typing.Tuple[float, ...]]:
    return Core.function_register_template(image_xdata, template_xdata)

def shift(src: DataAndMetadata.DataAndMetadata, shift: typing.Tuple[float, ...], *, order: int=1) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_shift(src, shift, order=order)

def fourier_shift(src: DataAndMetadata.DataAndMetadata, shift: typing.Tuple[float, ...]) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_fourier_shift(src, shift)

def align(src: DataAndMetadata.DataAndMetadata, target: DataAndMetadata.DataAndMetadata, upsample_factor: int = 1, bounds: typing.Union[Core.NormRectangleType, Core.NormIntervalType] = None) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_align(src, target, upsample_factor, bounds=bounds)

def fourier_align(src: DataAndMetadata.DataAndMetadata, target: DataAndMetadata.DataAndMetadata, upsample_factor: int = 1, bounds: typing.Union[Core.NormRectangleType, Core.NormIntervalType] = None) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_fourier_align(src, target, upsample_factor, bounds=bounds)

def sequence_register_translation(src: DataAndMetadata.DataAndMetadata, upsample_factor: int = 1, subtract_means: bool = True, bounds: typing.Union[Core.NormRectangleType, Core.NormIntervalType] = None) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_sequence_register_translation(src, upsample_factor, subtract_means)

def sequence_measure_relative_translation(src: DataAndMetadata.DataAndMetadata, ref: DataAndMetadata.DataAndMetadata, upsample_factor: int = 1, subtract_means: bool = True, bounds: typing.Union[Core.NormRectangleType, Core.NormIntervalType] = None) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_sequence_measure_relative_translation(src, ref, upsample_factor, subtract_means, bounds=bounds)

def sequence_squeeze_measurement(data_and_metadata: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_squeeze_measurement(data_and_metadata)

def sequence_align(src: DataAndMetadata.DataAndMetadata, upsample_factor: int = 1, bounds: typing.Union[Core.NormRectangleType, Core.NormIntervalType] = None) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_sequence_align(src, upsample_factor, bounds=bounds)

def sequence_fourier_align(src: DataAndMetadata.DataAndMetadata, upsample_factor: int = 1, bounds: typing.Union[Core.NormRectangleType, Core.NormIntervalType] = None) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_sequence_fourier_align(src, upsample_factor, bounds=bounds)

def sequence_integrate(src: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_sequence_integrate(src)

def sequence_trim(src: DataAndMetadata.DataAndMetadata, trim_start: int, trim_end: int) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_sequence_trim(src, trim_start, trim_end)

def sequence_insert(src1: DataAndMetadata.DataAndMetadata, src2: DataAndMetadata.DataAndMetadata, position: int) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_sequence_insert(src1, src2, position)

def sequence_concatenate(src1: DataAndMetadata.DataAndMetadata, src2: DataAndMetadata.DataAndMetadata) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_sequence_concatenate(src1, src2)

def sequence_join(data_and_metadata_list: typing.Sequence[DataAndMetadata.DataAndMetadata]) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_sequence_join(data_and_metadata_list)

def sequence_extract(src: DataAndMetadata.DataAndMetadata, position: int) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_sequence_extract(src, position)

def sequence_split(src: DataAndMetadata.DataAndMetadata) -> typing.Optional[typing.List[DataAndMetadata.DataAndMetadata]]:
    return Core.function_sequence_split(src)

# utility functions

def new_with_data(data: numpy.ndarray, *,
                  intensity_calibration: Calibration.Calibration = None,
                  dimensional_calibrations: DataAndMetadata.CalibrationListType = None,
                  metadata: dict = None,
                  timestamp: datetime.datetime = None,
                  data_descriptor: DataAndMetadata.DataDescriptor = None) -> DataAndMetadata.DataAndMetadata:
    return DataAndMetadata.new_data_and_metadata(data,
                                                 intensity_calibration=intensity_calibration,
                                                 dimensional_calibrations=dimensional_calibrations,
                                                 metadata=metadata,
                                                 timestamp=timestamp,
                                                 data_descriptor=data_descriptor)

def calibration(*, offset=0.0, scale=1.0, units=None):
    return Calibration.Calibration(offset, scale, units)

def data_descriptor(*, is_sequence=False, collection_dims=0, datum_dims=1) -> DataAndMetadata.DataDescriptor:
    return DataAndMetadata.DataDescriptor(is_sequence, collection_dims, datum_dims)

def map_function(fn, data_and_metadata: DataAndMetadata.DataAndMetadata, *args, **kwargs) -> typing.Optional[DataAndMetadata.DataAndMetadata]:
    return Core.function_array(fn, data_and_metadata, *args, **kwargs)

def norm_point(y: float, x: float) -> Core.NormPointType:
    return y, x

def norm_size(height, width) -> Core.NormSizeType:
    return height, width

def vector(start, end) -> Core.NormVectorType:
    return start, end

def rectangle_from_origin_size(origin: Core.NormPointType, size: Core.NormSizeType) -> Core.NormRectangleType:
    return typing.cast(Core.NormRectangleType, tuple(Geometry.FloatRect(origin, size)))

def rectangle_from_center_size(center: Core.NormPointType, size: Core.NormSizeType) -> Core.NormRectangleType:
    return typing.cast(Core.NormRectangleType, tuple(Geometry.FloatRect.from_center_and_size(center, size)))

def norm_interval(start, end) -> Core.NormIntervalType:
    return start, end

def norm_interval_to_px_interval(data_and_metadata: DataAndMetadata.DataAndMetadata, interval: Core.NormIntervalType) -> Core.NormIntervalType:
    data_shape = data_and_metadata.data_shape
    assert data_shape is not None
    return interval[0] * data_shape[0], interval[1] * data_shape[0]
