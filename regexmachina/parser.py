from sly import Lexer, Parser
from sly.lex import Token
from sly.yacc import YaccProduction


class RegexLexer(Lexer):
    METACHARACTER = r"[\*,\*\?,\+,\+\?,\,\^]"

    @_(r'[0-9]+')
    def INTEGER(self, t: Token):
        t.value = int(t.value)
        return t

    # https://stackoverflow.com/questions/49100678/regex-matching-unicode-variable-names for explanations
    @_(r'[^\W0-9]\w*')
    def PROPERTY(self, t: Token):
        pass  # TODO


class RegexParser(Parser):

    # TODO: review using the "standard" BNF instead of the perl grammar

    # list of terms
    @_('term { "|" term }')
    def expression(self, p: YaccProduction):
        return [p[0]] + p[1]

    @_('factor {  factor }')
    def term(self, p: YaccProduction):
        pass

    @_('atom [ METACHARACTER ]')
    def factor(self, p: YaccProduction):
        pass

    @_('expression')
    def atom(self: YaccProduction):
        pass

    @_('PROPERTY')
    def atom(self: YaccProduction):
        pass

    @_('"[" property_set "]"')
    def atom(self: YaccProduction):
        pass

    # min
    @_('"{" INTEGER [ "," ] "}"')
    def atom(self: YaccProduction):
        pass

    # min, max
    @_('"{" INTEGER "," INTEGER "}"')
    def atom(self: YaccProduction):
        pass
