data = "C:/Users/princ/AppData/Local/Temp/7e7b0340-f50b-4b75-8e93-9cc9861fefc7.dd:   2.1%    10.0 MB    00:00 ETA"
data_array = data.split()
print(f"Datatype: {type(data_array)}, Data array: {data_array}")
prg_str = data_array[1][:-1]
size_processed = data_array[2]
unit_processed = data_array[3]
print(f"Percentage: {prg_str}, Size: {size_processed}, {unit_processed}")


# Summary info
jpg_data = (
    'jpg with header "\xff\xd8\xff\xe0\x00\x10" and footer "\xff\xd9" --> 290 files'
)

png_data = 'png with header "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a" and footer "\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82" --> 3425 files'
