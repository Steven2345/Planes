# just to see them
#   ^        *      ***      *
# *****    * *       *       * *
#   *      ***>    *****    <***
#  ***     * *       v       * *
#            *               *
import random
from services.computer import Computer


class PlacementError(Exception):
    pass


class ShotError(Exception):
    pass


class GameOver(Exception):
    pass


class Service:
    def __init__(self):
        # creating 4 matrices that will store the information about where the planes are and where the players hit
        # could have been 2, but the design choice was to make 4 of them
        # convention: for whom to show - whose is
        self.matrix_user_user = [[0 for i in range(10)] for i in range(10)]
        self.matrix_user_computer = [[-1 for i in range(10)] for i in range(10)]
        self.matrix_computer_user = [[-1 for i in range(10)] for i in range(10)]
        self.matrix_computer_computer = [[0 for i in range(10)] for i in range(10)]

        # initialising the game means initialising the grid of the computer
        self.generate_planes()

        # instantiating Computer class
        self.computer = Computer()

        # initialising counters for game over
        self.planes_user = 3
        self.planes_computer = 3
        self.user_planes_down = []

# not used anymore
#    def doing_planes(self): # send_plane and generate_plane?
#        # as of now, this just puts some planes in the "visible" matrices
#        # at some point, it will gather information from the ui about where to place the planes
#        # plane-placement for computer will be random at some point, but now it is given in code
#
#        self.__place_plane(self.matrix_user_user, 1, 2, "d")
#        self.__place_plane(self.matrix_user_user, 7, 6, "l")
#        self.__place_plane(self.matrix_user_user, 4, 6, "r")
#
#        # self.generate_planes()
#        self.__place_plane(self.matrix_computer_computer, 0, 3, "d")
#        self.__place_plane(self.matrix_computer_computer, 8, 2, "u")
#        self.__place_plane(self.matrix_computer_computer, 3, 9, "l")

    def receive_plane_from_user(self, line, column: int, direct):
        # this is going to be called for at least 3 times, actually, in case the user messes up
        self.__place_plane(self.matrix_user_user, line, column, direct)

    def generate_planes(self):
        for i in range(3):
            ok = True
            while ok:
                try:
                    ok = False
                    self.__place_plane(self.matrix_computer_computer, random.randint(0, 9), random.randint(0, 9), random.choice(["u", "d", "l", "r"]))
                except PlacementError:
                    ok = True

    def __place_plane(self, matrix, lin, col, direction):
        # also should include some validation for the placement of the planes
        """
        ok = True
        while ok:
            try:
                ok = False
                self.place_plane(...)
            except PlacementError:
                ok = True
        """
        # PlacementError could mean out of the grid or overlapping planes
        if direction == "u":
            if lin < 3 or lin > 9 or col < 2 or col > 7:
                raise PlacementError("Plane is outside the grid")
        elif direction == "d":
            if lin < 0 or lin > 6 or col < 2 or col > 7:
                raise PlacementError("Plane is outside the grid")
        elif direction == "l":
            if lin < 2 or lin > 7 or col < 3 or col > 9:
                raise PlacementError("Plane is outside the grid")
        elif direction == "r":
            if lin < 2 or lin > 7 or col < 0 or col > 6:
                raise PlacementError("Plane is outside the grid")

        if direction == "u":
            if matrix[lin][col] != 0 or matrix[lin - 1][col] != 0 or matrix[lin - 2][col] != 0 or matrix[lin - 3][col] != 0 or matrix[lin - 1][col - 2] != 0 or matrix[lin - 1][col - 1] != 0 or matrix[lin - 1][col + 1] != 0 or matrix[lin - 1][col + 2] != 0 or matrix[lin - 3][col - 1] != 0 or matrix[lin - 3][col + 1] != 0:
                raise PlacementError("Plane is overlapping with another")
        elif direction == "d":
            if matrix[lin][col] != 0 or matrix[lin + 1][col] != 0 or matrix[lin + 2][col] != 0 or matrix[lin + 3][col] != 0 or matrix[lin + 1][col - 2] != 0 or matrix[lin + 1][col - 1] != 0 or matrix[lin + 1][col + 1] != 0 or matrix[lin + 1][col + 2] != 0 or matrix[lin + 3][col - 1] != 0 or matrix[lin + 3][col + 1] != 0:
                raise PlacementError("Plane is overlapping with another")
        elif direction == "l":
            if matrix[lin][col] != 0 or matrix[lin][col - 1] != 0 or matrix[lin][col - 2] != 0 or matrix[lin][col - 3] != 0 or matrix[lin - 2][col - 1] != 0 or matrix[lin - 1][col - 1] != 0 or matrix[lin + 1][col - 1] != 0 or matrix[lin + 2][col - 1] != 0 or matrix[lin - 1][col - 3] != 0 or matrix[lin + 1][col - 3] != 0:
                raise PlacementError("Plane is overlapping with another")
        elif direction == "r":
            if matrix[lin][col] != 0 or matrix[lin][col + 1] != 0 or matrix[lin][col + 2] != 0 or matrix[lin][col + 3] != 0 or matrix[lin - 2][col + 1] != 0 or matrix[lin - 1][col + 1] != 0 or matrix[lin + 1][col + 1] != 0 or matrix[lin + 2][col + 1] != 0 or matrix[lin - 1][col + 3] != 0 or matrix[lin + 1][col + 3] != 0:
                raise PlacementError("Plane is overlapping with another")

        # actual laying of the planes
        if direction == "u":
            matrix[lin][col] = "u"
            matrix[lin - 1][col] = matrix[lin - 2][col] = matrix[lin - 3][col] = 1
            matrix[lin - 1][col - 2] = matrix[lin - 1][col - 1] = matrix[lin - 1][col + 1] = matrix[lin - 1][col + 2] = 1
            matrix[lin - 3][col - 1] = matrix[lin - 3][col + 1] = 1
        elif direction == "d":
            matrix[lin][col] = "d"
            matrix[lin + 1][col] = matrix[lin + 2][col] = matrix[lin + 3][col] = 1
            matrix[lin + 1][col - 2] = matrix[lin + 1][col - 1] = matrix[lin + 1][col + 1] = matrix[lin + 1][col + 2] = 1
            matrix[lin + 3][col - 1] = matrix[lin + 3][col + 1] = 1
        elif direction == "l":
            matrix[lin][col] = "l"
            matrix[lin][col - 1] = matrix[lin][col - 2] = matrix[lin][col - 3] = 1
            matrix[lin - 2][col - 1] = matrix[lin - 1][col - 1] = matrix[lin + 1][col - 1] = matrix[lin + 2][col - 1] = 1
            matrix[lin - 1][col - 3] = matrix[lin + 1][col - 3] = 1
        elif direction == "r":
            matrix[lin][col] = "r"
            matrix[lin][col + 1] = matrix[lin][col + 2] = matrix[lin][col + 3] = 1
            matrix[lin - 2][col + 1] = matrix[lin - 1][col + 1] = matrix[lin + 1][col + 1] = matrix[lin + 2][col + 1] = 1
            matrix[lin - 1][col + 3] = matrix[lin + 1][col + 3] = 1

    def shot(self, sender: str, lin, col: int):
        # not counting on the ui for not giving points that were already shot at
        # going to check in here
        #
        # in the matrix of the opponent:
        # -1 - no information
        # 0 - missed shot
        # 1 - hit
        if sender == "user":
            if self.matrix_user_computer[lin][col] == -1:
                self.matrix_user_computer[lin][col] = self.matrix_computer_computer[lin][col]

                message_user = self.__mark_plane_down(self.matrix_user_computer, lin, col)
                if message_user == "Plane down!":
                    self.planes_computer -= 1

                # check game over condition
                if self.planes_computer == 0:
                    raise GameOver("User won!")

                return message_user
            raise ShotError
        elif sender == "computer":
            # computer is smart enough not to shot in the same spot twice
            self.matrix_computer_user[lin][col] = self.matrix_user_user[lin][col]
            message_computer = self.__mark_plane_down(self.matrix_computer_user, lin, col)

            if message_computer == "Plane down!":
                self.planes_user -= 1
                self.user_planes_down.append([lin, col, self.matrix_user_user[lin][col]])

            # check game over condition
            if self.planes_user == 0:
                raise GameOver("Computer won!")

            return message_computer

    def __mark_plane_down(self, matrix, lin, col):
        if matrix[lin][col] == "u":
            matrix[lin][col] = 1
            matrix[lin - 1][col] = matrix[lin - 2][col] = matrix[lin - 3][col] = 1
            matrix[lin - 1][col - 2] = matrix[lin - 1][col - 1] = matrix[lin - 1][col + 1] = matrix[lin - 1][col + 2] = 1
            matrix[lin - 3][col - 1] = matrix[lin - 3][col + 1] = 1
            return "Plane down!"
        elif matrix[lin][col] == "d":
            matrix[lin][col] = 1
            matrix[lin + 1][col] = matrix[lin + 2][col] = matrix[lin + 3][col] = 1
            matrix[lin + 1][col - 2] = matrix[lin + 1][col - 1] = matrix[lin + 1][col + 1] = matrix[lin + 1][col + 2] = 1
            matrix[lin + 3][col - 1] = matrix[lin + 3][col + 1] = 1
            return "Plane down!"
        elif matrix[lin][col] == "l":
            matrix[lin][col] = 1
            matrix[lin][col - 1] = matrix[lin][col - 2] = matrix[lin][col - 3] = 1
            matrix[lin - 2][col - 1] = matrix[lin - 1][col - 1] = matrix[lin + 1][col - 1] = matrix[lin + 2][col - 1] = 1
            matrix[lin - 1][col - 3] = matrix[lin + 1][col - 3] = 1
            return "Plane down!"
        elif matrix[lin][col] == "r":
            matrix[lin][col] = 1
            matrix[lin][col + 1] = matrix[lin][col + 2] = matrix[lin][col + 3] = 1
            matrix[lin - 2][col + 1] = matrix[lin - 1][col + 1] = matrix[lin + 1][col + 1] = matrix[lin + 2][col + 1] = 1
            matrix[lin - 1][col + 3] = matrix[lin + 1][col + 3] = 1
            return "Plane down!"
        elif matrix[lin][col] == 1:
            return "Plane hit!"
        return "Missed!"

    def call_computer_shot(self):
        return self.computer.make_shot(self.matrix_computer_user, self.user_planes_down)


    # def check_hit_down(self, matrix, lin, col):
    #     if matrix[lin][col] == 0:
    #         return -1
    #     elif matrix[lin][col] == 1:
    #         return 1
    #     elif matrix[lin][col] == 2:
    #         return 5


if __name__ == "__main__":
    serv = Service()

    # serv.doing_planes()
    serv.receive_plane_from_user(1, 2, "d")
    serv.receive_plane_from_user(7, 6, "l")
    serv.receive_plane_from_user(4, 6, "r")

    print(serv.shot("user", 8, 0))
    print(serv.shot("user", 7, 0))
    print(serv.shot("user", 8, 2))

    for i in range(10):
        print(serv.matrix_user_user[i])
    print()
    for i in range(10):
        print(serv.matrix_computer_computer[i])
    print()
    for i in range(10):
        print(serv.matrix_user_computer[i])
    print()
    for i in range(10):
        print(serv.matrix_computer_user[i])
