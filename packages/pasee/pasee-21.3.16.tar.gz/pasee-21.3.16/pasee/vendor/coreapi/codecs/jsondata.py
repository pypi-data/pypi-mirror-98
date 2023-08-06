# coding: utf-8
from pasee.vendor.coreapi.codecs.base import BaseCodec
from pasee.vendor.coreapi.exceptions import ParseError
import collections
import json


class JSONCodec(BaseCodec):
    media_type = "application/json"
    format = "json"

    def decode(self, bytestring, **options):
        """
        Return raw JSON data.
        """
        try:
            return json.loads(
                bytestring.decode("utf-8"), object_pairs_hook=collections.OrderedDict
            )
        except ValueError as exc:
            raise ParseError("Malformed JSON. %s" % exc)
