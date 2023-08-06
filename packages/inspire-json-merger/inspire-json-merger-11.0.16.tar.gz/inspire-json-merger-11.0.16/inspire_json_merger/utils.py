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

"""Helper functions for authors."""

from __future__ import absolute_import, division, print_function

import re
import six
from pyrsistent import freeze, thaw
from six.moves import zip

split_on_re = re.compile(r'[\.\s-]')

ORDER_KEY = "__pos"


def scan_author_string_for_phrases(s):
    """Scan a name string and output an object representing its structure.
    Example:
        Sample output for the name 'Jingleheimer Schmitt, John Jacob, XVI.' is::
            {
                'TOKEN_TAG_LIST' : ['lastnames', 'nonlastnames', 'titles', 'raw'],
                'lastnames'      : ['Jingleheimer', 'Schmitt'],
                'nonlastnames'   : ['John', 'Jacob'],
                'titles'         : ['XVI.'],
                'raw'            : 'Jingleheimer Schmitt, John Jacob, XVI.'
            }
    :param s: the input to be lexically tagged
    :type s: string
    :returns: dict of lexically tagged input items.
    :rtype: dict
    """

    if not isinstance(s, six.text_type):
        s = s.decode('utf-8')

    retval = {
        'TOKEN_TAG_LIST': [
            'lastnames',
            'nonlastnames',
            'titles',
            'raw'],
        'lastnames': [],
        'nonlastnames': [],
        'titles': [],
        'raw': s}
    l = s.split(',')  # noqa: E741
    if len(l) < 2:
        # No commas means a simple name
        new = s.strip()
        new = new.split(' ')
        if len(new) == 1:
            retval['lastnames'] = new        # rare single-name case
        else:
            retval['lastnames'] = new[-1:]
            retval['nonlastnames'] = new[:-1]
            for tag in ['lastnames', 'nonlastnames']:
                retval[tag] = [x.strip() for x in retval[tag]]
                retval[tag] = [re.split(split_on_re, x)
                               for x in retval[tag]]
                # flatten sublists
                retval[tag] = [item for sublist in retval[tag]
                               for item in sublist]
                retval[tag] = [x for x in retval[tag] if x != '']
    else:
        # Handle lastname-first multiple-names case
        retval['titles'] = l[2:]             # no titles? no problem
        retval['nonlastnames'] = l[1]
        retval['lastnames'] = l[0]
        for tag in ['lastnames', 'nonlastnames']:
            retval[tag] = retval[tag].strip()
            retval[tag] = re.split(split_on_re, retval[tag])
            # filter empty strings
            retval[tag] = [x for x in retval[tag] if x != '']
        retval['titles'] = [x.strip() for x in retval['titles'] if x != '']

    return retval


def filter_conflicts(conflicts_list, fields):
    """Use this function to automatically filter all the entries defined for a
    given rule.

    Params:
        conflicts_list(List[Conflict]): the list of conflicts to filter.
        fields(List[str]): fields to filter out, using an accessor syntax of
            the form ``field.subfield.subsubfield``.

    Return:
        List[Conflict]: the given list filtered by `fields`
    """
    for field in fields:
        conflicts_list = filter_conflicts_by_path(conflicts_list, field)

    return conflicts_list


def filter_conflicts_by_path(conflict_list, to_delete_path):
    """Filter a list of conflict for the given string. The string represents
    the path of the conflict in the form ``field.subfield.subsubfield``.

    Example:
        conflict_list = [
            ('SET_FIELD', ('figures', 0, 'key'), 'figure1.png'),
            ('SET_FIELD', ('figures', 1, 'key'), 'figure2.png')
        ]

        to_delete_path = 'figures.keys'
    """
    return [conf for conf in conflict_list if not is_to_delete(conf, to_delete_path)]


def is_to_delete(conflict, keys_path):
    to_delete = keys_path.split('.')
    conflict_path = conflict_to_list(conflict)
    if conflict[0] == 'MANUAL_MERGE':
        return False
    if len(to_delete) > len(conflict_path):
        return False

    return all(x == y for (x, y) in zip(to_delete, conflict_path))


def conflict_to_list(conflict):
    path = conflict[1]
    return [p for p in path if not isinstance(p, int)]


def filter_records(root, head, update, filters=()):
    """Apply the filters to the records."""
    root, head, update = freeze(root), freeze(head), freeze(update)
    for filter_ in filters:
        root, head, update = filter_(root, head, update)

    return thaw(root), thaw(head), thaw(update)
