from utils import ordereddict

class Backend(object):
    def translate_ast(self, ast):
        return self.visit_Ast(ast)

    def translate_child(self, node, child_name):
        child = node.children[child_name]
        if isinstance(child, list):
            return (self.visit_node(item) for item in child)
        else:
            return self.visit_node(child)

    def visit_node(self, node):
        return self._dispatch(node)(node)

    def _dispatch(self, node):
        type_name = type(node).__name__
        try:
            return getattr(self, 'visit_%s' % type_name)
        except AttributeError:
            raise NotImplementedError(
                "'visit_%s' is not implemented (tried to visit %s)" 
                % (type_name, node)
            )

    def visit_Ast(self, ast):
        for node in ast:
            yield self.visit_node(node)
