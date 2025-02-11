import cv2
import time
import torch
import numpy as np
import matplotlib.pyplot as plt

def cv_imread( file_path):
    try:
        cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    except:
        return None
    # if len(cv_img.shape) == 3:
    #     cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
    return cv_img

def show_img(imgs: np.ndarray, color=False):
    if (len(imgs.shape) == 3 and color) or (len(imgs.shape) == 2 and not color):
        imgs = np.expand_dims(imgs, axis=0)
    for img in imgs:
        # print(img)
        plt.figure()
        plt.imshow(img, cmap=None if color else 'gray')


def draw_bbox(img_path, result, color=(255, 0, 0),thickness=2):
    if isinstance(img_path, str):
        img_path = cv_imread(img_path)
        img_path = cv2.cvtColor(img_path, cv2.COLOR_BGR2RGB)
    img_path = img_path.copy()
    for point in result:
        point = point.astype(int)
        cv2.line(img_path, tuple(point[0]), tuple(point[1]), color, thickness)
        cv2.line(img_path, tuple(point[1]), tuple(point[2]), color, thickness)
        cv2.line(img_path, tuple(point[2]), tuple(point[3]), color, thickness)
        cv2.line(img_path, tuple(point[3]), tuple(point[0]), color, thickness)
    return img_path

def draw_bbox_with_2_mask(img_path, result1,result2, color1=(255, 0, 0),color2=(0,255,0),thickness=2):
    if isinstance(img_path, str):
        img_path = cv_imread(img_path)
        img_path = cv2.cvtColor(img_path, cv2.COLOR_BGR2RGB)
    img_path = img_path.copy()
    for point in result1:
        point = point.astype(int)
        cv2.line(img_path, tuple(point[0]), tuple(point[1]), color1, thickness)
        cv2.line(img_path, tuple(point[1]), tuple(point[2]), color1, thickness)
        cv2.line(img_path, tuple(point[2]), tuple(point[3]), color1, thickness)
        cv2.line(img_path, tuple(point[3]), tuple(point[0]), color1, thickness)

    for point in result2:
        point = point.astype(int)
        cv2.line(img_path, tuple(point[0]), tuple(point[1]), color2, thickness)
        cv2.line(img_path, tuple(point[1]), tuple(point[2]), color2, thickness)
        cv2.line(img_path, tuple(point[2]), tuple(point[3]), color2, thickness)
        cv2.line(img_path, tuple(point[3]), tuple(point[0]), color2, thickness)
    return img_path

def setup_logger(log_file_path: str = None):
    import logging
    from colorlog import ColoredFormatter
    logging.basicConfig(filename=log_file_path, format='%(asctime)s %(levelname)-8s %(filename)s: %(message)s',
                        # 定义输出log的格式
                        datefmt='%Y-%m-%d %H:%M:%S', )
    """Return a logger with a default ColoredFormatter."""
    formatter = ColoredFormatter("%(asctime)s %(log_color)s%(levelname)-8s %(reset)s %(filename)s: %(message)s",
                                 datefmt='%Y-%m-%d %H:%M:%S',
                                 reset=True,
                                 log_colors={
                                     'DEBUG': 'blue',
                                     'INFO': 'green',
                                     'WARNING': 'yellow',
                                     'ERROR': 'red',
                                     'CRITICAL': 'red',
                                 })

    logger = logging.getLogger('project')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.info('logger init finished')
    return logger


def save_checkpoint(checkpoint_path, model, optimizer, epoch, logger):
    state = {'state_dict': model.state_dict(),
             'optimizer': optimizer.state_dict(),
             'epoch': epoch}
    torch.save(state, checkpoint_path)
    logger.info('models saved to %s' % checkpoint_path)


def load_checkpoint(checkpoint_path, model, logger, device, optimizer=None):
    state = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(state['state_dict'])
    if optimizer is not None:
        optimizer.load_state_dict(state['optimizer'])
    start_epoch = state['epoch']
    logger.info('models loaded from %s' % checkpoint_path)
    return start_epoch


# --exeTime
def exe_time(func):
    def newFunc(*args, **args2):
        t0 = time.time()
        back = func(*args, **args2)
        print("{} cost {:.3f}s".format(func.__name__, time.time() - t0))
        return back
    return newFunc
