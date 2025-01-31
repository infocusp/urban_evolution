import rasterio
import cv2
import numpy as np 
import matplotlib.pyplot as plt
import imageio.v3 as iio
import os
def plot(ground, prediction,year):

    ground= cv2.cvtColor(ground, cv2.COLOR_BGR2RGB)
    # print((ground.shape[0]/2, ground.shape[1]/2))
    print((ground.shape[0]/2, ground.shape[1]/2))
    # ground=cv2.putText(ground,'GROUND', (int(5), int(ground.shape[1]/2)),cv2.FONT_HERSHEY_COMPLEX,1,color=(255,0,0))
    prediction = cv2.cvtColor(prediction, cv2.COLOR_BGR2RGB)
   
    print(prediction.shape)
    print(ground.shape)
    x_dim=min(prediction.shape[0],ground.shape[0])
    y_dim=min(prediction.shape[1],ground.shape[1])
    ground =ground[:740,:681,:]
    prediction=prediction[:740,:681,:]
    ground=np.pad(ground,((2,2),(2,2),(0,0)), mode='constant', constant_values=(0, 0))
    ground=cv2.putText(ground,'GROUND TRUTH', (int(ground.shape[0]/2), int(671)),cv2.FONT_HERSHEY_COMPLEX,1,color=(0,0,0))
    ground=cv2.putText(ground,year, (int(30), int(30)),cv2.FONT_HERSHEY_COMPLEX,1,color=(0,0,0))
    prediction=np.pad(prediction,((2,2),(2,2),(0,0)), mode='constant', constant_values=(0, 0))
    prediction=cv2.putText(prediction,'PREDICTION', (int(prediction.shape[0]/2), int(675)),cv2.FONT_HERSHEY_COMPLEX,1,color=(0,0,0))

    full_2015=np.hstack((ground,prediction))
    return full_2015


fol_name="/home/nikki/Pictures/Screenshots/"

ground_2015=cv2.imread(os.path.join(fol_name, "ground_2015.png"))
prediction_2015=cv2.imread(os.path.join(fol_name,"prediction_2015.png"))
ground_2016=cv2.imread(os.path.join(fol_name, "ground_2016.png"))
prediction_2016=cv2.imread(os.path.join(fol_name,"prediction_2016.png"))
ground_2017=cv2.imread(os.path.join(fol_name, "ground_2017.png"))
prediction_2017=cv2.imread(os.path.join(fol_name,"prediction_2017.png"))
ground_2018=cv2.imread(os.path.join(fol_name, "ground_2018.png"))
prediction_2018=cv2.imread(os.path.join(fol_name,"prediction_2018.png"))
ground_2019=cv2.imread(os.path.join(fol_name, "ground_2019.png"))
prediction_2019=cv2.imread(os.path.join(fol_name,"prediction_2019.png"))
ground_2020=cv2.imread(os.path.join(fol_name,"ground_2020.png"))
prediction_2020=cv2.imread(os.path.join(fol_name,"prediction_2020.png"))
year='2015'
full_2015=plot(ground_2015, prediction_2015,year)
year='2016'
full_2016=plot(ground_2016, prediction_2016,year)
year='2017'
full_2017=plot(ground_2017, prediction_2017,year)
year='2018'
full_2018=plot(ground_2018, prediction_2018,year)
year='2019'
full_2019=plot(ground_2019, prediction_2019,year)
year='2020'
full_2020=plot(ground_2020, prediction_2020,year)



plt.imsave('full_2015_image.png' ,full_2015)
plt.imsave('full_2016_image.png' ,full_2016)
plt.imsave('full_2017_image.png' ,full_2017)
plt.imsave('full_2018_image.png' ,full_2018)
plt.imsave('full_2019_image.png' ,full_2019)
plt.imsave('full_2020_image.png' ,full_2020)


filenames = ['full_2015_image.png', 'full_2016_image.png','full_2017_image.png','full_2018_image.png','full_2019_image.png','full_2020_image.png']
images = [ ]
for filename in filenames:
  images.append(iio.imread(filename))
iio.imwrite('all_images.gif', images, duration = 1500, loop = 0)