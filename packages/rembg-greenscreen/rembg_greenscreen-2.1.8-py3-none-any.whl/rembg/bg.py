import os
import typing
import moviepy.editor as mpy
import numpy as np
import requests
import torch
import torch.nn.functional
from hsh.library.hash import Hasher
from tqdm import tqdm
from .u2net import u2net

DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

def iter_frames(path):
    return mpy.VideoFileClip(path).resize(height=320).iter_frames(dtype="uint8")

class Net(torch.nn.Module):
    def __init__(self, model_name):
        super(Net, self).__init__()
        hasher = Hasher()

        model, hash_val, drive_target, env_var = {
            'u2netp':          (u2net.U2NETP,
                                'e4f636406ca4e2af789941e7f139ee2e',
                                '1rbSTGKAE-MTxBYHd-51l2hMOQPT_7EPy',
                                'U2NET_PATH'),
            'u2net':           (u2net.U2NET,
                                '09fb4e49b7f785c9f855baf94916840a',
                                '1-Yg0cxgrNhHP-016FPdp902BR-kSsA4P',
                                'U2NET_PATH'),
            'u2net_human_seg': (u2net.U2NET,
                                '347c3d51b01528e5c6c071e3cff1cb55',
                                '1ao1ovG1Qtx4b7EoskHXmi2E9rp5CHLcZ',
                                'U2NET_PATH')
            }[model_name]
        path = os.environ.get(env_var, os.path.expanduser(os.path.join("~", ".u2net", model_name + ".pth")))
        
        if not os.path.exists(path) or hasher.md5(path) != hash_val:
            head, tail = os.path.split(path)
            os.makedirs(head, exist_ok=True)

            URL = "https://docs.google.com/uc?export=download"

            session = requests.Session()
            response = session.get(URL, params={"id": drive_target}, stream=True)

            token = None
            for key, value in response.cookies.items():
                if key.startswith("download_warning"):
                    token = value
                    break

            if token:
                params = {"id": drive_target, "confirm": token}
                response = session.get(URL, params=params, stream=True)

            total = int(response.headers.get("content-length", 0))

            with open(path, "wb") as file, tqdm(
                desc=f"Downloading {tail} to {head}",
                total=total,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
                ) as bar:
                for data in response.iter_content(chunk_size=1024):
                    size = file.write(data)
                    bar.update(size)

        device = torch.device('cuda')
        precision = torch.float32

        model = torch.jit.load('model.pth')
        model.backbone_scale = 0.25
        model.refine_mode = 'sampling'
        model.refine_sample_pixels = 80_000
        model = model.to(device)

        self.precision = precision
        self.net = model

def remove_many(image_data: typing.List[np.array], net: Net):

    image_data = np.stack(image_data)
    image_data = torch.as_tensor(image_data).to(net.precision).to(DEVICE)

    bgr = torch.rand(10, 3, 1080, 1920).to(net.precision).to(DEVICE)

    pha, _ = net(image_data, bgr)[:2]

    return pha
