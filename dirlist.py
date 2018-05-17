import os

for dirname, dirnames, filenames in os.walk('dataset/LLDOS-1'):
    # print path to all filenames.
    for filename in filenames:
        print(os.path.join(dirname, filename))

    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk() from recursing into there.
    if '.git' in dirnames:
        # don't go into any .git directories.
        dirnames.remove('.git')

# filename = 'dmzphase1.csv'
# filename = filename.split('.')[0]
# print filename