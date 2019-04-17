import os
import numpy as np
current_path = os.path.dirname(os.path.abspath(__file__))
import subprocess
subprocess.run([current_path + '/run', 'check'])
