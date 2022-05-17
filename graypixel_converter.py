import cv2
import glob
import os

os.chdir(r'C:\Team SignBes\Dataset\traindataset\j')
print(os.getcwd())
for filename in glob.glob(r'C:\Team SignBes\Dataset\traindataset\j\*.jpeg'):
    print(filename)
    img=cv2.imread(filename) 
    #rl=cv2.resize(img, (500,500))
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    os.remove(filename)
    cv2.imwrite(f'{filename}.jpeg', gray_image)

for count, f in enumerate(os.listdir()):
    f_name, f_ext = os.path.splitext(f)
    f_name = "sign_j_" + str(count)
 
    new_name = f'{f_name}{f_ext}'
    os.rename(f, new_name)