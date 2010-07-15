Hello ☃!
========

The Snow Programming Language is a thin syntax layer on top of C
that produces beautiful C99 code.

Snow's syntax is inspired by Python. Thus, for blocks, it uses indentation
(4 spaces only) rather than braces.

Here comes the obligatory Hello Snowman in Snow::

   import stdio

   main as Function(argc as Int, argv as String*) -> Int:
       printf("Hello, ☃!")
       return 0
