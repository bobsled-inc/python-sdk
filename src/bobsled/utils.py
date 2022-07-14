
def flatten(contents, prefix="s3://rhizo-your-bucket-name"):
  """Helper function to flatten contents of source bucket

  :param contents: dictionary representing source bucket
  :param prefix: root path of the bucket
  :return: list of complete file paths for all files in source bucket
  """  
  result = []

  for obj in contents:
      if obj["content"] is None:
        result.append(prefix + obj["id"])
      else:
          result.extend(flatten(obj["content"]))

  return result
  