import torch.nn as nn
import torch
import numpy as np
import random
import os

def set_seed(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    # When running on the CuDNN backend, two further options must be set
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    print(f"Random seed set as {seed}")

def weights_init_normal(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        nn.init.normal_(m.weight.data, 0.0, 0.02) # reset Conv2d's weight(tensor) with Gaussian Distribution
        if hasattr(m, 'bias') and m.bias is not None:
            nn.init.constant_(m.bias.data, 0.0) # reset Conv2d's bias(tensor) with Constant(0)
        elif classname.find('InstanceNorm2d') != -1:
            nn.init.normal_(m.weight.data, 1.0, 0.02)
            nn.init.constant_(m.bias.data, 0.0)

def save_model(model, name, cfg):
    folder_path = cfg.model_folder
    i = 1
    new_model_name = name
    while os.path.exists(os.path.join(folder_path, new_model_name + ".pt")):
        new_model_name = name + "_" + str(i)
        i += 1

    path = os.path.join(folder_path, new_model_name + ".pt")

    torch.save(model, path)

    print(f"Model saved to {new_model_name}.pt")

def save_checkpoint(model, name, optimizer, epoch, loss, cfg):
    if not os.path.exists(cfg.model_folder):
        os.makedirs(cfg.model_folder)

    checkpoint_path = os.path.join(cfg.model_folder, str(name) + '_' + str(epoch) + ".pt")

    checkpoint = {
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'epoch': epoch
    }
    torch.save(checkpoint, checkpoint_path)
    print(f"Checkpoint saved to {checkpoint_path}")

def load_checkpoint(model, name, optimizer, checkpoint_path=None):
    checkpoint = torch.load(checkpoint_path)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    epoch = checkpoint['epoch']

    print(f"Loaded checkpoint {name} from epoch {epoch}")

    return model, optimizer, epoch

