## rby/generate_move_indices.py
import re

in_lines = []

with open('rby_move_indices.txt', 'r') as in_file:
    in_text = in_file.read()
    in_lines = in_text.split('const')

my_pattern = re.compile(r"(\w+)\s+; ([0-9a-f]{2})")
out_lines = []

for current_line in in_lines:
    if not current_line:
        continue
    my_match = re.search(my_pattern, current_line)
    if not my_match:
        print(f'error reading following line: "{current_line}".')
        print(current_line)
    if my_match:
        (move_name_RAW, move_index_RAW) = my_match.group(1, 2)
        move_name = re.sub(r'_', r' ', move_name_RAW).title()
        move_index = f'0x{int(move_index_RAW, 16):X}'
        out_lines.append(f"    {move_index}: '{move_name}',")

with open('out_move_indices.txt', 'w') as out_file:
    out_file.write("\n".join(out_lines))
