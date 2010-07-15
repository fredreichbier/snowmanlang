import os
import sys

TESTS_DIR = os.path.join(os.path.dirname(__file__), 'tests')

def run_tests():
    import subprocess
    for test_file in os.listdir(TESTS_DIR):
        if test_file.startswith('test_'):
            return_code = subprocess.Popen([
                'python', os.path.join(TESTS_DIR, test_file)
            ]).wait()
            #if return_code:
            #    return return_code

def parse_code(code):
    from snowman import parser
    if not hasattr(parse_code, '_parser'):
        parse_code._parser = parser.Parser(modules=[parser], file_prefix='.d_parser_mach_gen')
    return parser.parse(code, parse_code._parser)

def translate_code(*files):
    import nodes
    from backends.c import CGeneratorBackend as backend

    if files:
        for source_file in files:
            result_file_name = os.path.splitext(source_file)[0] + backend.fileext
            with open(source_file) as source:
                ast = parse_code(source.read())
            result_buffer = backend(ast).translate()
            with open(result_file_name, 'w') as result:
                result.write(result_buffer)
    else:
        # read input from stdin
        print backend.translate_ast(parse_code(sys.stdin.read()))


if __name__ == '__main__':
    args = sys.argv[:]
    this_file = args.pop(0)
    cmd = 'translate'
    if not args:
        files = ()
    elif args[0].startswith('--'):
        cmd = args.pop(0)[2:]
    exit(
        {'translate' : translate_code, 'test' : run_tests}[cmd](*args)
    )
