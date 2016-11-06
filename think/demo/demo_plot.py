import numpy as np
import matplotlib.pyplot as plt
import random, math
from demo_train import simu, signal_generator, idx_to_type
from demo_config import *

x = np.linspace(sample_l, sample_r, sample_num)
for t in range(supported_type):
	for _ in range(1):
		line, = plt.plot(x, signal_generator(x, t, simu_level), '-', linewidth=2, label=idx_to_type(t)+str(_))
	plt.legend()
	plt.show()

