import os
import sys

def run_tests():
    import subprocess
    for test_file in os.listdir('tests'):
        if test_file.startswith('test_'):
            return_code = subprocess.Popen([
                'python', os.path.join('tests', test_file)
            ]).wait()
            if return_code:
                return return_code

def parse_code(code):
    import parser
    if not hasattr(parse_code, '_parser'):
        parse_code._parser = parser.Parser(modules=[parser])
    return parser.parse(code, parse_code._parser)

def translate_code(*files):
    import nodes
    from backends.c import CGeneratorBackend
    backend = CGeneratorBackend()
    backend._Statement = nodes.Statement # mmmhh, lecker

    if files:
        for source_file in files:
            result_file_name = os.path.splitext(source_file)[0] + backend.fileext
            with open(source_file) as source:
                ast = parse_code(source.read())
            result_buffer = backend.translate_ast(ast)
            with open(result_file_name, 'w') as result:
                result.write(result_buffer)
    else:
        # read input from stdin
        print backend.translate(parse_code(sys.stdin.read()))


if __name__ == '__main__':
    def usage(exc):
        print >> sys.stderr, 'USAGE: %s (--test | --translate files*)' % exc
    args = sys.argv[:]
    this_file = args.pop(0)
    if not args:
        exit(usage(this_file))

    if args[0].startswith('--'):
        cmd = args.pop(0)[2:]
    else:
        cmd = 'translate'

    exit(
        {'translate' : translate_code, 'test' : run_tests}[cmd](*args)
    )
