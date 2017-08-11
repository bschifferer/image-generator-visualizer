from PIL import Image
import keras.preprocessing.image as image
import glob
import numpy as np
import matplotlib.pyplot as plt
import time

def init_standardParameter():
    parameter_space = {}
    parameter_space['featurewise_center'] = False
    parameter_space['samplewise_center'] = False
    parameter_space['featurewise_std_normalization'] = False
    parameter_space['samplewise_std_normalization'] = False
    parameter_space['zca_whitening'] = False
    parameter_space['zca_epsilon'] = 1e-6
    parameter_space['rotation_range'] = 0.
    parameter_space['width_shift_range'] = 0.
    parameter_space['height_shift_range'] = 0.
    parameter_space['shear_range'] = 0.
    parameter_space['zoom_range'] = 0.
    parameter_space['channel_shift_range'] = 0.
    parameter_space['fill_mode'] = 'nearest'
    parameter_space['cval'] = 0.
    parameter_space['horizontal_flip'] = False
    parameter_space['vertical_flip'] = False
    return parameter_space

def getImageGenerateor(parameter_final):
    return image.ImageDataGenerator(featurewise_center=parameter_final['featurewise_center'], samplewise_center=parameter_final['samplewise_center'], featurewise_std_normalization=parameter_final['featurewise_std_normalization'], samplewise_std_normalization=parameter_final['samplewise_std_normalization'], zca_whitening=parameter_final['zca_whitening'], rotation_range=parameter_final['rotation_range'], width_shift_range=parameter_final['width_shift_range'], height_shift_range=parameter_final['height_shift_range'], shear_range=parameter_final['shear_range'], zoom_range=parameter_final['zoom_range'], channel_shift_range=parameter_final['channel_shift_range'], fill_mode=parameter_final['fill_mode'], cval=parameter_final['cval'], horizontal_flip=parameter_final['horizontal_flip'], vertical_flip=parameter_final['vertical_flip'])

def getPlot(key, parameter_values, count_imgs, subplot_size):
    fig, ax = plt.subplots((len(parameter_values)+1), count_imgs, figsize=subplot_size)
    plt.suptitle(key, size=12)
    plt.setp(ax, xticks=[], yticks=[])
    return fig, ax

def getDataGenerator(parameter_final, imgs, ylabels):
    datagen = getImageGenerateor(parameter_final)
    datagen.fit(imgs)
    datagen_flow = datagen.flow(imgs, ylabels, batch_size=len(imgs))
    return datagen_flow

def addSubplot(ylabel_gen, col_counter, row_counter, img, ytitle, ax):
    x = np.where(ylabel_gen==col_counter)
    ax[row_counter, col_counter].imshow(img[x[0][0]]*255)
    if col_counter == 0:
        ax[row_counter, col_counter].set_ylabel(ytitle, rotation=90, size=12)

def visualization(imgs, parameter_space, path, subplot_size=(10,10)):
    parameter_keys = parameter_space.keys()
    count_imgs = len(imgs)
    ylabels = np.arange(count_imgs)
    for key in parameter_keys:
        parameter_values = parameter_space[key]
        fig, ax = getPlot(key, parameter_values, count_imgs, subplot_size)
        row_counter = 0
        ytitle = 'original'
        for ind_value in np.arange((len(parameter_values)+1)):
            parameter_final = init_standardParameter()
            if row_counter>0:
                parameter_final[key] = parameter_values[ind_value-1]
                ytitle = parameter_values[ind_value-1]
            if key == 'fill_mode':
                parameter_final['height_shift_range'] = 0.5
            if key == 'cval':
                parameter_final['height_shift_range'] = 0.5
                parameter_final['fill_mode'] = 'constant'
            datagen_flow = getDataGenerator(parameter_final, imgs, ylabels)
            col_counter = 0
            for img_gen in datagen_flow:
                img = img_gen[0]
                ylabel_gen = img_gen[1]
                for col_counter in ylabels:
                    addSubplot(ylabel_gen, col_counter, row_counter, img, ytitle, ax)
                break
            row_counter = row_counter + 1
        time.sleep(0.2)
        fig.savefig(path + key + '.png')
        #plt.close(fig)

