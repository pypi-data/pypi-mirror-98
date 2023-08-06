from boringmd.invoke import invoke


def cli_entry() -> None:
    exit(invoke())


if __name__ == "__main__":
    cli_entry()
