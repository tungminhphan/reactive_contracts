"""
Abstraction scheme for three islands
Tung M. Phan
California Institute of Technology
April 24, 2019
"""

DELTA = ['button1', 'button2', 'bridge']

def instructions(r1, r2):
    """
    """
    def robot1(x,y):
        """
        convert coordinates of robot1 to island
        """
        if x <= 2 and y <= 1:
            return 'r1_home'
        elif x <= 1 and y >= 3:
            return 'r1_near'
        elif x >= 3 and y >= 3:
            return 'r1_far'
        elif x == 1 and y == 2:
            return 'r1_bridge1'
        elif x == 2 and y == 4:
            return 'r1_bridge2'
        else:
            print('error: abstraction is not defined for these coordinates!')

    def robot2(x,y):
        """
        convert coordinates of robot2 to island
        """
        if x <= 2 and y <= 1:
            return 'r2_home'
        elif x <= 1 and y >= 3:
            return 'r2_near'
        elif x >= 3 and y >= 3:
            return 'r2_far'
        elif x == 1 and y == 2:
            return 'r2_bridge1'
        elif x == 2 and y == 4:
            return 'r2_bridge2'
        else:
            print('error: abstraction not defined for these coordinates!')
    x1, y1 = r1
    x2, y2 = r2
    return [robot1(x1,y1), robot2(x2,y2)]
