import re

with open('/home/lucky/stuff/notes_fang/09-dynamic-programming/09-edit-distance.md', 'r') as f:
    content = f.read()

import ast
python_blocks = re.findall(r'```python\n(.*?)```', content, re.DOTALL)
for i, block in enumerate(python_blocks):
    try:
        ast.parse(block)
        print(f"Block {i+1} OK")
    except SyntaxError as e:
        print(f"Block {i+1} SyntaxError: {e}")
        
