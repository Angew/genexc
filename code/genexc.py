import argparse
import sys

import pyperclip


class GenexC:
    def __init__(self, brackets=None):
        if brackets is None: brackets = ""
        len_b = len(brackets)
        if len_b % 2 != 0:
            raise ValueError("`brackets` must be of even length")
        if len_b:
            self.brackets = (brackets[:len_b//2], brackets[len_b//2:])
        else:
            self.brackets = None

    def run(self, text):
        text = "".join(filter(lambda x: not x.isspace(), text))
        if self.brackets:
            text = text.replace(self.brackets[0], "<")
            text = text.replace(self.brackets[1], ">")
        return text


def run(input, output, brackets=None):
    genexc = GenexC(brackets)
    output(genexc.run(input()))


def read_clipboard():
    return pyperclip.paste()

def read_stdin():
    raise NotImplementedError("Not implemented yet")

def write_clipboard(text):
    pyperclip.copy(text)

def write_stdout(text):
    print(text)


def main(args):
    parser = argparse.ArgumentParser(
        prog="genexc",
        description=
            "GENerator EXpression Compiler: tool to ease creation of "
            "CMake generator expressions (\"genexes\")",
    )
    parser.add_argument(
        "-C", "--clipboard",
        help="Take input from clipboard, store output in clipboard",
        action="store_true",
        dest="use_clipboard",
    )
    parser.add_argument(
        "-b", "--brackets",
        help='Translate the provided string (or "[]" if omitted) into < and >',
        nargs="?",
        default="", # when not present at all
        const="[]", # when used without argument
    )

    opt = parser.parse_args(args)
    run(
        brackets=opt.brackets,
        input=read_clipboard if opt.use_clipboard else read_stdin,
        output=write_clipboard if opt.use_clipboard else write_stdout,
    )


if __name__ == "__main__":
    main(sys.argv[1:])
