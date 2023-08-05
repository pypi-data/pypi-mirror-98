"""
Module for converting lark parse trees to their equivalent dictionary models.
"""

from lark import Tree
from lark.lexer import Token

from .exceptions import NestedDescriptions, UnsupportedStartRule

from .hgvs_parser import parse


def to_model(description, start_rule=None):
    """
    Convert an  HGVS description, or parts of it, e.g., a location,
    a variants list, etc., if an appropriate alternative `start_rule`
    is provided, to a nested dictionary model.

    :arg str description: HGVS description.
    :arg str start_rule: Alternative start rule.
    :returns: Description dictionary model.
    :rtype: dict
    """
    parse_tree = parse(description, start_rule=start_rule)
    return _parse_tree_to_model(parse_tree, start_rule)


def _parse_tree_to_model(parse_tree, start_rule=None):
    """
    Convert a parse tree to a nested dictionary model.

    :arg lark.Tree parse_tree: HGVS description.
    :arg str start_rule: Alternative start rule.
    :returns: Description dictionary model.
    :rtype: dict
    """
    if start_rule is None:
        return _description_to_model(parse_tree)
    if start_rule == "reference":
        return _reference_to_model(parse_tree)
    elif start_rule == "variants":
        return _variants_to_model(parse_tree)
    elif start_rule == "variant":
        return _variant_to_model(parse_tree)
    elif start_rule == "location":
        return _location_to_model(parse_tree)
    elif start_rule == "inserted":
        return _inserted_to_model(parse_tree)
    raise UnsupportedStartRule(start_rule)


def _description_to_model(parse_tree):
    """
    Convert a lark tree obtained by parsing an HGVS description to
    a nested dictionary model.

    :arg lark.Tree parse_tree: Lark based parse tree.
    :returns: Dictionary model.
    :rtype: dict
    """
    model = {}
    if isinstance(parse_tree, Tree):
        for child in parse_tree.children:
            if isinstance(child, Token):
                if child.type == "COORDINATE_SYSTEM":
                    model["coordinate_system"] = child.value
            elif isinstance(parse_tree, Tree):
                if child.data == "reference":
                    model["reference"] = _reference_to_model(child)
                elif child.data == "variants":
                    model["variants"] = _variants_to_model(child)
    return model


def _reference_to_model(reference):
    """
    Convert a lark tree corresponding to the `reference` rule to its
    dictionary model.

    :arg lark.Tree reference: Lark reference parse tree.
    :returns: Dictionary model.
    :rtype: dict
    """
    if len(reference.children) == 1:
        return {"id": reference.children[0].value}
    elif len(reference.children) == 2:
        return {
            "id": reference.children[0].value,
            "selector": _reference_to_model(reference.children[1]),
        }


def _variants_to_model(variants):
    """
    Convert a lark tree corresponding to the `variants` rule to its
    dictionary model.

    :arg lark.Tree variants: Lark parse tree.
    :returns: Dictionary model.
    :rtype: dict
    """
    output = []
    for variant in variants.children:
        output.append(_variant_to_model(variant))
    return output


def _variant_to_model(variant):
    """
    Converts the lark tree corresponding to the `variant` rule to its
    dictionary model.

    :arg lark.Tree variant: Lark parse tree.
    :returns: Dictionary model.
    :rtype: dict
    """
    if variant.data == "_ambig":
        variant = _solve_variant_ambiguity(variant)

    output = {"location": _location_to_model(variant.children[0])}
    if len(variant.children) == 2:
        variant = variant.children[1]
        output["type"] = variant.data
        output["source"] = "reference"
        if len(variant.children) == 1:
            if variant.data == "deletion":
                output["deleted"] = _deleted_to_model(variant.children[0])
            else:
                output["inserted"] = _inserted_to_model(variant.children[0])
        elif len(variant.children) == 2:
            output["deleted"] = _deleted_to_model(variant.children[0])
            output["inserted"] = _inserted_to_model(variant.children[1])

    return output


def _solve_variant_ambiguity(variant):
    """
    Deals with the following type of ambiguities:
        - `REF1:100insREF2:100_200`
          where the variant can be seen as a repeat in which `insREF2` is
          wrongly interpreted as a reference, or as an insertion (correct).
          This applies to other variant types also.
        - `REF1:100delinsREF2:100_200`
          where this variant can be seen as a deletion in which `insREF2` is
          wrongly interpreted as a reference, or as a deletion insertion, case
          in which `REF2` is the reference (correct).
    :arg lark.Tree variant: Lark parse tree.
    :returns: Valid tree path.
    :rtype: lark.Tree
    """
    if variant.children[0].children[1].data == "repeat":
        return variant.children[1]
    elif variant.children[1].children[1].data == "repeat":
        return variant.children[0]
    elif (
        variant.children[0].children[1].data == "deletion_insertion"
        and variant.children[1].children[1].data == "deletion"
    ):
        return variant.children[0]
    elif (
        variant.children[1].children[1].data == "deletion_insertion"
        and variant.children[0].children[1].data == "deletion"
    ):
        return variant.children[1]


def _location_to_model(location):
    """
    Converts the lark tree corresponding to the location rule to its
    dictionary model.

    :arg lark.Tree location: Lark parse tree.
    :returns: Dictionary model.
    :rtype: dict
    """
    location = location.children[0]
    if location.data == "range":
        return _range_to_model(location)
    elif location.data in ["point", "uncertain_point"]:
        return _point_to_model(location)


def _range_to_model(range_location):
    """
    Converts the lark tree corresponding to a `range` location
    rule to its dictionary model.

    :arg lark.Tree range_location: Lark parse tree.
    :returns dict: Dictionary model.
    """
    range_location = {
        "type": "range",
        "start": _point_to_model(range_location.children[0]),
        "end": _point_to_model(range_location.children[1]),
    }
    return range_location


def _point_to_model(point):
    """
    Converts a lark tree corresponding to a point/uncertain point rule
    to a dictionary model.

    :arg lark.Tree point: Point parse tree.
    :returns dict: Dictionary model.
    """
    if point.data == "uncertain_point":
        return {**_range_to_model(point), **{"uncertain": True}}
    output = {"type": "point"}
    for token in point.children:
        if token.type == "OUTSIDE_CDS":
            if token.value == "*":
                output["outside_cds"] = "downstream"
            elif token.value == "-":
                output["outside_cds"] = "upstream"
        elif token.type == "NUMBER":
            output["position"] = int(token.value)
        elif token.type == "UNKNOWN":
            output["uncertain"] = True
        elif token.type == "OFFSET":
            output["offset"] = _offset_to_model(token)
    return output


def _offset_to_model(offset):
    """
    Converts a lark token corresponding to a point offset
    to a dictionary model.

    :arg lark.lexer.Token offset: Point offset token.
    :returns dict: Dictionary model.
    """
    output = {}
    if "?" in offset.value:
        output["uncertain"] = True
        if "+" in offset.value:
            output["downstream"] = True
        elif "-" in offset.value:
            output["upstream"] = True
    else:
        output["value"] = int(offset.value)
    return output


def _length_to_model(length):
    """
    Converts a lark tree corresponding to a length rule to a
    dictionary model.

    :arg lark.Tree_or_lark.lexer.Token: Lark parse tree / token.
    :returns dict: Dictionary model.
    """
    length = length.children[0]
    if isinstance(length, Token):
        return _length_point_to_model(length)
    elif length.data == "exact_range":
        return {
            "type": "range",
            "start": _length_point_to_model(length.children[0]),
            "end": _length_point_to_model(length.children[1]),
            "uncertain": True,
        }


def _length_point_to_model(length_point):
    """
    Generates a point dictionary model from a lark token that
    corresponds to a length instance.

    :arg lark.lexer.Token length_point: Length point token.
    :returns dict: Dictionary model.
    """
    if length_point.type == "UNKNOWN":
        return {"type": "point", "uncertain": True}
    if length_point.type == "NUMBER":
        return {"type": "point", "value": int(length_point.value)}


def _deleted_to_model(deleted):
    """
    Generates a deleted dictionary model from a lark token or parse
    tree that corresponds to a deleted instance.

    :arg lark.Tree/lark.lexer.Token deleted: Lark parse tree / token.
    :returns: Dictionary model.
    :rtype: dict
    """
    if isinstance(deleted, Token):
        return [{"sequence": deleted.value, "source": "description"}]
    return _inserted_to_model(deleted)


def _inserted_to_model(inserted):
    """
    Converts a lark tree corresponding to the inserted rule to its
    equivalent dictionary model.

    :arg lark.Tree inserted: Inserted parse tree.
    :returns: Dictionary model.
    :rtype: dict
    """
    output = []
    for inserted_subtree in inserted.children:
        if inserted_subtree.data == "_ambig":
            inserted_subtree = _solve_insert_ambiguity(inserted_subtree)
        output.extend(_insert_to_model(inserted_subtree))
    return output


def _insert_to_model(insert):
    """
    Converts a lark tree corresponding to the `insert` rule to its
    equivalent dictionary model.

    :arg lark.Tree insert: Lark parse tree.
    :returns dict: Dictionary model.
    """
    if (
        isinstance(insert.children[0], Tree)
        and insert.children[0].data == "repeat_mixed"
    ):
        return _repeat_mixed_to_model(insert)
    output = {}
    for insert_part in insert.children:
        if isinstance(insert_part, Token):
            if insert_part.type == "SEQUENCE":
                output.update({"sequence": insert_part.value, "source": "description"})
            elif insert_part.type == "INVERTED":
                output["inverted"] = True
        elif isinstance(insert_part, Tree):
            output.update(_insert_tree_part_to_model(insert_part))
    return [output]


def _insert_tree_part_to_model(insert_part):
    """
    Converts a lark tree corresponding to an insert part to its
    equivalent dictionary model.

    :arg lark.Tree insert_part: Insert part parse tree.
    :returns dict: Dictionary model.
    """
    output = {}
    if insert_part.data == "location":
        output["location"] = _location_to_model(insert_part)
        output["source"] = "reference"
    elif insert_part.data == "length":
        output["length"] = _length_to_model(insert_part)
    elif insert_part.data == "repeat_number":
        output["repeat_number"] = _length_to_model(insert_part)
    elif insert_part.data == "description":
        output.update(_insert_description_to_model(insert_part))
    return output


def _repeat_mixed_to_model(insert):
    """
    Converts a lark tree corresponding to a mixed repeat insert,
    e.g., `AA[50][60]` equivalent dictionary model.

    :arg lark.Tree insert: Lark parse tree.
    :returns dict: Dictionary model.
    """
    output = []
    for repeat_mixed in insert.children:
        output.extend(_insert_to_model(repeat_mixed))
    return output


def _insert_description_to_model(insert_description):
    """
    Converts a lark tree corresponding to an insert description part, e.g,
    `R1:500` to its equivalent dictionary model.

    :arg lark.Tree insert_description: Lark parse tree.
    :returns dict: Dictionary model.
    """
    output = {}
    for description_part in insert_description.children:
        if (
                isinstance(description_part, Token)
                and description_part.type == "COORDINATE_SYSTEM"
        ):
            output["coordinate_system"] = description_part.value
        elif description_part.data == "variants":
            if len(description_part.children) != 1:
                raise NestedDescriptions()
            variant = description_part.children[0]
            if len(variant.children) != 1:
                raise NestedDescriptions()
            else:
                output["location"] = _location_to_model(variant.children[0])
        elif description_part.data == "reference":
            output["source"] = _reference_to_model(description_part)
    print(output)
    return output


def _solve_insert_ambiguity(insert):
    """
    Deals with ambiguities in the `insert` description part
    that arise between locations and lengths.

    Example:
    - REF:100>200 - 200 can be interpreted as a location or a length.

    We interpret insert as length (size) for the following:
    - NUMBER
    - (NUMBER)
    - (NUMBER_NUMBER)
    Examples:
    - 10, (10) something of length 10 is inserted;
    - (10_20): something of a length between 10 and 20 is inserted.
    - (?_20)
    - (20_?)
    - ?

    We interpret insert as location for the following:
    - point_point
    - (point_point)_point
    - point_(point_point)
    Examples:
    - 10_20
    - 10_(20_30)
    - (10_20)_30
    - (10_20)_(30_40)
    """
    if len(insert.children) == 2:
        if (
            insert.children[0].children[0].data == "length"
            and insert.children[1].children[0].data == "location"
        ):
            return insert.children[0]
        elif (
            insert.children[0].children[0].data == "location"
            and insert.children[1].children[0].data == "length"
        ):
            return insert.children[1]
