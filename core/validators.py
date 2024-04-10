import re
from typing import Union, List

import pandas as pd


def validate_url(urls: Union[pd.Series, str], include_protocol: bool = False) -> Union[pd.Series, bool]:
    """  """
    regex_no_http = r"^(ftp|http(s)?)://?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(\/\S*)?$|^([a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$)"
    regex_with_http = r'^(ftp|http|https)://?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(\/\S*)?$'
    regex = regex_with_http if include_protocol else regex_no_http
    if isinstance(urls, (pd.Series, pd.Index)):
        is_url = urls.str.contains(regex, regex=True, case=False)
        if (~is_url).sum() > 0:
            return False
        else:
            return True
    elif isinstance(urls, str):
        return bool(re.compile(regex).match(urls))
    
    else:
        raise ValueError("urls must be type of: pd.Series, pd.Index, str")
    
