## Move journal.sh logic into here
import subprocess
import sys


def main() -> int:
    print(sys.argv)
    print(f"Opening vi")
    subprocess.run(["vi"])
    print(f"Closed vi")
    return 0


if __name__ == "__main__":
    exit(main())
