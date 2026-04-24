import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/pes2ug23cs625/maze_robot_ws/install/maze_solver'
