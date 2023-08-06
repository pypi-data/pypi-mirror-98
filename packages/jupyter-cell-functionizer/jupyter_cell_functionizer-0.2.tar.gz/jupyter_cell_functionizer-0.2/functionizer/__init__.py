from __future__ import print_function

import ast

from IPython.core.magic import Magics, magics_class, cell_magic
from IPython.core import magic_arguments
import re

@magics_class
class FunctionizerMagics(Magics):

    @magic_arguments.magic_arguments()
    @magic_arguments.argument("--as_dict", action="store_true", default=False, help="return as a dictionary")
    @magic_arguments.argument("-a", "--args", type=str, nargs="+", help="arguments")
    @magic_arguments.argument("-r", "--ret", type=str, nargs="+", help="return values")
    @magic_arguments.argument("-d", "--disable", action="store_true", default=False, help="disable")
    @magic_arguments.argument("--skip", action="store_true", default=False, help="only define function, skip execution")
    @magic_arguments.argument("--skip_last", action="store_true", default=False, help="drop last line")
    @magic_arguments.argument("--return_last", action="store_true", default=False, help="return last line. will override -r")
    @magic_arguments.argument("fn", type=str, help="function name")
    @cell_magic
    def functionize(self, line, cell):
        args = magic_arguments.parse_argstring(self.functionize, line)
        fn = args.fn
        func_args = args.args or []
        ret = args.ret or []
        skip = args.skip
        skip_last = args.skip_last
        return_last = args.return_last
        as_dict = args.as_dict
        shell = self.shell

        if args.disable:
            shell.run_cell(cell)


        arg_sig = ",".join(func_args)


        lines = cell.splitlines()

        # purge empty lines
        while True:
            last_line = lines[-1]
            if re.match(r"\S+", last_line) or not lines:
                # is not empty
                break
            lines.pop(-1)

        if skip_last:
            lines.pop(-1)

        if not lines:
            lines.append("pass")
        else:
            if return_last:
                last_expr = lines.pop(-1)
                ret_expr = f"return {last_expr}"
            else:
                if as_dict:
                    ret_expr = f'return dict({",".join([f"{r}={r}" for r in ret])})'
                else:
                    ret_expr = f'return {",".join(ret)}'
            lines.append(ret_expr)

        indent_cell = "\n".join(["    " + l for l in lines])

        function_def = (
            f'def {fn}({arg_sig}):\n' 
            f'{indent_cell}\n'
        )

        combined = function_def if skip else function_def + cell
        shell.run_cell(combined)


def load_ipython_extension(ipython):
    ipython.register_magics(FunctionizerMagics)
