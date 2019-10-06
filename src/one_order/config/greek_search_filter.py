from __future__ import unicode_literals

import operator, unidecode
from functools import reduce

from django.db import models
from django.utils import six
from rest_framework.compat import (
    distinct
)
from rest_framework.filters import SearchFilter
import unicodedata as ud


def is_latin(uchr):
    latin_letters = {}
    try:
        return latin_letters[uchr]
    except KeyError:
        return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))

def only_roman_chars(unistr):
    return all(is_latin(uchr)
               for uchr in unistr
               if uchr.isalpha())  # isalpha suggested by John Machin

class GreekSearchFilter(SearchFilter):
    def get_search_terms(self, request):
        """
        Override to remove greek acceents from search.
        Latin characters apply to latin fields
        Greek characters apply to latin and greek fields, not caring about accents
        Case insensitive search
        """
        params = request.query_params.get(self.search_param, '')
        params = params.replace(',', ' ').split()
        param_list = []
        for param in params:
            param_list.append(unidecode.unidecode(param))

        print(param_list)

        return param_list
