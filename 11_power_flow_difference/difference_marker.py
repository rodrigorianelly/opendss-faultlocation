import cv2
import matplotlib.pyplot as plt
import numpy as np

def compare_images(path1, path2):
    # Read image in BGR format
    img1 = cv2.imread(path1,cv2.IMREAD_ANYCOLOR)
    #img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)

    img2 = cv2.imread(path2,cv2.IMREAD_ANYCOLOR)

    for k in [0,1,2]:
        for i in range(np.shape(img1)[0]):
            for j in range(np.shape(img1)[1]):
                if img1[i][j][k] != img2[i][j][k]:
                    if k == 0:
                        img1[i][j][k] = 235
                    if k == 1:
                        img1[i][j][k] = 183
                    if k == 2:
                        img1[i][j][k] = 0

    cv2.imshow("Window",img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":

    print(
    """
This code compares the power flow between
ckt24 without PV and ckt 24 with 339 small PV systems
in power scales of 0.3 MW, 3 MW and 13 MW. It is necessary
to use many scales to see in totality the power flow differences
    """
    )

    print("(press a keyboard key to close the images)")

    # 300 kW scale
    compare_images("diff_manyPV_300//power_noPV.png",
    "diff_manyPV_300//power_PV.png")

    # 3 MW scale
    compare_images("diff_manyPV_3k//power_noPV.png",
    "diff_manyPV_3k//power_PV.png")

    # 13 MW scale
    compare_images("diff_manyPV_13k//power_noPV.png",
    "diff_manyPV_13k//power_PV.png")
