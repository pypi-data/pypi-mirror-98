

def set_seed_tf(seed_value=42):
    import os
    import random
    import numpy as np
    import tensorflow as tf

    os.environ['PYTHONHASHSEED'] = '0'
    os.environ['CUDA_VISIBLE_DEVICES'] = ""

    np.random.seed(seed_value)
    random.seed(seed_value)
    tf.random.set_seed(seed_value)
    print('设置随机种子: {}' . format(seed_value))
    

def set_seed(seed_value):
    import random
    import numpy as np

    random.seed(seed_value)
    np.random.seed(seed=seed_value)
    print('设置随机种子: {}' . format(seed_value))
