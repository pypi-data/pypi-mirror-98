# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

from __future__ import absolute_import, division, print_function
from six import text_type

from json_merger.comparator import PrimaryKeyComparator
from json_merger.contrib.inspirehep.author_util import (
    AuthorNameDistanceCalculator,
    AuthorNameNormalizer,
    NameInitial,
    NameToken,
)
from json_merger.contrib.inspirehep.comparators import \
    DistanceFunctionComparator
import unidecode

from inspire_json_merger.utils import scan_author_string_for_phrases
from json_merger.utils import get_obj_at_key_path


def author_tokenize(name):
    """This is how the name should be tokenized for the matcher."""
    phrases = scan_author_string_for_phrases(name)
    res = {'lastnames': [], 'nonlastnames': []}
    for key, tokens in phrases.items():
        lst = res.get(key)
        if lst is None:
            continue
        for token in tokens:
            if len(token) == 1:
                lst.append(NameInitial(token))
            else:
                lst.append(NameToken(token))
    return res


def normalize_title(data):
    data = data.lower()
    if not isinstance(data, text_type):
        data = data.decode('utf-8')
    data = unidecode.unidecode(data)
    return data


class IDNormalizer(object):
    """Callable that can be used to normalize by a given id for authors."""
    def __init__(self, id_type):
        self.id_type = id_type

    def __call__(self, author):
        for id_field in author.get('ids', []):
            if id_field.get('schema') == self.id_type:
                return id_field.get('value')
        # This is safe since the normalization is not the final decider.
        return None


class AuthorComparator(DistanceFunctionComparator):
    threshold = 0.12
    distance_function = AuthorNameDistanceCalculator(author_tokenize)
    norm_functions = [
        IDNormalizer('ORCID'),
        IDNormalizer('INSPIRE ID'),
        IDNormalizer('INSPIRE BAI'),
        AuthorNameNormalizer(author_tokenize),
        AuthorNameNormalizer(author_tokenize, asciify=True),
        AuthorNameNormalizer(author_tokenize, first_names_number=1),
        AuthorNameNormalizer(author_tokenize, first_names_number=1, asciify=True),
        AuthorNameNormalizer(author_tokenize, first_names_number=1, first_name_to_initial=True),
        AuthorNameNormalizer(author_tokenize, first_names_number=1, first_name_to_initial=True, asciify=True),
    ]


def get_pk_comparator(primary_key_fields, normalization_functions=None):
    class Ret(PrimaryKeyComparator):
        __doc__ = (
            'primary_key_fields:%s, normalization_functions:%s' % (
                primary_key_fields,
                normalization_functions,
            )
        )
    Ret.primary_key_fields = primary_key_fields
    Ret.normalization_functions = normalization_functions or {}
    return Ret


def get_pk_comparator_ignore_if_both_empty(primary_key_fields, normalization_functions=None):
    class Ret(PrimaryKeyComparator):
        __doc__ = (
            'primary_key_fields:%s, normalization_functions:%s' % (
                primary_key_fields,
                normalization_functions,
            )
        )

        def _have_field_equal(self, obj1, obj2, field):
            key_path = tuple(k for k in field.split('.') if k)
            o1 = get_obj_at_key_path(obj1, key_path, "")
            o2 = get_obj_at_key_path(obj2, key_path, "")

            fn = self.normalization_functions.get(field, lambda x: x)
            return fn(o1) == fn(o2)

    Ret.primary_key_fields = primary_key_fields
    Ret.normalization_functions = normalization_functions or {}
    return Ret


AffiliationComparator = get_pk_comparator([['record.$ref'], ['value']])
CollectionsComparator = get_pk_comparator(['primary'])
CreationDatetimeComparator = get_pk_comparator(['creation_datetime'])
DateComparator = get_pk_comparator(['date'])
FundingInfoComparator = get_pk_comparator(['project_number'])
ImprintsComparator = get_pk_comparator(['publisher'])
LanguageComparator = get_pk_comparator(['language'])
LicenseComparator = get_pk_comparator(['imposing'])
MaterialComparator = get_pk_comparator(['material'])
RefComparator = get_pk_comparator(['$ref'])
SchemaComparator = get_pk_comparator(['schema'])
SourceComparator = get_pk_comparator(['source'])
SourceValueComparator = get_pk_comparator([['source', 'value']])
TitleComparator = get_pk_comparator_ignore_if_both_empty(
    [['title', 'subtitle']],
    normalization_functions={'title': normalize_title, 'subtitle': normalize_title}
)
URLComparator = get_pk_comparator(['url'])
ValueComparator = get_pk_comparator(['value'])


PublicationInfoComparator = get_pk_comparator([
    ['journal_title', 'journal_volume']
])

FigureComparator = get_pk_comparator([
    ['key']
])

DocumentComparator = get_pk_comparator([
    ['source', 'description'],
    ['source', 'fulltext'],
    ['source', 'original_url'],
])

COMPARATORS = {
    '_desy_bookkeeping': DateComparator,
    '_private_notes': SourceComparator,
    'abstracts': SourceComparator,
    'acquisition_source': SourceComparator,
    'arxiv_eprints': ValueComparator,
    'authors': AuthorComparator,
    'authors.affiliations': AffiliationComparator,
    'authors.ids': SchemaComparator,
    'book_series': TitleComparator,
    'collaborations': ValueComparator,
    'copyright': MaterialComparator,
    'deleted_records': RefComparator,
    'documents': DocumentComparator,
    'dois': SourceValueComparator,
    'external_system_identifiers': SchemaComparator,
    'figures': FigureComparator,
    'funding_info': FundingInfoComparator,
    'imprints': ImprintsComparator,
    'isbns': ValueComparator,
    'keywords': ValueComparator,
    'license': LicenseComparator,
    'new_record': RefComparator,
    'persistent_identifiers': ValueComparator,
    'public_notes': SourceComparator,
    'publication_info': PublicationInfoComparator,
    'references.reference.authors': AuthorComparator,
    'report_numbers': SourceValueComparator,
    'title_translations': LanguageComparator,
    'titles': TitleComparator,
}
