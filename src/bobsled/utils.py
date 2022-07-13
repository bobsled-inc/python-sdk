
def flatten(contents, prefix="s3://rhizo-your-bucket-name"):
  
  result = []

  for obj in contents:
      if obj["content"] is None:
        result.append(prefix + obj["id"])
      else:
          result.extend(flatten(obj["content"]))

  return result
  