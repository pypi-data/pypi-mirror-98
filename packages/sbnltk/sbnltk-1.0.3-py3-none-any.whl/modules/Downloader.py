import gdown
import os
import sbnltk
from os import path


class downloader():

    download_link={}            # for reserved link
    download_link_default=""    # deafault download link
    url_prefix="https://drive.google.com/uc?id="    # download url prefix
    def __init__(self):
        try:
            if path.exists('../dataset/download_link.txt')==False:
                url = self.url_prefix+self.download_link_default;
                output = 'dataset/download_link.txt'
                gdown.download(url, output, quiet=False)
            for line in open('../dataset/download_link.txt', 'r'):
                line=line.rstrip('\n')
                items=line.split(' ')
                self.download_link[items[0]]=(items[1],items[2])    # Header = (download_id, fileType)
        except:
            raise ValueError("Error in loading download link! Try again!")

    '''
    model_path='model/'     for models
    model_path='dataset/'   for dataset
    
    '''
    def download(self,model,model_path):
        try:
            if self.download_link.get(model)==None:
                raise ValueError('Model Name does not exists!! ')
            model_path=model_path+model+'.'+self.download_link[model][1]
            if path.exists(model_path)==True:
                pass
            else:
                url = self.url_prefix + self.download_link[model][0]
                output = model_path
                gdown.download(url, output, quiet=False)
        except:
            raise ValueError("Error when downloading model!! Check internet Connection!!")

    def remove(self,model_path):
        try:
            os.remove(model_path)
            print(f"{sbnltk.bcolors.OKGREEN} {model_path} is removed!! {sbnltk.bcolors.ENDC} ")
        except:
            raise  ValueError("Model path does not exist!!")


    def reDownload(self,model,model_path):
        try:
            if self.download_link.get(model)==None:
                raise ValueError("Model path does not exist!!")
            model_path=model_path+model+'.'+self.download_link[model][1]
            if path.exists(model_path)==True:
                self.remove(model_path)
            url = self.url_prefix + self.download_link[model][0]
            output = model_path
            gdown.download(url, output, quiet=False)
            print(f"{sbnltk.bcolors.OKGREEN} Download Completed!! {sbnltk.bcolors.ENDC} ")
        except:
            raise ValueError("Error when downloading model!! Check Internet Connection")
