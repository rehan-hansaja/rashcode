#detect.py
# import cv2
# import json
# import torchvision
# import torch
# from flask import jsonify

# from detectron2.data import build_detection_test_loader
# from detectron2.evaluation import COCOEvaluator, inference_on_dataset
from detectron2.utils.visualizer import ColorMode
# from detectron2.engine import DefaultTrainer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.utils.visualizer import Visualizer
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo
from detectron2.utils.logger import setup_logger
# import detectron2
from scipy.spatial import distance
# from PIL import Image
# from tensorboard.backend.event_processing import event_accumulator as ea
# from matplotlib import colors
# import seaborn as snsi
import os
# from pycocotools.coco import COCO
# import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
# import random
pylab.rcParams['figure.figsize'] = (8.0, 10.0)  # Import Libraries

# For visualization

# Scipy for calculating distance


setup_logger()

# import some common libraries

# import some common detectron2 utilities


def detect(image_path, model, scale):
    # get configuration
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file(
        "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1  # only has one class (damage) + 1
    cfg.MODEL.RETINANET.NUM_CLASSES = 1  # only has one class (damage) + 1
    cfg.MODEL.WEIGHTS = os.path.join(
        "models/damage_segmentation_model_v5.pth")
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
    cfg['MODEL']['DEVICE'] = 'cpu'  # or cuda
    damage_predictor = DefaultPredictor(cfg)

    cfg_mul = get_cfg()
    cfg_mul.merge_from_file(model_zoo.get_config_file(
        "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    # only has five classes (headlamp,hood,rear_bumper,front_bumper_door) + 1
    cfg_mul.MODEL.ROI_HEADS.NUM_CLASSES = 5
    # only has five classes (headlamp,hood,rear_bumper,front_bumper_door) + 1
    cfg_mul.MODEL.RETINANET.NUM_CLASSES = 5
    cfg_mul.MODEL.WEIGHTS = os.path.join(
        "models/part_segmentation_model.pth")
    cfg_mul.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
    cfg_mul['MODEL']['DEVICE'] = 'cpu'  # or cuda
    part_predictor = DefaultPredictor(cfg_mul)

    damage_class_map = {0: 'damage'}
    parts_class_map = {0: 'headlamp', 1: 'rear_bumper',
                       2: 'door', 3: 'hood', 4: 'front_bumper'}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 12))
    im = io.imread(image_path)

    # damage inference
    damage_outputs = damage_predictor(im)
    damage_v = Visualizer(im[:, :, ::-1],
                          metadata=MetadataCatalog.get("car_dataset_val"),
                          scale=0.5,
                          # remove the colors of unsegmented pixels. This option is only available for segmentation models
                          instance_mode=ColorMode.IMAGE_BW
                          )
    damage_out = damage_v.draw_instance_predictions(
        damage_outputs["instances"].to("cpu"))

    # part inference
    parts_outputs = part_predictor(im)
    parts_v = Visualizer(im[:, :, ::-1],
                         metadata=MetadataCatalog.get("car_mul_dataset_val"),
                         scale=0.5,
                         # remove the colors of unsegmented pixels. This option is only available for segmentation models
                         instance_mode=ColorMode.IMAGE_BW
                         )
    parts_out = parts_v.draw_instance_predictions(
        parts_outputs["instances"].to("cpu"))

    # #plot
    # ax1.imshow(damage_out.get_image()[:, :, ::-1],)
    # ax2.imshow(parts_out.get_image()[:, :, ::-1])

    damage_prediction_classes = [damage_class_map[el] + "_" + str(
        indx) for indx, el in enumerate(damage_outputs["instances"].pred_classes.tolist())]
    print(damage_outputs["instances"].pred_boxes.get_centers(
    ).tolist(), damage_outputs["instances"].pred_boxes)
    damage_polygon_centers = damage_outputs["instances"].pred_boxes
    damage_dict = dict(zip(damage_prediction_classes, damage_polygon_centers))
    parts_prediction_classes = [parts_class_map[el] + "_" + str(
        indx) for indx, el in enumerate(parts_outputs["instances"].pred_classes.tolist())]
    parts_polygon_centers = parts_outputs["instances"].pred_boxes

    # Remove centers which lie in beyond 800 units
    parts_polygon_centers_filtered = list(
        filter(lambda x: x[0] < 800 and x[1] < 800, parts_polygon_centers))
    parts_dict = dict(zip(parts_prediction_classes,
                      parts_polygon_centers_filtered))

    def get_centers(point):
        return [(point[0] + point[2]) / 2, (point[1] + point[3]) / 2]

    def get_area(point):
        return abs(point[2] - point[0]) * abs(point[3] - point[1])

    def detect_damage_part(damage_dict, parts_dict):
        not_identified_damages = []
        try:
            max_distance = 10e9
            assert len(
                damage_dict) > 0, "AssertError: damage_dict should have atleast one damage"
            assert len(
                parts_dict) > 0, "AssertError: parts_dict should have atleast one part"
            max_distance_dict = dict(
                zip(damage_dict.keys(), [max_distance]*len(damage_dict)))
            part_name = dict(zip(damage_dict.keys(), ['']*len(damage_dict)))

            for y in parts_dict.keys():
                for x in damage_dict.keys():
                    # print(damage_dict[x].tolist(), parts_dict[y])
                    dis = distance.euclidean(get_centers(
                        damage_dict[x].tolist()), get_centers(parts_dict[y].tolist()))
                    if dis < max_distance_dict[x]:

                        part_name[x] = [y.rsplit('_', 1)[0], get_area(
                            damage_dict[x].tolist())]
                    else:
                        not_identified_damages.append([x, y])
            return list(part_name.values()), not_identified_damages

        except Exception as e:
            print(e)
            return [], []

    REAL_WIDTH_IN_CM = scale
    CAR_MODEL = model

    REPLACE_IF_AREA_GREATER_THAN = {
        'toyota': {
            'door': 2000,
            'headlamp': 0,
            'rear_bumper': 1000,
            'hood': 1500,
            'front_bumper': 3000
        }
    }

    COST_DICTIONARY = {'toyota': {
        'door': {'replace': 10000, 'fix': 100},
        'headlamp': {'replace': 20000},
        'rear_bumper': {'replace': 30000, 'fix': 200},
        'hood': {'replace': 40000, 'fix': 300},
        'front_bumper': {'replace': 15000, 'fix': 150}}
    }

    def should_replace(item):
        return item[1] > REPLACE_IF_AREA_GREATER_THAN[CAR_MODEL][item[0]]

    def calculate_cost(item):
        if (should_replace(item)):
            r_or_f = 'replace'
            return (COST_DICTIONARY[CAR_MODEL][item[0]]['replace'])
        else:
            r_or_f = "fix"
            return (COST_DICTIONARY[CAR_MODEL][item[0]]['fix'] * item[1])

    identified, not_identified = detect_damage_part(damage_dict, parts_dict)

    total_cost = 0
    rows = []

    print("#"*25 + " DAMAGES " + "#"*25)
    print()
    print("Part" + " " * 30 + "Area")
    print("-" * 65)
    for item in identified:
        # print(item)
        if (should_replace(item)):
            r_or_f = 'Replace'
        else:
            r_or_f = "Fix"
        cost = calculate_cost(item)
        rows.append([item[0], r_or_f, cost, item[1]])
        print(item[0], " " * (30 - len(item[0]) + 4), item[1])

    print()

    print("#"*25 + " COST ESTIMATION " + "#"*25)
    print("")
    print("Part" + " " * 30 + "Replace/Fix" + " " *
          10 + "Cost (Rs)" + " " * 10 + "Damaged Area")
    print("-" * 65)

    fix = []
    replace = []

    # Items to be fixed
    for row in rows:
        if (row[0] not in [x[0] for x in rows if x[1] == 'Replace']):
            total_cost += row[2]
            print(row[0], " " * (30 - len(row[0]) + 4), row[1] + " " *
                  (10 - len(row[1]) + 9), str(row[2]), " " * 10 + str(row[3]))
            fix.append(row)

    # Items to be replaced
    for item in list(set([x[0] for x in rows if x[1] == 'Replace'])):
        row = [x for x in rows if x[1] == 'Replace' and x[0] == item][0]
        total_cost += row[2]
        print(row[0], " " * (30 - len(row[0]) + 4), row[1] +
              " " * (10 - len(row[1]) + 9), str(row[2]))
        replace.append(row)

    print("-" * 65)
    print("TOTAL DETECTED ESTIMATED COST", " " *
          int((40 - len("TOTAL DETECTED ESTIMATED COST") + 14)/1), str(total_cost))
    print()
    print("#" * 65)
    # print("Damaged Parts: ",identified)
    print("Not detected: ", not_identified)

    # At the end of the detect function in detect.py, add the following code to save the results

    # Define the path to the text file
    results_file_path = 'detected/results.txt'

    # Open the file in write mode
    with open(results_file_path, 'w') as file:
        # Write the header
        file.write("                            COST ESTIMATION            \n\n")
        # file.write("Part" + " " * 30 + "Replace/Fix" + " " * 10 + "Cost (Rs)" + " " * 10 + "Damaged Area\n")
        file.write("Part" + " " * 30 + "Replace/Fix" + " " * 10 + "Cost (Rs)" + "\n")
        file.write("-" * 65 + "\n")

        # Write the items to be fixed
        for row in fix:
            file.write(f"{row[0]}" + " " * (30 - len(row[0])) + f"{row[1]}" + " " * (
                        10 - len(row[1])) + f"{row[2]}" + " " * 10 + f"{row[3]}\n")

        # Write the items to be replaced
        for item in replace:
            file.write(
                f"{item[0]}" + " " * (30 - len(item[0])) + f"{item[1]}" + " " * (10 - len(item[1])) + f"{item[2]}\n")

        # Write the total cost
        file.write("-" * 65 + "\n")
        file.write(f"TOTAL DETECTED ESTIMATED COST" + " " * (
                    40 - len("TOTAL DETECTED ESTIMATED COST") + 14) + f"{total_cost}\n")


    # #plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
    ax1.set_title("Detected damaged areas")
    ax1.imshow(damage_out.get_image()[:, :, ::-1],)
    ax2.set_title('Detected parts')
    ax2.imshow(parts_out.get_image()[:, :, ::-1])
    plt.savefig('detected/output.jpg', format='jpg', bbox_inches='tight')

    return {'replace': replace, 'fix': fix}



