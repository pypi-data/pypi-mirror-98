"""Convert text to snake case"""
import re
import sys


def main() -> None:
    """Snekify CLI interface"""
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
    else:
        text = sys.stdin.read()

    snekified_lines = [snekify(line) for line in text.splitlines()]
    print('\n'.join(snekified_lines))


def snekify(line: str) -> str:
    """Snekify text"""
    words = re.findall(r'[A-Za-z0-9]+', line)
    return '_'.join(word.lower() for word in words)
