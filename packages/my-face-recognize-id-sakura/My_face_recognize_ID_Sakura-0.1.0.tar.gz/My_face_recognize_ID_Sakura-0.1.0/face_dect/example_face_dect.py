#encoding = utf-8
import torch
import os
import copy
from PIL import Image
import shutil
import numpy as np
import dlib
import cv2
import sys
# 在这里可以更改是从哪里import的

import torchvision.transforms as transforms
from torch.nn.modules.distance import PairwiseDistance
from Models.CBAM_Face_attention_Resnet_notmaskV3 import resnet34_cbam

# preprocess万金油，好想在week6有改动过，我看看
def preprocess(image_path, detector, predictor, img_size, cl, mask=True):
    image = dlib.load_rgb_image(image_path)
    face_img, TF = None, 0
    # 人脸对齐、切图
    dets = detector(image, 1)
    if len(dets) == 1:
        faces = dlib.full_object_detections()
        faces.append(predictor(image, dets[0]))
        images = dlib.get_face_chips(image, faces, size=img_size)

        image = np.array(images[0]).astype(np.uint8)
        # face_img = Image.fromarray(image).convert('RGB')  #
        face_img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # 生成人脸mask
        dets = detector(image, 1)
        if len(dets) == 1:
            point68 = predictor(image, dets[0])
            landmarks = list()
            INDEX = [0, 2, 14, 16, 17, 18, 19, 24, 25, 26]
            eyebrow_list = [19, 24]
            eyes_list = [36, 45]
            eyebrow = 0
            eyes = 0

            for eb, ey in zip(eyebrow_list, eyes_list):
                eyebrow += point68.part(eb).y
                eyes += point68.part(ey).y
            add_pixel = int(eyes / 2 - eyebrow / 2)

            for idx in INDEX:
                x = point68.part(idx).x
                if idx in eyebrow_list:
                    y = (point68.part(idx).y - 2 * add_pixel) if (point68.part(idx).y - 2 * add_pixel) > 0 else 0
                else:
                    y = point68.part(idx).y
                landmarks.append((x, y))
            belows = []
            # TODO 把鼻子给搞下来 ，增加鼻子关键点
            belows.append([point68.part(29).x, point68.part(29).y])
            for i in range(2, 15, 1):
                belows.append([point68.part(i).x, point68.part(i).y])
            belows = np.array(belows)
            colors = [(200, 183, 144), (163, 150, 134), (172, 170, 169), \
                      (167, 168, 166), (173, 171, 170), (161, 161, 160), \
                      (170, 162, 162)]
            # cl = np.random.choice(len(colors), 1)[0]
            # cl = 0
            if mask:
                cv2.fillConvexPoly(face_img, belows, colors[cl])
            else:
                pass
    return Image.fromarray(face_img).convert('RGB')

def ishowm(ima, imb):
    font = cv2.FONT_HERSHEY_SIMPLEX
    imgone = np.asarray(ima)
    imgtwo = np.asarray(imb)
    # 为了让cv2显示出来
    imgone = cv2.cvtColor(imgone, cv2.COLOR_RGB2BGR)
    imgtwo = cv2.cvtColor(imgtwo, cv2.COLOR_RGB2BGR)
    cv2.putText(imgtwo, 'lay',(1,25),font,1,[0,0,255],2)
    # 两个在通道上合并起来？
    # 让两个图片横着显示
    imgall = np.concatenate([imgone, imgtwo], axis=1)
    return imgall

# 完成输入两个图片路径就能够比较的功能
def compare(img1_path,img2_path,save_path,mask=True):
    pwd = save_path
    font = cv2.FONT_HERSHEY_SIMPLEX
    model = resnet34_cbam(pretrained=False, showlayer=True, num_classes=128)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_pathi = 'Model_training_checkpoints/model_34_triplet_epoch_19_rocNotMasked0.932_rocMasked0.846notmaskV9.pt'
    masked = os.path.join(pwd, 'mask')
    notmasked = os.path.join(pwd, 'notmask')
    print(model_pathi)
    if mask==True:
        from config_mask import config
        os.system('rm -rf %s' % masked)
        if not os.path.exists(masked):
            os.mkdir(masked)
    else:
        from config_notmask import config
        if not os.path.exists(notmasked):
            os.mkdir(notmasked)

    # 判断预训练模型是否存在
    if os.path.exists(model_pathi):
        if torch.cuda.is_available():
            model_state = torch.load(model_pathi)
        else:
            model_state = torch.load(model_pathi, map_location='cpu')
        model.load_state_dict(model_state['model_state_dict'])
        print('loaded %s' % model_pathi)
    else:
        print('不存在预训练模型！')
        sys.exit(0)

    if torch.cuda.is_available():
        model.cuda()
    model.eval()
    # 进行transform，一般是先resize然后to tensor,最后normal
    test_data_transforms = transforms.Compose([
        transforms.Resize([config['image_size'], config['image_size']]),  # resize
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.5, 0.5, 0.5],
            std=[0.5, 0.5, 0.5]
        )
    ])

    threshold = 0.55
    detector = dlib.get_frontal_face_detector()
    # 这个也是配置文件读的
    predicter_path = config['predicter_path']
    predictor = dlib.shape_predictor(predicter_path)
    img_size = config['image_size']
    ima = preprocess(img1_path, detector, predictor, img_size, 1, mask)
    imb = preprocess(img2_path, detector, predictor, img_size, 3, mask)
    # 这部分是调用函数直接显示用的
    imb_ = copy.deepcopy(imb)
    ima_ = copy.deepcopy(ima)
    #
    ima, imb = test_data_transforms(ima), test_data_transforms(imb)
    if torch.cuda.is_available():
        data_a = ima.unsqueeze(0).cuda()
        data_b = imb.unsqueeze(0).cuda()
    else:
        data_a, data_b = ima.unsqueeze(0), imb.unsqueeze(0)
    # 调用上面函数
    imgall = ishowm(ima_, imb_)
    output_a, output_b = model(data_a), model(data_b)
    # 归一化
    output_a = torch.div(output_a, torch.norm(output_a))
    output_b = torch.div(output_b, torch.norm(output_b))
    l2_distance = PairwiseDistance(2)  # .cuda()
    # 进行l2距离的计算
    distance = l2_distance.forward(output_a, output_b)
    print('从两张图片提取出来的特征向量的欧氏距离是：%1.3f' % distance)
    # 写上去
    if distance > threshold:
        cv2.putText(imgall, 'dis:%1.4f, not the same people' % distance, (1, 19), font, 0.6, [128, 0, 128], 1)

    else:
        cv2.putText(imgall, 'dis:%1.4f, the same people' % distance, (1, 19), font, 0.6, [0, 128, 128], 1)
    imgall = Image.fromarray(imgall).convert('RGB')
    # 如果戴口罩就保存图片
    version = 'V9';
    if mask:
        # 放到了那个文件夹里
        imgall.save(os.path.join(masked, 'dis%1.3f_faceshow_%s.jpg' % (distance, version)))
    else:
        imgall.save(os.path.join(notmasked, 'dis%1.3f_faceshow_%s.jpg' % (distance, version)))


if __name__ == '__main__':
    save_path = './'
    img1_path = './photo/1_0001.jpg'
    img2_path = './photo/1_0002.jpg'
    compare(img1_path, img2_path, save_path,mask=True)