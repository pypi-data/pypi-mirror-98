try:
    from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic, line_cell_magic)
    from IPython.core.page import page
    from scalene import scalene_profiler
    from scalene.scalene_arguments import ScaleneArguments
    from typing import Any
    import os
    import sys
    import tempfile
    import textwrap
    
    @magics_class
    class ScaleneMagics(Magics): # type: ignore

        def run_code(self, args: ScaleneArguments, code: str) -> None:
            # Create a temporary file to hold the supplied code.
            tmpfile = tempfile.NamedTemporaryFile(mode="w+", delete=False, prefix="scalene_profile_", suffix=".py")
            tmpfile.write(code)
            tmpfile.close()
            args.cpu_only = True # full Scalene is not yet working, force to use CPU-only mode
            scalene_profiler.Scalene.run_profiler(args, [tmpfile.name])
           
        @line_cell_magic
        def scalene(self, line : str, cell : str = "") -> None:
            """See https://github.com/plasma-umass/scalene for usage info."""
            if line:
                sys.argv = ["scalene"]
                sys.argv.extend(line.split(" "))
                (args, left) = scalene_profiler.Scalene.parse_args()
            else:
                args = ScaleneArguments()
            if cell:
                self.run_code(args, cell) # type: ignore
                
        @line_magic
        def scrun(self, line: str = "") -> None:
            """See https://github.com/plasma-umass/scalene for usage info."""
            from scalene import scalene_profiler
            if line:
                sys.argv = ["scalene"]
                sys.argv.extend(line.split(" "))
                (args, left) = scalene_profiler.Scalene.parse_args()
                self.run_code(args, (" ").join(left)) # type: ignore

    def load_ipython_extension(ip: Any) -> None:
        ip.register_magics(ScaleneMagics)
        try:
            # For some reason, this isn't loading correctly on the web.
            with open("scalene-usage.txt", "r") as usage:
                str = usage.read()
            ScaleneMagics.scrun.__doc__ = str
            ScaleneMagics.scalene.__doc__ = str
        except Exception:
            pass
        import textwrap
        print("\n".join(textwrap.wrap("Scalene extension successfully loaded. Note: Scalene currently only supports CPU profiling inside Jupyter notebooks. For full Scalene profiling, use the command line version.")))
        
except:
    pass
