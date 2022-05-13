## rby/generate_TM_indices.py

TM00_index = 0xC8
out_text = ''

for current_TM in range(1, 51):
    # set current index, begins at 0xC9 = 0xC8 + 1
    current_index = TM00_index + current_TM
    current_TM_name = 'TM' + str(current_TM).zfill(2)
    output_string = f"\n    0x{current_index:X}: '{current_TM_name}',"
    out_text += output_string

with open('TM_out.txt', 'w') as file:
    file.write(out_text)
