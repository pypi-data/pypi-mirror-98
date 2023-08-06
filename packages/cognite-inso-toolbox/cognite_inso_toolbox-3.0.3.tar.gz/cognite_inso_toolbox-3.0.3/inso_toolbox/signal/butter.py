import warnings
from typing import Dict, Optional, Union

import pandas as pd
import scipy.signal as signal


def butterworth(
    data: Union[pd.DataFrame, pd.Series], butter_kwargs: Optional[Dict] = None
) -> Union[pd.DataFrame, pd.Series]:
    """ Butterworth filter.
    Uses second-order section (sos) representation, polynomial (ba) representation,
    or zeros, poles, and system gain (zpk) representation.

    Args:
        data (pd.DataFrame or pd.Series): Time series to filter.
        butter_kwargs (Dict): Keyword arguments for scipy.signal.butter filter. Requires N (order of the filter), Wn (critical frequency) and output (filtering type) to be specified. Please read scipy.signal.butter for more details.

    Returns:
        pd.DataFrame or pd.Series: Filtered signal.
    """  # noqa

    if butter_kwargs is None:
        butter_kwargs = {"N": 1, "Wn": 0.1, "output": "sos"}
        warnings.warn(f"Using default arguments for 'N', 'Wn' and 'output': {butter_kwargs}", RuntimeWarning)

    # Only pd.Series and pd.DataFrame inputs are supported
    if not isinstance(data, pd.Series) and not isinstance(data, pd.DataFrame):
        raise ValueError("Only pd.Series and pd.DataFrame inputs are supported.")

    # Check all arguments are specified
    if set(["N", "Wn", "output"]).difference(butter_kwargs):
        raise RuntimeError("N, Wn and output need to be specified")

    # Warn user if there are any missing values
    if data.isna().any(axis=None):
        warnings.warn("There are missing values present in the time series.", RuntimeWarning)

    output_arg = butter_kwargs["output"]
    if output_arg == "sos":

        # Create butter filter
        filter_output = signal.butter(**butter_kwargs)

        # Apply second order sections filter
        filtered = signal.sosfilt(filter_output, data, axis=0)

    elif output_arg == "ba":

        # Create butter filter
        b, a = signal.butter(**butter_kwargs)

        # Apply direct form II transposed implementation of the standard difference equation filter
        filtered = signal.lfilter(b, a, data, axis=0)

    elif output_arg == "zpk":

        # Create butter filter
        z, p, k = signal.butter(**butter_kwargs)

        # Return polynomial transfer function representation from zeros and poles
        b, a = signal.zpk2tf(z, p, k)

        # Apply direct form II transposed implementation of the standard difference equation filter
        filtered = signal.lfilter(b, a, data, axis=0)
    else:
        raise RuntimeError(f"Expected output argument to be either 'sos', 'ba' or 'zpk', not {output_arg}")

    # Return series if that was the input type
    if isinstance(data, pd.Series):
        return pd.Series(filtered, index=data.index)

    # Return dataframe with same timestamps
    return pd.DataFrame(data=filtered, index=data.index, columns=data.columns)
