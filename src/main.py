import sys
from src.config import ConfigManager
from src.models import Binary
from src.executor import Executor


class BinmanCLI:
    def __init__(self):
        self.config_manager = ConfigManager()

    def run_config(self) -> None:
        print("--- Binman Configuration ---")
        binaries = self.config_manager.load_binaries()

        while True:
            route = input("Specify route: ").strip()
            codename = input("Codename: ").strip()

            if route and codename:
                # Creates object using custom Binary class
                binaries[codename] = Binary(alias=codename, path=route)
            else:
                print("Route and codename/alias can not be empty.")
                continue

            while True:
                again = input("Want to add another binary [y/N]: ").strip().lower()

                if again == "":
                    again = "n"

                if again == "y" or again == "n":
                    break

                print(f"Unexpected argument ({again}). Please enter 'y' or 'n'.")

            if again == "n":
                break

        self.config_manager.save_binaries(binaries)
        print("\nConfiguration saved!")
        for name, binary in binaries.items():
            print(f"{name} ({binary.path}) is ready to use! (binman -b {name} args)")

    def run_execution(self, args: list) -> None:
        if "-b" not in args:
            print("Error: Missing binary alias. Use: binman -b <codename> [args]")
            print("Or configure new binaries using: binman config")
            sys.exit(1)

        try:
            b_index = args.index("-b")
            codename = args[b_index + 1]
        except IndexError:
            print("Error: You must specify a codename after -b")
            sys.exit(1)

        binaries = self.config_manager.load_binaries()
        if codename not in binaries:
            print(f"Error: Codename '{codename}' not found. Run 'binman config' first.")
            sys.exit(1)

        target_binary = binaries[codename]

        bin_args = args[:b_index] + args[b_index + 2:]

        executor = Executor(binary=target_binary, args=bin_args)
        executor.execute()


def main():
    cli = BinmanCLI()
    args = sys.argv[1:]

    if len(args) > 0 and args[0] == "config":
        cli.run_config()
    else:
        cli.run_execution(args)


if __name__ == "__main__":
    main()