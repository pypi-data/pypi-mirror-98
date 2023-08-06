import os


CLOUD_STORAGE_PROTOCOL = "gs://"


def join(*paths):
    """An analogue to os.path.join for Google Cloud storage paths.

    :param iter paths:
    :return str:
    """
    if not paths:
        return ""

    path = os.path.normpath(os.path.join(*paths)).replace(os.sep, "/")

    if path.startswith("gs:/"):
        if not path.startswith(CLOUD_STORAGE_PROTOCOL):
            path = path.replace("gs:/", CLOUD_STORAGE_PROTOCOL)

    return path


def generate_gs_path(bucket_name, *paths):
    """Generate the Google Cloud storage path for a path in a bucket.

    :param str bucket_name:
    :param iter paths:
    :return str:
    """
    if not paths:
        return CLOUD_STORAGE_PROTOCOL + bucket_name
    return CLOUD_STORAGE_PROTOCOL + join(bucket_name, paths[0].lstrip("/"), *paths[1:])


def split_bucket_name_from_gs_path(gs_path):
    """Split the bucket name from the path.

    :param str gs_path:
    :return (str, str):
    """
    path = strip_protocol_from_path(gs_path).split("/")
    return path[0], join(*path[1:])


def strip_protocol_from_path(path):
    """Strip the `gs://` protocol from the path.

    :param str path:
    :return str:
    """
    if not path.startswith(CLOUD_STORAGE_PROTOCOL):
        return path
    return path.split(":")[1].lstrip("/")


def relpath(path, start):
    """Compute the relative path of an object in a bucket.

    :param str path:
    :param str start:
    :return str:
    """
    if start is not None:
        start = strip_protocol_from_path(start)

    return os.path.relpath(strip_protocol_from_path(path), start)


def split(path):
    """Split a path into its head and tail. `storage.path.split` (this function) is the analogue of `os.path.split` for
    Google Cloud Storage paths.

    :param str path:
    :return (str, str):
    """
    paths = path.split("/")
    return join(*paths[:-1]), paths[-1]


def dirname(path, name_only=False):
    """Get the path of the directory of the given path. If `name_only` is `True`, just return the name of the directory.

    :param str path:
    :param bool name_only:
    :return str:
    """
    directory_path = os.path.dirname(path)

    if name_only:
        return split(directory_path)[-1]

    return directory_path
