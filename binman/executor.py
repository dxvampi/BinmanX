import os
import sys
from typing import List, Optional
from binman.models import Binary

class Executor:
    def __init__(self, binary: Binary, args: Optional[List[str]] = None):
        self.binary = binary
        # If no args are passed, empty list is returned
        self.args = args if args is not None else []

    def execute(self) -> None:
        """Replaces actual process with binary."""
        if not self.binary.exists():
            print(f"❌ Error: Binary for '{self.binary.alias}' does not exist in: {self.binary.path}")
            sys.exit(1)

        # os.execv requires: (bin_path, [process_name, arg1, arg2, ...])
        os.execv(self.binary.path, [self.binary.path] + self.args)