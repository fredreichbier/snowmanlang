import re

INDENTATION_SPACES = 4
INDENTATION_RE = re.compile('^( *)')

class IndentationError(Exception):
    pass

def preprocess(code):
    new_lines = []
    indentation_level = 0
    for lineno, line in enumerate(code.splitlines(), 1):
        number_of_spaces = len(INDENTATION_RE.search(line).group(1))
        if number_of_spaces % INDENTATION_SPACES:
            raise IndentationError('Invalid indentation (%d) in line %d' % (number_of_spaces, lineno))
        new_level = number_of_spaces / INDENTATION_SPACES
        if new_level > indentation_level:
            new_lines[-1] += ' {'
            new_lines.append(line)
        elif new_level < indentation_level:
            new_lines.append('}')
            new_lines.append(line)
        else:
            new_lines.append(line)
        indentation_level = new_level
    return '\n'.join(new_lines)

