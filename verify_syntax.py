import os
import py_compile
import re
import sys
import tempfile
import textwrap


def extract_python_blocks(md_file):
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Simple regex to extract python code blocks
    blocks = re.findall(r"```python\n([\s\S]*?)```", content)
    return blocks


def verify_syntax(code_block):
    code_block = textwrap.dedent(code_block)
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tf:
        tf.write(code_block.encode("utf-8"))
        temp_name = tf.name

    try:
        py_compile.compile(temp_name, doraise=True)
        return True, None
    except py_compile.PyCompileError as e:
        return False, str(e)
    finally:
        if os.path.exists(temp_name):
            os.remove(temp_name)


def main():
    solutions_dir = "solutions"
    errors = []
    total_blocks = 0

    for root, dirs, files in os.walk(solutions_dir):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                blocks = extract_python_blocks(full_path)
                for i, block in enumerate(blocks):
                    total_blocks += 1
                    is_valid, error = verify_syntax(block)
                    if not is_valid:
                        errors.append(f"Error in {full_path} (block {i+1}):\n{error}")

    print(f"Total Python blocks found: {total_blocks}")
    if errors:
        print(f"Found {len(errors)} syntax errors:")
        for err in errors:
            print("-" * 20)
            print(err)
        sys.exit(1)
    else:
        print("All Python blocks have valid syntax.")


if __name__ == "__main__":
    main()
