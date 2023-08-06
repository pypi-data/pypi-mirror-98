# -*- coding: utf-8 -*-

from pip_services3_expressions.calculator.tokenizers.ExpressionTokenizer import ExpressionTokenizer
from pip_services3_expressions.tokenizers.Token import Token
from pip_services3_expressions.tokenizers.TokenType import TokenType

from test.tokenizers.TokenizerFixture import TokenizerFixture


class TestExpressionTokenizer:
    def tests_quote_token(self):
        token_string = "A'xyz'\"abc\ndeg\" 'jkl\"def'\"ab\"\"de\"'df''er'"
        expected_tokens = [
            Token(TokenType.Word, "A"), Token(TokenType.Quoted, "xyz"),
            Token(TokenType.Word, "abc\ndeg"), Token(TokenType.Whitespace, " "),
            Token(TokenType.Quoted, "jkl\"def"), Token(TokenType.Word, "ab\"de"),
            Token(TokenType.Quoted, "df'er")
        ]

        tokenizer = ExpressionTokenizer()
        tokenizer.skip_eof = True
        tokenizer.decode_strings = True
        token_list = tokenizer.tokenize_buffer(token_string)

        TokenizerFixture.assert_are_equals_token_lists(expected_tokens, token_list)

    def test_word_token(self):
        token_string = "A'xyz'Ebf_2\n2_2"
        expected_tokens = [Token(TokenType.Word, "A"), Token(TokenType.Quoted, "xyz"),
                           Token(TokenType.Word, "Ebf_2"), Token(TokenType.Whitespace, "\n"),
                           Token(TokenType.Integer, "2"), Token(TokenType.Word, "_2")]
        tokenizer = ExpressionTokenizer()
        tokenizer.skip_eof = True
        tokenizer.decode_strings = True
        token_list = tokenizer.tokenize_buffer(token_string)

        TokenizerFixture.assert_are_equals_token_lists(expected_tokens, token_list)

    def test_number_token(self):
        token_string = "123-321 .543-.76-. 123.456 123e45 543.11E+43 1e 3E-"
        expected_tokens = [
            Token(TokenType.Integer, "123"), Token(TokenType.Symbol, "-"),
            Token(TokenType.Integer, "321"), Token(TokenType.Whitespace, " "),
            Token(TokenType.Float, ".543"), Token(TokenType.Symbol, "-"),
            Token(TokenType.Float, ".76"), Token(TokenType.Symbol, "-"),
            Token(TokenType.Symbol, "."), Token(TokenType.Whitespace, " "),
            Token(TokenType.Float, "123.456"), Token(TokenType.Whitespace, " "),
            Token(TokenType.Float, "123e45"), Token(TokenType.Whitespace, " "),
            Token(TokenType.Float, "543.11E+43"), Token(TokenType.Whitespace, " "),
            Token(TokenType.Integer, "1"), Token(TokenType.Word, "e"),
            Token(TokenType.Whitespace, " "), Token(TokenType.Integer, "3"),
            Token(TokenType.Word, "E"), Token(TokenType.Symbol, "-")
        ]

        tokenizer = ExpressionTokenizer()
        tokenizer.skip_eof = True
        tokenizer.decode_strings = True
        token_list = tokenizer.tokenize_buffer(token_string)

        TokenizerFixture.assert_are_equals_token_lists(expected_tokens, token_list)

    def test_expression_token(self):
        token_string = "A + b / (3 - Max(-123, 1)*2)"

        tokenizer = ExpressionTokenizer()
        token_list = tokenizer.tokenize_buffer(token_string)

        assert 25 == len(token_list)
