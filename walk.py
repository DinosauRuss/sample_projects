'''
Program to randomly take a number of 'steps'
and plot the results
'''

import matplotlib.pyplot as plt
from random import choice

class RandomWalk():
    '''A class to generate random walks'''

    def __init__(self, steps= 5000):
        self.steps = steps

        # All walks start at (0, 0)
        self.x_values = [0]
        self.y_values = [0]

    def fill_walk(self):
        '''Calculate all the points from the walk'''

        # Take correct number of steps
        while len(self.x_values) < self.steps:
            x_direction = choice([-1, 1])
            x_distance = choice([0, 1, 2, 3, 4])
            x_step = x_distance  * x_direction

            y_direction = choice([-1, 1])
            y_distance = choice([0, 1, 2, 3, 4])
            y_step = y_distance  * y_direction

            # Reject steps which stay in place
            if x_step == 0 and y_step == 0:
                continue

            # Calculate the coordinate of each step
            next_x = self.x_values[-1] + x_step
            next_y = self.y_values[-1] + y_step

            self.x_values.append(next_x)
            self.y_values.append(next_y)


def main_loop():
    try:
        how_many = input('How many steps to take(1,000 - 50,000)\n\
Press enter for default of 25000: ') or 25000

        if int(how_many) < 1000:
            how_many = 1000
            print('Out of range, plotting 1000 steps')
        
        elif int(how_many) > 50000:
            how_many = 50000
            print('Out of range, plotting 50000 steps')

        else:
            print('Plotting {} steps'.format(how_many))
        
        Magoo = RandomWalk(int(how_many))
        Magoo.fill_walk()

        plt.figure(dpi= 128, figsize= (10,6))

        point_nums = list(range(Magoo.steps))
        half = int(Magoo.steps/2)
        plt.scatter(Magoo.x_values, Magoo.y_values, c=point_nums, \
                    s= 1, cmap= plt.cm.coolwarm, edgecolor = 'none')
        plt.scatter(Magoo.x_values[0], Magoo.y_values[0], c= 'lawngreen', s= 40)
        plt.scatter(Magoo.x_values[-1], Magoo.y_values[-1], c= 'red', s= 40)
        plt.scatter(Magoo.x_values[half], Magoo.y_values[half],\
                    c= 'gold', s= 25)

        # Remove axis labels
        plt.axes().get_xaxis().set_visible(False)
        plt.axes().get_yaxis().set_visible(False)

        plt.show()
    except Exception as e:
##        print('Error:', e)
        print('Not a valid number')

if __name__ == '__main__':
    main_loop()



