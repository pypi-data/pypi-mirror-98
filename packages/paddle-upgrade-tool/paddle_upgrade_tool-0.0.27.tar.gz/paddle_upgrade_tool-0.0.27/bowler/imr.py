#!/usr/bin/env python3
#
# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import logging
from typing import Any, List, Optional

from fissix.fixer_util import LParen, Name

from .helpers import find_last
from .types import (
    ARG_END,
    ARG_LISTS,
    LN,
    STARS,
    SYMBOL,
    TOKEN,
    Capture,
    IMRError,
    Leaf,
    Node,
)

log = logging.getLogger(__name__)


class FunctionArgument:
    def __init__(self, name="", value=None, annotation="", star=None, prefix=None):
        self.name       = name
        self.value      = value
        self.annotation = annotation
        self.star       = star
        self.prefix     = prefix

    @classmethod
    def build(cls, leaf, is_def, **kwargs):
        while leaf is not None and leaf.type not in ARG_END:
            if leaf.type in (SYMBOL.star_expr, SYMBOL.argument):
                return cls.build(leaf.children[0], is_def, prefix=leaf.prefix)

            elif leaf.type in STARS:
                kwargs["star"] = leaf.clone()

            elif leaf.type == SYMBOL.tname:
                kwargs["name"] = leaf.children[0].value
                kwargs["annotation"] = leaf.children[-1].value

            elif leaf.type == TOKEN.EQUAL:
                pass

            elif leaf.type == TOKEN.NAME:
                if (is_def and "name" not in kwargs) or (
                    leaf.next_sibling and leaf.next_sibling.type == TOKEN.EQUAL
                ):
                    kwargs["name"] = leaf.value
                else:
                    kwargs["value"] = leaf.clone()

            else:
                # assume everything else is a complex value
                kwargs["value"] = leaf.clone()

            kwargs.setdefault("prefix", leaf.prefix)
            leaf = leaf.next_sibling

        return FunctionArgument(**kwargs)

    @classmethod
    def build_list(
        cls, arguments, is_def
    ):
        result = []

        # empty function
        if not arguments:
            return result

        # only care about what's on the inside
        if arguments[0].type in ARG_LISTS:
            leaf = arguments[0].children[0]
        else:
            leaf = arguments[0]

        while leaf is not None:
            arg = cls.build(leaf, is_def)
            log.debug("{} -> {}".format(leaf, arg))
            result.append(arg)

            # consume leafs for this argument
            while leaf is not None and leaf.type not in ARG_END:
                log.debug("consuming {}".format(leaf))
                leaf = leaf.next_sibling

            # assume we stopped on a comma or parenthesis
            if leaf:
                log.debug("separator {}".format(leaf))
                leaf = leaf.next_sibling

        return result

    def explode(self, is_def, prefix = ""):
        result = []
        prefix = self.prefix if self.prefix else prefix
        if is_def:
            if self.star:
                self.star.prefix = prefix
                result.append(self.star)
                prefix = ""

            if self.annotation:
                result.append(
                    Node(
                        SYMBOL.tname,
                        [
                            Name(self.name, prefix=prefix),
                            Leaf(TOKEN.COLON, ":", prefix=""),
                            Name(self.annotation, prefix=" "),
                        ],
                        prefix=prefix,
                    )
                )
            else:
                result.append(Name(self.name, prefix=prefix))

            if self.value:
                space = " " if self.annotation else ""
                result.append(Leaf(TOKEN.EQUAL, "=", prefix=space))
                result.append(self.value)

        else:
            if self.star:
                if self.star.type == TOKEN.STAR:
                    node = Node(SYMBOL.star_expr, [self.star], prefix=prefix)
                elif self.star.type == TOKEN.DOUBLESTAR:
                    node = Node(SYMBOL.argument, [self.star], prefix=prefix)

                if self.value:
                    self.value.prefix = ""
                    node.append_child(self.value)

                result.append(node)
                return result

            if self.name:
                self.value.prefix = ""
                result.append(
                    Node(
                        SYMBOL.argument,
                        [
                            Name(self.name, prefix=prefix),
                            Leaf(TOKEN.EQUAL, value="=", prefix=""),
                            self.value,
                        ],
                        prefix=prefix,
                    )
                )
            else:
                self.value.prefix = prefix
                result.append(self.value)

        return result

    @classmethod
    def explode_list(
        cls, arguments, is_def
    ):
        nodes = []
        prefix = ""
        index = 0
        for argument in arguments:
            if index:
                nodes.append(Leaf(TOKEN.COMMA, ",", prefix=""))
                prefix = " "

            result = argument.explode(is_def, prefix=prefix)
            log.debug("{} -> {}".format(argument, result))
            nodes.extend(result)
            index += 1

        if not nodes:
            return None

        if len(nodes) == 1:
            return nodes[0]

        elif is_def:
            return Node(SYMBOL.typedargslist, nodes, prefix=nodes[0].prefix)

        else:
            return Node(SYMBOL.arglist, nodes, prefix=nodes[0].prefix)


class FunctionSpec:
    def __init__(self, name, argument, is_def, capture, node):
        self.name = name
        self.arguments = arguments
        self.is_def = is_def
        self.capture = capture
        self.node = node

    @classmethod
    def build(cls, node, capture):
        try:
            name = capture["function_name"]
            is_def = "function_def" in capture
            args = capture["function_arguments"]
        except KeyError as e:
            raise IMRError("function spec invalid") from e

        arguments = FunctionArgument.build_list(args, is_def)

        return FunctionSpec(name.value, arguments, is_def, capture, node)

    def explode(self):
        arguments = FunctionArgument.explode_list(self.arguments, self.is_def)

        rparen = find_last(self.capture["function_parameters"], TOKEN.RPAR)
        rprefix = rparen.prefix if rparen else ""

        if self.is_def:
            parameters = Node(
                SYMBOL.parameters,
                [LParen(), Leaf(TOKEN.RPAR, ")", prefix=rprefix)],
                prefix="",
            )
        else:
            parameters = Node(
                SYMBOL.trailer,
                [LParen(), Leaf(TOKEN.RPAR, ")", prefix=rprefix)],
                prefix="",
            )

        if arguments:
            parameters.insert_child(1, arguments)

        self.capture["function_parameters"].replace(parameters)

        return self.node
