import numpy as np
import os
import cv2
import pickle
import random

def img_data_importer(path):
    """
    Accepts only one parameter i.e path of main folder, after generating
    the data, the output will be returned in a tuple (X_train,y_train,mapping) which contains
    X_train(categories), y_train(labels) and mapping(its a dictionary which maps
    the categories and their index value), How to execute is shown below
    X,y,m = img_data_importer(path of main folder), X holds the image data,  
    y_train holds the index value of categories and mapping(Dictionary/Hash-Map) 
    holds the categories and their particular index value.
    """
    train_data = []
    X_train = []
    y_train = []
    categories = os.listdir(path)
    
    option1 = input("Do you want to convert your image data to grey scale? y/n: ")
    
    option2 = input("Do you want to resize your data? y/n [default:100x100]: ")
    if option2 == "y" or option2 == "Y" or option2 == "yes" or option2=="YES":
        img_size = int(input("enter the size: "))
    else:
        img_size = 100
        
    print("Generating, Shuffling & Mapping the Data...")    
    for category in categories:
        full_path = os.path.join(path,category)
        cat_index = categories.index(category)
        for image in os.listdir(full_path):
            try:
                if option1=="y" or option1=="Y" or option1=="yes" or option1=="YES":
                    image_arr = cv2.imread(os.path.join(full_path,image),
                                      cv2.IMREAD_GRAYSCALE)
                else:
                    image_arr = cv2.imread(os.path.join(full_path,image))
                
                resized_img_arr = cv2.resize(image_arr,(img_size,img_size))
                train_data.append([resized_img_arr,cat_index])
            except Exception as e:
                print(e)
    
    random.shuffle(train_data)
    for x,y in train_data:
        X_train.append(x)
        y_train.append(y)
    
    mapping = {category:categories.index(category) for category in categories }
    
    if option1=="y" or option1=="Y" or option1=="yes" or option1=="YES":
        X_train = np.array(X_train).reshape(-1,img_size,img_size,1)
    else:
        X_train = np.array(X_train).reshape(-1,img_size,img_size,3)
    
    option3 = input("Do you want to normalize your data? y/n [recommended]: ")
    if option3 == "y" or option3 == "Y" or option3 == "yes" or option3 =="YES":
        X_train = np.array(X_train)/255.0
        
    option4 = input("Do you want to save your data? y/n [will be saved using pickle]: ")
    if option4 == "y" or option4 == "Y" or option4 == "yes" or option4=="YES":
        save_x = open("X_categories.pickle","wb")
        pickle.dump(X_train,save_x)
        save_x.close()

        save_y = open("y_labels.pickle","wb")
        pickle.dump(y_train,save_y)
        save_y.close()
    
    return X_train,y_train,mapping

def author():
    """
    Returns the Author Name
    """
    return "Author: Vinayak Bhosale"