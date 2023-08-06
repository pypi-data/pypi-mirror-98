# `bpycv`: computer vision and deep learning utils for Blender

### Contents: [Features](#-features) | [Install](#-install) | [Fast Demo](#-fast-demo) | [Tips](#-tips) 

![0](https://user-images.githubusercontent.com/10448025/96836463-98135680-1477-11eb-8a5f-8911bc454336.jpg)      
*Render instance annoatation, RGB image and depth in one line code*

## ▮ Features
 - [x] Render depth
 - [x] Render annotations for semantic segmentation, instance segmentation, and panoptic segmentation 
 - [x] Generate 6DoF pose ground truth
 - [x] Pre-define domain randomization: light
 - [x] Pre-define domain randomization: background
 - [x] Pre-define domain randomization: [distractors](https://arxiv.org/pdf/1804.06516)
 - [x] Pre-define domain randomization: textures
 - [x] Support docker: `docker run -v /tmp:/tmp diyer22/bpycv`
 - [x] To Cityscapes format
 - [ ] To COCO format

**News:** [We win 🥈2nd place in IROS 2020 Open Cloud Robot Table Organization Challenge (OCRTOC)](https://github.com/DIYer22/bpycv/issues/15)

## ▮ Install
`bpycv` support Blender 2.8, 2.9

Troubleshooting tips: [doc/troubleshooting.md](doc/troubleshooting.md)

#### 1. Install OpenExr
`bpycv` use OpenExr to extract depth map from Blender

For a Debian-based Linux(Ubuntu):
```bash
sudo apt-get install libopenexr-dev
```

For other OS, please follow [OpenExr's instruction](https://excamera.com/sphinx/articles-openexr.html).

#### 2. Install python package
Example for Blender 2.90:
```bash
cd <path to blender>/2.90/python/bin
./python3.7m -m ensurepip  # get pip
./python3.7m -m pip install -U pip setuptools wheel 
./python3.7m -m pip install -U opencv-python openexr bpycv
```

## ▮ Fast Demo
#### 1. Instance Segmentation and Depth Demo
Copy-paste this code to `Scripting/Text Editor` and click `Run Script` button(or `Alt+P`)
```python
import cv2
import bpy
import bpycv
import random
import numpy as np

# remove all MESH objects
[bpy.data.objects.remove(obj) for obj in bpy.data.objects if obj.type == "MESH"]

for index in range(1, 20):
    # create cube and sphere as instance at random location
    location = [random.uniform(-2, 2) for _ in range(3)]
    if index % 2:
        bpy.ops.mesh.primitive_cube_add(size=0.5, location=location)
        categories_id = 1
    else:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=location)
        categories_id = 2
    obj = bpy.context.active_object
    # set each instance a unique inst_id, which is used to generate instance annotation.
    obj["inst_id"] = categories_id * 1000 + index

# render image, instance annoatation and depth in one line code
# result["ycb_meta"] is 6d pose GT
result = bpycv.render_data()

# save result
cv2.imwrite(
    "demo-rgb.jpg", result["image"][..., ::-1]
)  # transfer RGB image to opencv's BGR

# save instance map as 16 bit png
# the value of each pixel represents the inst_id of the object to which the pixel belongs
cv2.imwrite("demo-inst.png", np.uint16(result["inst"]))

# convert depth units from meters to millimeters
depth_in_mm = result["depth"] * 1000
cv2.imwrite("demo-depth.png", np.uint16(depth_in_mm))  # save as 16bit png

# visualization inst_rgb_depth for human
cv2.imwrite("demo-vis(inst_rgb_depth).jpg", result.vis()[..., ::-1])
```
Open `./demo-vis(inst_rgb_depth).jpg`:   

![demo-vis(inst_rgb_depth)](https://user-images.githubusercontent.com/10448025/96727938-322abe80-13e6-11eb-9888-58886e8e68fd.jpg)

#### 2. YCB Demo
Inculding domain randomization for background, light, and distractor.
```shell
mkdir ycb_demo
cd ycb_demo/

# prepare demo code and data
git clone https://github.com/DIYer22/bpycv
git clone https://github.com/DIYer22/bpycv_example_data

cd bpycv/example/

blender -b -P ycb_demo.py

cd dataset/vis/
ls .  # visualize result here
```
Open `0.jpg`:   
![0](https://user-images.githubusercontent.com/10448025/96836463-98135680-1477-11eb-8a5f-8911bc454336.jpg)    
(instance_map | RGB | depth)

YCB demo code: [example/ycb_demo.py](example/ycb_demo.py)

#### 3. 6DoF Pose Demo
<img src="https://user-images.githubusercontent.com/10448025/74708759-5e3ee000-5258-11ea-8849-0174c34d507c.png" style="width:300px">

Generate and visualize 6DoF pose GT: [example/6d_pose_demo.py](example/6d_pose_demo.py)

## ▮ Tips
 > Blender may can't direct load `.obj` and `.dea` file from YCB and ShapeNet dataset.  
 > It's better to transefer and format using [`meshlabserver`](https://github.com/cnr-isti-vclab/meshlab/releases) by run `meshlabserver -i raw.obj -o for_blender.obj -m wt`

<br>
<br>
<div align="center">

**[suggestion](https://github.com/DIYer22/bpycv/issues) and pull request are welcome** 😊
</div>