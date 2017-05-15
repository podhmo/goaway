import subprocess
from indent import block


def main():
    print("")
    print("example")
    print("----------------------------------------")
    print("")

    print("main.py")
    with block("python"):
        with open("examples/readme/main.py") as rf:
            for line in rf:
                print(line.rstrip())

    with block("bash"):
        cmd = "make -C examples/readme"
        p = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in p.stdout.decode("utf-8").split("\n"):
            print(line)

    print("main.go")
    with block("main.go"):
        with open("examples/readme/main.go") as rf:
            for line in rf:
                print(line.rstrip())


if __name__ == "__main__":
    main()
