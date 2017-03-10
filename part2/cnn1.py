import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
import matplotlib.pylab as plt
from utils import generate_labelled_patches, load_labelled_patches, load_class_names
from keras import backend as K

# define the patch size as a variable so its easier to change later. For now,
# we'll set it to 28, just like the mnist images
patch_size = 28

# load data
train_data = generate_labelled_patches(["SU4010"], patch_size, shuffle=True)
valid_data = load_labelled_patches(["SU4011"], patch_size, limit=1000, shuffle=True)

# load the class names
clznames = load_class_names()
num_classes = len(clznames)

def larger_model(input_shape, num_classes):
	# create model
	model = Sequential()
	model.add(Convolution2D(30, 5, 5, border_mode='valid', input_shape=input_shape, activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Convolution2D(15, 3, 3, activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.2))
	model.add(Flatten())
	model.add(Dense(128, activation='relu'))
	model.add(Dense(50, activation='relu'))
	model.add(Dense(num_classes, activation='softmax'))
	
	return model

# build the model
model = larger_model(valid_data[0][0].shape, num_classes)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit_generator(train_data, samples_per_epoch=10016, nb_epoch=10, validation_data=valid_data, verbose=1)

# load 4 randomly selected patches and their labels
(X_test, y_test_true) = load_labelled_patches(["SU4012"], patch_size, limit=4, shuffle=True)
y_test = model.predict_classes(X_test)

#if we're using the theano backend, we need to change indexing order for matplotlib to interpret the patches:
if K.image_dim_ordering() == 'th':
	X_test = X_test.transpose(0, 3, 1, 2)

# plot 4 images
plt.subplot(221).set_title(clznames[y_test[0].argmax()])
plt.imshow(X_test[0])
plt.subplot(222).set_title(clznames[y_test[1].argmax()])
plt.imshow(X_test[1])
plt.subplot(223).set_title(clznames[y_test[2].argmax()])
plt.imshow(X_test[2])
plt.subplot(224).set_title(clznames[y_test[3].argmax()])
plt.imshow(X_test[3])

# show the plot
plt.show()