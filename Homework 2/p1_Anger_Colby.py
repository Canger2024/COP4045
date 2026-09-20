import ast
import io
import tokenize


def line_number(input_filename: str, output_filename: str) -> None:
    """Write a copy of a text file with each line prefixed by its line number."""
    try:
        with open(input_filename, "r", encoding="utf-8") as infile:
            with open(output_filename, "w", encoding="utf-8") as outfile:
                for number, line in enumerate(infile, start=1):
                    outfile.write(f"{number}. {line}")
    except Exception as error:
        print(f"Error processing the file: {error}")
        raise


def remove_comments(code: str) -> str:
    """Return Python code with comment tokens removed."""
    tokens = tokenize.generate_tokens(io.StringIO(code).readline)
    kept_tokens = [
        token for token in tokens
        if token.type != tokenize.COMMENT
    ]
    return tokenize.untokenize(kept_tokens)


def parse_functions(filename: str) -> tuple:
    """Parse a Python file and return information about its functions."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            source = file.read()

        tree = ast.parse(source)
        lines = source.splitlines()
        result = []

        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                arguments = ast.unparse(node.args)

                code = "\n".join(
                    lines[node.lineno - 1:node.end_lineno]
                )

                code = remove_comments(code)

                code = "\n".join(
                    line.rstrip()
                    for line in code.splitlines()
                    if line.strip()
                ) + "\n"

                result.append(
                    (node.lineno, node.name, arguments, code)
                )

        result.sort(key=lambda item: item[1])
        return tuple(result)

    except Exception as error:
        print(f"Error parsing the Python file: {error}")
        raise


def main() -> None:
    """Test line_number and parse_functions using this source file."""
    input_filename = __file__
    output_filename = __file__ + ".txt"

    line_number(input_filename, output_filename)

    print("Numbered file created:")
    print(output_filename)

    print("\nParsed functions:")

    functions = parse_functions(input_filename)

    for function in functions:
        print(function)


if __name__ == "__main__":
    main()
