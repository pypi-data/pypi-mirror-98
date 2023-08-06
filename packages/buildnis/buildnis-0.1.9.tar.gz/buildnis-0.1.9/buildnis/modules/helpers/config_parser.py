# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     config_parser.py
# Date:     28.Feb.2021
###############################################################################

from __future__ import annotations

import logging
import re
from typing import List

from buildnis.modules.helpers.file_compare import FileCompare
from buildnis.modules.helpers.placeholder_regex import (
    placeholder_regex,
    replaceConstants,
)


############################################################################
def expandItem(item: str, parents: List[object]) -> object:
    """Parses the given item, if it contains a placeholder, that placeholder
    is expanded. If the item doesn't contain a placeholder, the item's
    unaltered string is returned.

    Args:
        item (str): The item to parse and expand its placeholder
        parents (List[object]): The parents of the item to search for
                                the placeholder's content.

    Returns:
        object: The expanded string if the item contained a placeholder, the
             original string else. If the placeholder points to another
             object that is not a string, this object is returned.
    """
    ret_val = replaceConstants(item)

    result = placeholder_regex.search(ret_val)
    parent_to_use_id = 0
    if result:
        # print("Found Placeholder: {place}".format(place=result.group(1)))
        placeholder = result.group(1)
        parent_regex = re.compile(r"(\.\./)")

        result = parent_regex.match(placeholder)
        while result is not None:
            placeholder = placeholder.removeprefix("../")
            result = parent_regex.match(placeholder)
            parent_to_use_id -= 1

        try:
            substitute = getPlaceholder(
                parents=parents,
                parent_to_use_id=parent_to_use_id,
                placeholder=placeholder,
            )
        except Exception:
            return ret_val

        if isinstance(substitute, str):
            ret_val = placeholder_regex.sub(substitute, item)
        else:
            ret_val = substitute

    return ret_val


################################################################################
def getPlaceholder(
    parents: List[object], parent_to_use_id: int, placeholder: str
) -> object:
    """Returns the expanded placeholder. Searches for the attribute with name
        `placeholder` or the value of the key `placeholder` in the parent.

    Args:
        parents (List[object]): The list of parents to search the expansion in.
        parent_to_use_id (int): The id of the parent in the list, to use for the
                                replacement.
        placeholder (str): The string to replace with an element of the same name

    Raises:
        Exception:  if the replacement of the placeholder from the parent element throws
                    an exception.

    Returns:
        object: The replacement for the placeholder.
    """
    try:
        parent = parents[parent_to_use_id]

        if isinstance(parent[placeholder], str):
            substitute = parent[placeholder].replace("\\", "\\\\")
        else:
            substitute = parent[placeholder]
        # print("Replace {ph} with: {elem}".format(ph=placeholder, elem=substitute))
    except Exception:
        try:
            parent = parents[parent_to_use_id]
            if isinstance(getattr(parent, placeholder), str):
                substitute = getattr(parent, placeholder).replace("\\", "\\\\")
            else:
                substitute = getattr(parent, placeholder)
                # print(
                #     "Replace {ph} with: {elem}, class".format(
                #         ph=placeholder, elem=substitute
                #     )
                # )
        except Exception as excp:
            raise excp

    return substitute


###############################################################################
def parseConfigElement(element: object, parents: List[object] = None) -> object:
    """Parses the given config element and replaces placeholders.
    Placeholders are strings of the form `${PLACEHOLDER}`, with start with a
    dollar sign followed by an opening curly brace and end with a curly brace.
    The string between the two curly braces is changed against it's value.

    Args:
        element (object): The configuration element to parse and expand.
        parent (List[object], optional): The parent and the parent's parent and it's
        parent as a list, starting with the parent as first element. Defaults to None.

    Returns:
        object: The parsed and expanded object.
    """
    if parents is None:
        parents = []
    # print("parseConfigElement: {element}, parents: {parents}".format(
    #    element=element.__class__, parents=len(parents)))
    local_parents = parents.copy()

    ret_val = element

    if isinstance(element, list):
        ret_val = parseList(element, local_parents)

    elif isinstance(element, FileCompare):
        ret_val = element

    elif isinstance(element, logging.Logger):
        ret_val = element

    elif isinstance(element, str):
        ret_val = expandItem(element, local_parents)

    elif hasattr(element, "__dict__"):
        local_parents = parents.copy()
        local_parents.append(element)
        for key in element.__dict__:
            element.__dict__[key] = parseConfigElement(
                element.__dict__[key], local_parents
            )
        ret_val = element

    return ret_val


################################################################################
def parseList(element: List[object], local_parents: List[object]) -> List[object]:
    """Parses the items of a list.

    Args:
        element (List[object]): The list to parse
        local_parents (List[object]): The list of parents

    Returns:
        List[object]: The parsed and, if applicable, expanded, list of items.
    """
    tmp_list = []
    for subitem in element:
        if hasattr(subitem, "__dict__"):
            tmp_list.append(parseConfigElement(subitem, local_parents))

        elif isinstance(subitem, dict):
            local_parents.append(element)
            for key in subitem:
                subitem[key] = parseConfigElement(subitem[key], local_parents)
            tmp_list.append(subitem)

        else:
            if isinstance(subitem, str):
                tmp_list.append(expandItem(subitem, local_parents))
            else:
                tmp_list.append(subitem)

    return tmp_list
