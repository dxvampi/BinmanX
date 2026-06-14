import sys
from binmanx.config import ConfigManager
from binmanx.models import Binary
from binmanx.executor import Executor


class BinmanxCLI:
    def __init__(self):
        self.config_manager = ConfigManager()

    def _show_aliases(self) -> list:
        aliases = self.config_manager.get_all_aliases()
        if not aliases:
            print("No alias is saved yet.")
            return []

        for indice, (alias, ruta) in enumerate(aliases):
            print(f"{indice}. {alias} ({ruta})")

        return aliases

    def run_list(self) -> None:
        self._show_aliases()

    def run_delete(self) -> None:
        while True:
            aliases = self._show_aliases()

            if not aliases:
                break

            try:
                selection = input("Select an option to delete: ").strip()
                if not selection:
                    print("Empty selection, try again")
                    continue

                index = int(selection)

                if 0 <= index < len(aliases):
                    alias_to_delete, path_to_delete = aliases[index]

                    self.config_manager.delete_alias_by_name(alias_to_delete)
                    print(f"Deleted {index} ({alias_to_delete} [{path_to_delete}]) successfully!")
                else:
                    print("Number out of range. Select a valid one.")
                    continue

            except ValueError:
                print("Please, introduce a valid number.")
                continue

            more = input("Want to delete more? [y/N] ").strip().lower()
            if more != 'y':
                break

    def run_config(self) -> None:
        print("--- Binmanx Configuration ---")
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
            print(f"{name} ({binary.path}) is ready to use! (binmanx -b {name} args)")

    def run_execution(self, args: list) -> None:
        if "-b" not in args:
            print("Error: Missing binary alias. Use: binmanx -b <codename> [args]")
            print("Or configure new binaries using: binmanx config")
            print("Show saved aliases using: binmanx list")
            print("Delete aliases using: binmanx delete")
            sys.exit(1)

        try:
            b_index = args.index("-b")
            codename = args[b_index + 1]
        except IndexError:
            print("Error: You must specify a codename after -b")
            sys.exit(1)

        binaries = self.config_manager.load_binaries()
        if codename not in binaries:
            print(f"Error: Codename '{codename}' not found. Run 'binmanx config' first.")
            sys.exit(1)

        target_binary = binaries[codename]

        bin_args = args[:b_index] + args[b_index + 2:]

        executor = Executor(binary=target_binary, args=bin_args)
        executor.execute()


def main():
    cli = BinmanxCLI()
    args = sys.argv[1:]

    if len(args) > 0:
        comando = args[0]
        if comando == "config":
            cli.run_config()
        elif comando == "list":
            cli.run_list()
        elif comando == "delete":
            cli.run_delete()
        else:
            cli.run_execution(args)
    else:
        cli.run_execution(args)


if __name__ == "__main__":
    main()