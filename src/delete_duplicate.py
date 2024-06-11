import os
dir1 = "/Users/abdulvahab.kharadi/"
dir2 = "/Users/abdulvahab.kharadi/transterm/"
dir3 = "/Users/abdulvahab.kharadi/2ndscore/"
files_1 = [file for file in os.listdir(dir1)]
#files_2 = [file for file in os.listdir(dir2)]
files_3 = [file for file in os.listdir(dir3)]
for file1 in files_1:
    for file3 in files_3:
        if file1 == file3:
            print(file1)
            #os.system("rm -r {}/{}".format(dir1, file1))