import os

# for dirname, dirnames, filenames in os.walk('/home/rafiar/Documents/Kuliah/TA/TA-Program'):
#     # print path to all subdirectories first.
#     for subdirname in dirnames:
#         print(os.path.join(dirname, subdirname))

#     # print path to all filenames.
#     for filename in filenames:
#         print(os.path.join(dirname, filename))

#     # Advanced usage:
#     # editing the 'dirnames' list will stop os.walk() from recursing into there.
#     if '.git' in dirnames:
#         # don't go into any .git directories.
#         dirnames.remove('.git')

os.chdir('dataset')
cwd = os.getcwd()

print cwd
for name in os.listdir("dataset"):
    print name 