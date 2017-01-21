
from unittest import TestCase
import os

class TestLlvmCpy(TestCase):
    def _delete_temps(self):
        try:
            os.unlink(self.filename)
        except FileNotFoundError:
            pass

    def setUp(self):
        self.filename = self.__class__.__name__
        with open(self.filename, 'w') as f:
            f.write('''
define i32 @foo(i32 %x) {
    ret i32 1
}
''')

    def tearDown(self):
        self._delete_temps()

    def test_example(self):
        import sys
        from llvmcpy.llvm import create_memory_buffer_with_contents_of_file, get_global_context

        buf = create_memory_buffer_with_contents_of_file(self.filename)
        context = get_global_context()
        module = context.parse_ir(buf)
        assert module

        funcs = list(module.iter_functions())
        assert len(funcs) == 1

        for function in module.iter_functions():
            for bb in function.iter_basic_blocks():
                for instruction in bb.iter_instructions():
                    instruction.dump()
