"""main entry for ekgen command-line interface"""


def main():
    from ekgen import E3SMKGen
    ret, _ = E3SMKGen().run_command()
    return ret


if __name__ == "__main__":
    main()
