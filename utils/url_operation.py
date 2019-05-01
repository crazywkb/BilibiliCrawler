from urllib.parse import parse_qs, urlparse


def get_param_value(url, params_keys):
    parse_result = urlparse(url)
    params = {key: value for key, value in parse_qs(parse_result.query).items()}
    result = params.get(params_keys, None)
    if result and len(result) == 1:
        result = result[0]

    return result

