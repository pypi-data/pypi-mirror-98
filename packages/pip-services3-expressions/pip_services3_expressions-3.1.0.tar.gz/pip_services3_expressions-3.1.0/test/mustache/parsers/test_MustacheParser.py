# -*- coding: utf-8 -*-

from pip_services3_expressions.mustache.parsers.MustacheParser import MustacheParser
from pip_services3_expressions.mustache.parsers.MustacheToken import MustacheToken
from pip_services3_expressions.mustache.parsers.MustacheTokenType import MustacheTokenType


class TestMustacheParser:

    def test_lexical_analysis(self):
        parser = MustacheParser()
        parser.template = "Hello, {{{NAME}}}{{ #if ESCLAMATION }}!{{/if}}{{{^ESCLAMATION}}}.{{{/ESCLAMATION}}}"
        expected_tokens = [
            MustacheToken(MustacheTokenType.Value, "Hello, "),
            MustacheToken(MustacheTokenType.EscapedVariable, "NAME"),
            MustacheToken(MustacheTokenType.Section, "ESCLAMATION"),
            MustacheToken(MustacheTokenType.Value, "!"),
            MustacheToken(MustacheTokenType.SectionEnd, None),
            MustacheToken(MustacheTokenType.InvertedSection, "ESCLAMATION"),
            MustacheToken(MustacheTokenType.Value, "."),
            MustacheToken(MustacheTokenType.SectionEnd, "ESCLAMATION"),
        ]

        tokens = parser.initial_tokens
        assert len(expected_tokens) == len(tokens)

        for i in range(len(tokens)):
            assert expected_tokens[i].type == tokens[i].type
            assert expected_tokens[i].value == tokens[i].value

    def test_syntax_analysis(self):
        parser = MustacheParser()
        parser.template = "Hello, {{{NAME}}}{{ #if ESCLAMATION }}!{{/if}}{{{^ESCLAMATION}}}.{{{/ESCLAMATION}}}"

        expected_tokens = [
            MustacheToken(MustacheTokenType.Value, "Hello, "),
            MustacheToken(MustacheTokenType.EscapedVariable, "NAME"),
            MustacheToken(MustacheTokenType.Section, "ESCLAMATION"),
            MustacheToken(MustacheTokenType.InvertedSection, "ESCLAMATION"),
        ]

        tokens = parser.result_tokens
        assert len(expected_tokens) == len(tokens)

        for i in range(len(tokens)):
            assert expected_tokens[i].type == tokens[i].type
            assert expected_tokens[i].value == tokens[i].value

    def test_variable_names(self):
        parser = MustacheParser()
        parser.template = "Hello, {{{NAME}}}{{ #if ESCLAMATION }}!{{/if}}{{{^ESCLAMATION}}}.{{{/ESCLAMATION}}}"
        assert 2 == len(parser.variable_names)
        assert 'NAME' == parser.variable_names[0]
        assert "ESCLAMATION" == parser.variable_names[1]
