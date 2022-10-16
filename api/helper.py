import hashlib
def filter_dict_keys(dictionary, keys):
    result = {}
    for key in keys:
        if key in dictionary:
            result[key] = dictionary[key]

    return result

def get_model_fields(model: object):
    """
    :param model: Model Object
    :return: Model fields including child elements of referenced fields
    """
    meta_fields = model._meta.get_fields()
    output_fields = [f.name for f in meta_fields]

    return output_fields

def get_hash_key(key: str):
    """
    :param key: Value to be hashed
    :return hashed key
    """
    hashed_key = hashlib.sha1(key.encode('utf-8')).hexdigest()
    return hashed_key
from urllib import parse as url_parse
def replace_query_param(url, key, val):
    """
    Given a URL and a key/val pair, set or replace an item in the query
    parameters of the URL, and return the new URL.
    """
    result = url_parse.urlparse(url)
    query_dict = url_parse.parse_qs(result.query, keep_blank_values=True)
    query_dict[key] = [val]
    query = url_parse.urlencode(sorted(list(query_dict.items())), doseq=True)
    return url_parse.urlunsplit((result.scheme, result.netloc, result.path, query, result.fragment))

def get_next_prev_url(url, page_no, result_count, page_len):
    page_param = 'page_no'
    max_page_no = int(result_count / page_len) + int(result_count % page_len != 0)
    next_link = prev_link = None
    if max_page_no > page_no:
        next_link = replace_query_param(url, page_param, page_no + 1)
    if page_no > 1:
        prev_link = replace_query_param(url, page_param, page_no - 1)
    return next_link, prev_link