# importing libraries
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from torchvision import datasets
from torch.utils.data import DataLoader
from PIL import Image
import os
from faces import get_face_data
import webbrowser


mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20) # initializing mtcnn for face detection
resnet = InceptionResnetV1(pretrained='vggface2').eval() # initializing resnet for face img to embeding conversion


def face_match(img_path, data_path="data.pt"): # img_path= location of photo, data_path= location of data.pt 
    # getting embedding matrix of the given img
    img = Image.open(img_path)
    face, prob = mtcnn(img, return_prob=True) # returns cropped face and probability
    emb = resnet(face.unsqueeze(0)).detach() # detech is to make required gradient false
    
    saved_data = torch.load(data_path) # loading data.pt file
    embedding_list = saved_data[0] # getting embedding data
    name_list = saved_data[1] # getting list of names
    dist_list = [] # list of matched distances, minimum distance is used to identify the person
    
    for idx, emb_db in enumerate(embedding_list):
        dist = torch.dist(emb, emb_db).item()
        dist_list.append(dist)
        
    idx_min = dist_list.index(min(dist_list))
    return (name_list[idx_min], min(dist_list))


get_face_data()


# result = face_match("face_data\Face20241002-1822072.jpg")
# print(result)

test_path = "face_data/"
test_filenames = [test_path + fname for fname in os.listdir(test_path)]
names = []
for pics in range(len(test_filenames)):
    pred_name =  face_match(test_filenames[pics])
    #print(pred_name)
    names.append(pred_name[0])


patient = set(names)
print(patient)


# Dictionary to store patient names and their respective Google Drive links
patient_links = {
    "yash": "https://drive.google.com/drive/folders/1dR5InyxgsAQ1OgdFTfRTrcVgL8hsdWup?usp=sharing",
    "sri": "https://drive.google.com/drive/folders/1k-53KFfACZssm-CCNOO32X5SGfT4ZRAy?usp=sharing",
    "Aditya": "https://drive.google.com/drive/folders/1wzVGG17JgL8Dt56uV2gg5x7BtIiC4IMX?usp=sharing",
    "sanket": "https://drive.google.com/drive/folders/1JuCnJXADfJCzGlp35u65X5On0ywuj6Ml?usp=sharing"
}

# Check if the detected patient is in the dictionary and open the respective link
for name, link in patient_links.items():
    if name in patient:
        webbrowser.open(link)

# chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# # Register Chrome as a browser
# webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
