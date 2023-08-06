from boringmd.invoke import invoke


def cli_entry() -> int:
    return invoke()


if __name__ == "__main__":
    cli_entry()
