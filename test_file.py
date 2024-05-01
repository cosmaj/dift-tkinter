data = "C:/Users/princ/AppData/Local/Temp/7e7b0340-f50b-4b75-8e93-9cc9861fefc7.dd:   2.1%    10.0 MB    00:00 ETA"
data_array = data.split()
print(f"Datatype: {type(data_array)}, Data array: {data_array}")
prg_str = data_array[1][:-1]
size_processed = data_array[2]
unit_processed = data_array[3]
print(f"Percentage: {prg_str}, Size: {size_processed}, {unit_processed}")
