from functions.write_file_content import write_file

print("Write lorem ipsum 1")
write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")

print("Write lorem ipsum 2")
write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")

print("Not allowed")
write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
