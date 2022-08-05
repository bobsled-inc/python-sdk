from . import BobsledException

def handle_errors(response):
    status = response.status_code
    data = response.text
    # figure out right way to extract error message for every error
    print(status, data)
    
    if response.status_code == 401 or response.status_code == 403:
        raise BobsledException.BadCredentialsError(status = response.status_code, data = data) # errorType might change?
    elif response.status_code == 404:
        raise BobsledException.UnknownObjectError(status = response.status_code, data = data)
    elif response.status_code == 500:
        raise BobsledException.InternalServerError(status = response.status_code, data = data)
    else:
        raise BobsledException(status = response.status_code, data = data)

def flatten(contents, prefix, time=0):
    """Helper function to flatten contents of source bucket

    :param contents: dictionary representing source bucket
    :param prefix: root path of the bucket
    :return: list of complete file paths for all files in source bucket
    """  
    result = []
    total_size = 0
    for obj in contents:
        if obj["content"] is None:
            timestamp = obj["lastModified"] // 1000
            if timestamp >= time:
                total_size += obj["size"]
                result.append(prefix + obj["id"])
        else:
            result.extend(flatten(obj["content"], prefix))

    return result, total_size
  