from .helpers import deprecated
import os
import matplotlib.pyplot as plt
from matplotlib import gridspec
import cv2
import numpy as np
from .images import read_image

TEXT_COLOR = (255, 255, 255)


def get_random_rgb():
    return (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))


def visualize_bbox(img, bbox, class_name=None, color=None, thickness=2):
    """Visualizes a single bounding box on the image"""
    color = color or get_random_rgb()
    # x_min, y_min, w, h = bbox
    # x_min, x_max, y_min, y_max = int(x_min), int(
    #     x_min + w), int(y_min), int(y_min + h)
    x_min, y_min, x_max, y_max = bbox.astype(int)

    cv2.rectangle(img, (x_min, y_min), (x_max, y_max),
                  color=color, thickness=thickness)

    if class_name is not None:
        ((text_width, text_height), _) = cv2.getTextSize(
            class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)

        cv2.rectangle(img, (x_min, y_min - int(2.0 * text_height)),
                      (x_min + int(text_width*1.5), y_min), color, -1)

        cv2.putText(
            img,
            text=class_name,
            org=(x_min, y_min - int(0.3 * text_height)),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=TEXT_COLOR,
            lineType=cv2.LINE_AA,
        )
    return img


def convert_coco_to_default(bbox):
    '''x, y, w, h --> x, y, xx, yy'''
    bbox_coco = bbox.copy()
    bbox_coco[:, 2] = bbox_coco[:, 2] + bbox_coco[:, 0]
    bbox_coco[:, 3] = bbox_coco[:, 3] + bbox_coco[:, 1]
    return bbox_coco


def convert_default_to_coco(bbox):
    '''x, y, xx, yy --> x, y, w, h'''
    bbox_coco = bbox.copy()
    bbox_coco[:, 2] = bbox_coco[:, 2] - bbox_coco[:, 0]
    bbox_coco[:, 3] = bbox_coco[:, 3] - bbox_coco[:, 1]
    return bbox_coco


def visualize(image, bboxes,
              scores=None, category_ids=None, category_id_to_name=None,
              figsize=(12, 12), thickness=2, color=None, bbox_format='default'):
    img = image.copy()

    scores = [''] * len(bboxes) if scores is None else scores
    category_ids = [''] * len(bboxes) if category_ids is None else category_ids

    for bbox, sc, category_id in zip(bboxes, scores, category_ids):
        if category_id_to_name is not None:
            class_name = category_id_to_name[category_id]
            class_name = class_name + ' - ' + str(np.round(sc, 3))
        else:
            class_name = None
        img = visualize_bbox(img, bbox, class_name,
                             color=color,
                             thickness=thickness)
    plt.figure(figsize=figsize)
    plt.axis('off')
    plt.imshow(img)


def draw_mask(img_arr, mask_arr):
    """Draw image with mask"""
    pass


def randint(val_min=0, val_max=255):
    return np.random.randint(val_min, val_max)


@deprecated(message='draw_boxes() function is deprecated. Please use visualize() instead.')
def draw_boxes(img_arr, bboxes, color=None, thickness=2, mode='default'):
    assert mode in ['default', 'coco']
    for box in bboxes:
        draw_box(img_arr, box, color=color, thickness=thickness, mode=mode)


@deprecated(message='draw_box() function is deprecated. Please use visualize() instead.')
def draw_box(img_arr, box, thickness=2, color=None, mode='default'):
    h_img, w_img, c_img = img_arr.shape
    if color is None:
        color = (randint(), randint(), randint())
    print('box', box)
    if mode == 'default':
        x, y, xx, yy = box
        x = int(max(0, x))
        xx = int(min(w_img, xx))
        y = int(max(0, y))
        yy = int(min(h_img, yy))

    elif mode == 'coco':
        x, y, w, h = box
        x = int(max(0, x))
        w = int(min(w_img, x+w_img))
        y = int(max(0, y))
        h = int(min(h_img, y+h_img))
        x, y, xx, yy = x, y, x+w, y+h

    cv2.rectangle(img_arr, (x, y), (xx, yy), color=color, thickness=thickness)


def show_multi_images(list_img_arr,
                      list_subtitles=None,
                      ratio_size=10,
                      rows=1,
                      cmap=None,
                      plt_show=True,
                      title=None,
                      show_colorbar=False,
                      colorbar_fontsize=20,
                      fontsize=30,
                      subtitle_fontsize=20,
                      wspace=0,
                      hspace=0, *args, **kwargs):
    """Show multiple images in a plot"""

    assert ratio_size >= 2, ValueError("ratio_size must be greater than 1")

    columns = len(list_img_arr)//rows
    fig = plt.figure(figsize=(int(ratio_size*columns), int((ratio_size/2)*rows)))
    gs = gridspec.GridSpec(rows, columns,
                           wspace=wspace,
                           hspace=wspace)
    if list_subtitles is not None:
        assert len(list_subtitles) == len(list_img_arr), ValueError('titles and images must be the same in length')

    for i in range(1, columns*rows + 1):
        a = fig.add_subplot(rows, columns, i)
        plt.imshow(list_img_arr[i - 1], cmap=cmap)
        a.set_aspect('equal')
        a.set_xticklabels([])
        a.set_yticklabels([])
        if list_subtitles is not None:
            a.set_title(list_subtitles[i - 1], fontsize=subtitle_fontsize)

    if show_colorbar:
        cbar = plt.colorbar()
        for t in cbar.ax.get_yticklabels():
            t.set_fontsize(colorbar_fontsize)

    if title:
        fig.suptitle(title, fontsize=fontsize)

    if plt_show:
        plt.show()


def show_image_with_paths(list_paths,
                          rows=1,
                          img_dir=None, **kwargs):
    list_img_arr = []
    for path in list_paths:
        if img_dir:
            path = os.path.join(img_dir, path)
        img_arr = read_image(path)
        list_img_arr.append(img_arr)
    show_multi_images(list_img_arr=list_img_arr, rows=rows, **kwargs)
