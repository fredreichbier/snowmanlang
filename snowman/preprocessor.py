INDENTATION_SPACES = 4

class IndentationError(Exception):
    pass

def _preprocess(code):
    indentation_level = 0
    open_parenthesis = 0
    open_double_quote = False

    for lineno, line in enumerate(code.splitlines(), 1):
        if not line:
            continue

        if line.count('"') % 2:
            open_double_quote = not open_double_quote
        open_parenthesis += line.count('(')
        open_parenthesis -= line.count(')')

        if open_parenthesis or open_double_quote:
            # This line is within an expression enclosed
            # by parenthesis or part of a string started
            # on an earlier line.
            # No preprocessing on this line.
            yield line
            continue

        number_of_spaces = 0
        for char in line:
            if char != ' ':
                break
            number_of_spaces += 1
        else:
            # only whitespace on this line. ignore it.
            continue

        new_level = number_of_spaces / INDENTATION_SPACES
        if number_of_spaces % INDENTATION_SPACES:
            raise IndentationError('Invalid indentation (%d) in line %d' % (number_of_spaces, lineno))

        if new_level > indentation_level:
            yield '{'
        elif new_level < indentation_level:
            for i in xrange(indentation_level - new_level):
                yield '}'
        yield line
        yield ';'

        indentation_level = new_level

    for i in xrange(indentation_level):
        yield '}'

def pairwise(generator):
    last = None
    for item in generator:
        if last is not None:
            yield last, item
        last = item
    yield last, None

def _preprocess2(generator):
    for line1, line2 in pairwise(generator):
        if line2 != '{':
            yield line1

def preprocess(code):
    generator = _preprocess(code)
    code = '\n'.join(_preprocess2(generator))
    #print code
    return code
