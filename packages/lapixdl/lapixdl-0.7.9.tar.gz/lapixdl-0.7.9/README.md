# LAPiX DL - Utils for Computer Vision Deep Learning research

This package contains utilitary functions to support train and evaluation of Deep Learning models applied to images.

Three computer vision approaches are covered: Segmentation, Detection and Classification.

## How to use

### For Model Evaluation

This module exports the following functions for model evaluation:
```
from lapixdl.evaluation.evaluate import evaluate_segmentation
from lapixdl.evaluation.evaluate import evaluate_detection
from lapixdl.evaluation.evaluate import evaluate_classification
```

All model evaluation methods need two iterators: **one for the ground truth itens and one for the predictions**.

These iterators must be sorted equaly, assuring that the ground truth and the prediction of the same sample are at the same position.

#### Example of segmentation model evaluation using **PyTorch**:

```
from lapixdl.evaluation.evaluate import evaluate_segmentation

classes = ['background', 'object']

# Iterator for GT masks 
# `dl` is a PyTorch DataLoader
def gt_mask_iterator_from_dl(dl):
  for imgs, masks in iter(dl):
    for mask in masks:
      yield mask

# Iterator for prediction masks 
# `predict` a function that, given an image, predicts the mask.
def pred_mask_iterator_from_dl(dl, predict):
  for imgs, masks in iter(dl):
    for img in imgs:
      yield predict(img)

gt_masks = gt_mask_iterator_from_dl(validation_dl)
pred_masks = pred_mask_iterator_from_dl(validation_dl, prediction_function)

# Calculates and shows metrics
eval = evaluate_segmentation(gt_masks, pred_masks, classes)

# Shows confusion matrix and returns its Figure and Axes
fig, axes = eval.show_confusion_matrix()
```

### For Results Visualization

This module exports the following functions for results visualization:
```
from lapixdl.evaluation.visualize import show_segmentations
from lapixdl.evaluation.visualize import show_classifications
from lapixdl.evaluation.visualize import show_detections
```

The available color maps are the [ones from matplotlib](https://matplotlib.org/3.1.1/gallery/color/colormap_reference.html).

### For Data Conversion

This module exports the following functions for data conversion:
```
from lapixdl.convert.labelbox import labelbox_to_coco
```

#### Example of conversion from **Labelbox** to **COCO** labels format:

```
import json
from lapixdl.convert.labelbox import labelbox_to_coco

# Loads Labelbox json
with open('./labelbox.json') as in_file:
    labelbox_file = json.load(in_file)

# Converts it
coco_dict = labelbox_to_coco(labelbox_file)

# Saves converted json
with open('./coco.json', 'w') as out_file:
    json.dump(coco_dict, out_file)

```
