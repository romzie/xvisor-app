import sys
from PIL import Image

if len(sys.argv) < 2:
    print("arguments needed: <image_path>")
    exit(0)

img_path = sys.argv[1]

img = Image.open(img_path, 'r')
pixs = list(img.getdata())
size = len(pixs)

width, height = img.size

with open('pixels.h', 'w') as f:

    f.write('#ifndef _IMG_H_\n#define _IMG_H_')
    f.write('\n\n')
    f.write('#define widthImage {}\n'.format(width))
    f.write('#define heightImage {}\n'.format(height))
    f.write('\n')
    f.write('int pixels[{}][3] = \n'.format(size))
    f.write('{')

    for i in range(size):
        if i % 5 == 0:
            f.write('\n\t')

        f.write('{')
        f.write('{}, {}, {}'.format(str(pixs[i][0]), str(pixs[i][1]), str(pixs[i][2])))
        f.write('}')

        if i == size - 1:
            f.write('\n};\n')
            f.write('\n#endif')
        else:
            f.write(', ')
