class ParsingError(Exception):
    def __init__(self, message, s, position):
        self.message = message
        self.s = s
        self.position = position

        assert position <= s
        super(ParsingError, self).__init__('%s (position %d)' % (message, position))


class LintParsingError(Exception):
    def __init__(self, message, s, position):
        self.message = message
        self.s = s
        self.position = position

        assert position <= s
        super(LintParsingError, self).__init__('%s (position %d)' % (message, position))


class SubCommandError(Exception):
    def __init__(self, message, s, position):
        self.message = message
        self.s = s
        self.position = position

        assert position <= s
        super(SubCommandError, self).__init__('%s (position %d)' % (message, position))


class FlagError(Exception):
    def __init__(self, message, s, position):
        self.message = message
        self.s = s
        self.position = position

        assert position <= s
        super(FlagError, self).__init__('%s (position %d)' % (message, position))
