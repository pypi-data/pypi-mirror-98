# -*- encoding: utf-8 -*-
"""
A wrapper for Annotations directory.
"""

import os
import glob
import csv
import logging
import tqdm
import numpy as np
from .xml_tools import PascalXml
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def split_list(val, split_num):
    max_val = max(val)
    min_val = min(val)
    x = list(np.arange(min_val, max_val,
                       (max_val - min_val) / split_num)) + [max_val]

    normalized_val = [(n - min_val) / (max_val - min_val) for n in val]
    normalized_val = [int(n * split_num) for n in normalized_val]
    y = [normalized_val.count(n) for n in range(split_num + 1)]
    return x, y


class Annotations():
    """ deal with annotations in PascalVOC format dataset.

    Attributes:
        ann_dir: str, the dir including xmls.
    Raises:
        AssertError: can not find path.
    """
    def __init__(self, ann_dir):
        self.dir = ann_dir
        self.ann_list = []

    def load(self, name_list=None):
        if name_list is None:
            self.ann_list = sorted(
                glob.glob(os.path.join(self.dir, '*.xml')))
        else:
            self.ann_list = [
                os.path.join(self.dir, '{}.xml'.format(name))
                for name in name_list
            ]
        logger.info('Find {} xml files.'.format(len(self.ann_list)))
        return self

    def count_category(self):
        name_dict = {}
        for xml_path in self.ann_list:
            xml_data = PascalXml().load(xml_path)
            xml_name_list = [obj.name for obj in xml_data.object]
            for name in xml_name_list:
                if name not in name_dict:
                    name_dict[name] = {'count': 0, 'included_file': []}
                name_dict[name]['count'] += 1
                file_name = os.path.basename(xml_path)
                if file_name not in name_dict[name]['included_file']:
                    name_dict[name]['included_file'].append(file_name)
        return name_dict

    def get_bbox_info(self):
        id_bbox_map = {}
        for xml_path in self.ann_list:
            xml_data = PascalXml().load(xml_path)
            size = [int(xml_data.size.heihgt), int(xml_data.size.width)]
            if 0 in size:
                print('Warrning: {} size error: {}'.format(xml_path, size))
                continue
            objects = xml_data.object
            id_bbox_map[os.path.basename(xml_path)] = objects
        return id_bbox_map

    def iou_analyse(self, save_dir='./', split_num=100):
        """ Draw iou distribution in dataset.

        Args:
            save_dir: str, image save dir;
            split_num: int, the number of data partitions
        """
        class_iou_map = {}
        for xml_path in self.ann_list:
            xml_data = PascalXml().load(xml_path)
            width = int(xml_data.size.width)
            height = int(xml_data.size.height)
            image_area = width * height

            for obj in xml_data.object:
                if obj.name not in class_iou_map:
                    class_iou_map[obj.name] = []

                xmin = int(obj.bndbox.xmin)
                ymin = int(obj.bndbox.ymin)
                xmax = int(obj.bndbox.xmax)
                ymax = int(obj.bndbox.ymax)
                roi_area = (xmax - xmin) * (ymax - ymin)
                class_iou_map[obj.name].append(roi_area / image_area)

        for key, val in class_iou_map.items():
            x, y = split_list(val, split_num)

            plt.figure(figsize=(8, 4))
            plt.plot(x, y, "bD-", linewidth=1)
            plt.xlabel("IOU(object area/image area)")
            plt.ylabel("Times")
            plt.title("The distribution of Objects' IOU in the dataset")
            plt.savefig(
                os.path.join(save_dir, "IOU_distribution-{}.jpg".format(key)))
        return class_iou_map

    def height_analyse(self, save_dir='./', split_num=100):
        """ Draw height ratio distribution in dataset.

        Args:
            save_dir: str, image save dir;
            split_num: int, the number of data partitions
        """
        class_iou_map = {}
        for xml_path in self.ann_list:
            xml_data = PascalXml().load(xml_path)
            height = int(xml_data.size.height)

            for obj in xml_data.object:
                if obj.name not in class_iou_map:
                    class_iou_map[obj.name] = []

                ymin = int(obj.bndbox.ymin)
                ymax = int(obj.bndbox.ymax)
                class_iou_map[obj.name].append((ymax - ymin) / height)

        for key, val in class_iou_map.items():
            x, y = split_list(val, split_num)

            plt.figure(figsize=(8, 4))
            plt.plot(x, y, "bD-", linewidth=1)
            plt.xlabel("Height ratio(object/image) percent/%")
            plt.ylabel("Times")
            plt.title("The distribution of Objects' height in the dataset")
            plt.savefig(
                os.path.join(save_dir,
                             "Height_distribution-{}.jpg".format(key)))
        return class_iou_map

    def width_analyse(self, save_dir='./', split_num=100):
        """ Draw width ratio distribution in dataset.

        Args:
            save_dir: str, image save dir;
            split_num: int, the number of data partitions
        """
        class_iou_map = {}
        for xml_path in self.ann_list:
            xml_data = PascalXml().load(xml_path)
            width = int(xml_data.size.width)

            for obj in xml_data.object:
                if obj.name not in class_iou_map:
                    class_iou_map[obj.name] = []

                xmin = int(obj.bndbox.xmin)
                xmax = int(obj.bndbox.xmax)
                width_ratio = (xmax - xmin) / width

                class_iou_map[obj.name].append(width_ratio)

        for key, val in class_iou_map.items():
            x, y = split_list(val, split_num)

            plt.figure(figsize=(8, 4))
            plt.plot(x, y, "bD-", linewidth=1)
            plt.xlabel("Width ratio(object/image) percent/%")
            plt.ylabel("Times")
            plt.title("The distribution of Objects' width in the dataset")
            plt.savefig(
                os.path.join(save_dir,
                             "Width_distribution-{}.jpg".format(key)))
        return class_iou_map

    def convert2csv(self, save_path, category_list=[]):
        """find all bndbox info and save to csv file. If category_list exist, only save
        the categories in list.

        Arguments:
            save_path: a csv file path.
            category_list: a list for keep category to save.

        Raises:
            AssertionError: the save path not a csv file path.
        """
        header = [
            'file_name', 'width', 'height', 'category', 'xmin', 'ymin', 'xmax',
            'ymax'
        ]

        xmls_list = sorted(glob.glob(os.path.join(self.dir, '*.xml')))
        logger.info(f"Find {len(xmls_list)} xmls")

        assert '.csv' == save_path[
            -4:], "Make sure the save path is a new csv file path"
        f = open(save_path, 'w')
        f_csv = csv.writer(f)
        f_csv.writerow(header)

        # bbox_info_list = []
        for xml_path in tqdm.tqdm(xmls_list):
            # print(xml_path)
            bbox_list = PascalXml().load(xml_path).convert2csv(category_list)
            f_csv.writerows(bbox_list)

        f.close()

        return self
