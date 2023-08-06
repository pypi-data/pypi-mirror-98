# -*- coding: utf-8 -*-

from pip_services3_expressions.tokenizers.Token import Token
from pip_services3_expressions.tokenizers.TokenType import TokenType
from pip_services3_expressions.tokenizers.generic.GenericTokenizer import GenericTokenizer
from test.tokenizers.TokenizerFixture import TokenizerFixture


class TestGenericTokenizer:

    def test_expressions(self):
        token_string = 'A+B/123 - \t "xyz"\n <>-10.11# This is a comment'
        expected_tokens = [
            Token(TokenType.Word, 'A'),
            Token(TokenType.Symbol, "+"),
            Token(TokenType.Word, "B"),
            Token(TokenType.Symbol, "/"),
            Token(TokenType.Integer, "123"),
            Token(TokenType.Whitespace, " "),
            Token(TokenType.Symbol, "-"),
            Token(TokenType.Whitespace, " \t "),
            Token(TokenType.Quoted, '"xyz"'),
            Token(TokenType.Whitespace, "\n "),
            Token(TokenType.Symbol, "<>"),
            Token(TokenType.Float, "-10.11"),
            Token(TokenType.Comment, "# This is a comment"),
            Token(TokenType.Eof, None)
        ]
        tokenizer = GenericTokenizer()
        token_list = tokenizer.tokenize_buffer(token_string)

        TokenizerFixture.assert_are_equals_token_lists(expected_tokens, token_list)

    def test_word_token(self):
        token_string = 'A"xyz"Ebf_2\n2x_2'
        expected_tokens = [
            Token(TokenType.Word, "A"),
            Token(TokenType.Quoted, "xyz"),
            Token(TokenType.Word, "Ebf_2"),
            Token(TokenType.Whitespace, "\n"),
            Token(TokenType.Integer, "2"),
            Token(TokenType.Word, "x_2")
        ]
        tokenizer = GenericTokenizer()
        tokenizer.skip_eof = True
        tokenizer.decode_strings = True
        token_list = tokenizer.tokenize_buffer(token_string)

        TokenizerFixture.assert_are_equals_token_lists(expected_tokens, token_list)

    def test_number_token(self):
        token_string = "123-321 .543-.76-. -123.456"
        expected_tokens = [
            Token(TokenType.Integer, "123"),
            Token(TokenType.Integer, "-321"),
            Token(TokenType.Whitespace, " "),
            Token(TokenType.Float, ".543"),
            Token(TokenType.Float, "-.76"),
            Token(TokenType.Symbol, "-"),
            Token(TokenType.Symbol, "."),
            Token(TokenType.Whitespace, " "),
            Token(TokenType.Float, "-123.456")
        ]
        tokenizer = GenericTokenizer()
        tokenizer.skip_eof = True
        tokenizer.decode_strings = True
        token_list = tokenizer.tokenize_buffer(token_string)

        TokenizerFixture.assert_are_equals_token_lists(expected_tokens, token_list)

    def test_expression_token(self):
        token_string = "A + b / (3 - Max(-123, 1)*2)"

        tokenizer = GenericTokenizer()
        token_list = tokenizer.tokenize_buffer(token_string)

        assert 24 == len(token_list)

    def test_expression_token2(self):
        token_string = "1>2"
        expected_tokens = [
            Token(TokenType.Integer, "1"),
            Token(TokenType.Symbol, ">"),
            Token(TokenType.Integer, "2"),
        ]

        tokenizer = GenericTokenizer()
        tokenizer.skip_eof = True
        token_list = tokenizer.tokenize_buffer(token_string)

        TokenizerFixture.assert_are_equals_token_lists(expected_tokens, token_list)
