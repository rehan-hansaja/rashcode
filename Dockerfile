FROM ubuntu

RUN apt update
RUN apt install python3-pip git -y libgl1-mesa-glx
RUN pip3 install Flask pycocotools -U torch torchvision opencv-python
RUN git clone https://github.com/facebookresearch/detectron2 detectron2_repo
RUN pip3 install -e detectron2_repo
RUN apt install -y libglib2.0-0
RUN pip3 install scipy scikit-image matplotlib
#RUN pip3 install git+https://github.com/facebookresearch/fvcore.git \
#     pip install opencv-python \
#    pip install -U torch torchvision \
#    pip install pycocotools

WORKDIR /app

COPY . .

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]