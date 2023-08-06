## Image Data Importer For Deep Learning

A Python package which will help you to import image data for your deep learning project. The function inside the package is called "img_data_importer" which accepts only one parameter i.e path of main folder (main folder is the one inside which all different categories folders are present),and during execution it will ask you to pick some options,choose them according to your data set after generating the data, the output will be returned in tuple (X_train,y_train) in which X_train has categories image data and y_train has labels, How to execute is shown below

## Execution
X,y = img_data_importer(path of main folder), 
X holds the image data and y holds the labels

## typical options shown below

Do you want to convert your image data to grey scale? y/n: choose your option

Do you want to resize your data? y/n [default:100x100]: choose your option

Generating & Shuffling the Data...

Do you want to normalize your data? y/n [recommended]: choose your option

Do you want to save your data? y/n [will be saved using pickle]: choose your option