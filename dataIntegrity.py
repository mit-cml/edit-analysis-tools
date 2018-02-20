import xml.etree.ElementTree as etree
from functools import reduce


def check_blocks_corruption(blocks):
    """
    Checks raw blocks data (as a string) for corruption.
    Raises a BlocksXmlSanityException if any corruption is detected.
    Returns nothing.
    :param blocks:
    """

    # detect a class of data corruption: empty blocks
    if not blocks:
        raise BlocksXmlSanityException("Blocks data is empty.", blocks)

    # Checks if extra characters exist beyond the </xml>

    end = '</xml>'
    split_string = blocks.split(end)

    if len(split_string) != 2:
        raise BlocksXmlSanityException("Blocks data does not contain exactly one </xml> tag.", blocks)

    if split_string[1] != '':
        raise BlocksXmlSanityException("Blocks data has extra characters beyond </xml> tag.", blocks)

    # Checks xml sanity by parsing it

    try:
        etree.fromstring(blocks)
    except etree.ParseError:
        raise BlocksXmlSanityException("Blocks data is not sane- crashed XML parser.", blocks)


def check_all_fields_present(snapshot_dict):
    """
    Ensures necessary fields are present in a snapshot dictionary.
    Raises a FieldsMissingException if corruption is detected.
    Returns nothing.
    :param snapshot_dict: Dictionary of fields to check
    """
    fields_to_check = ['sendDate',
                       'userName',
                       'projectName',
                       'projectId',
                       'screenName',
                       'sessionId',
                       'form',
                       'blocks']
    fields_in_data = snapshot_dict['contents'].keys()
    t = [f in fields_in_data for f in fields_to_check]
    something_missing = not reduce(lambda x, y: x and y, t)
    if something_missing:
        # at least one field is missing
        num_missing = t.count(False)
        first_missing = t.index(False)
        raise FieldsMissingException("Missing at least one field in data. Missing " + str(num_missing) +
                                     ". First missing = " + fields_to_check[first_missing], snapshot_dict)


class DataIntegrityException(Exception):
    def __init__(self, message, snapshot_contents):
        self.message = message
        self.snapshot_contents = snapshot_contents


class FieldsMissingException(DataIntegrityException):
    pass


class BlocksXmlSanityException(DataIntegrityException):
    pass
