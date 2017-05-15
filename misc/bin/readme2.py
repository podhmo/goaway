import subprocess
from indent import block


def main():
    print("")
    print("example2")
    print("----------------------------------------")
    print("")

    print("main.py")
    with block("python"):
        with open("examples/junks/struct.py") as rf:
            for line in rf:
                print(line.rstrip())

    with block("bash"):
        cmd = "python examples/junks/struct.py > examples/junks/struct.go"
        p = subprocess.run(
            cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        for line in p.stdout.decode("utf-8").split("\n"):
            print(line)

    print("struct.go")
    with block("struct.go"):
        with open("examples/junks/struct.go") as rf:
            for line in rf:
                print(line.rstrip())


if __name__ == "__main__":
    main()
