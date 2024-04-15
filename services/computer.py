import copy


class LocationError(Exception):
    pass


class ConditionError(Exception):
    pass


def order_values(llist):
    return llist[1]


class Computer:
    def __init__(self):#, matrix):
        pass
        # some initialisation for auxiliary data structures

        # we have 3 matrices: the unchanged matrix_of_opponent, the visible_matrix where we try to position planes and that
        # has to be restored after... does it have to be restored? I don't think so, 'cause we already save the necessary
        # information in the 2 lists, and we don't care if we overwrite it for this one shot. So, only 2 matrices.
        ## self.matrix_of_opponent = matrix
        ## self.visible_matrix = copy.deepcopy(matrix)  # the matrix in which we test if the plane(s) can be positioned
        ## self.values_matrix = [[0 for i in range(10)] for i in range(10)]  # the matrix in which we increment

        ## self.hit = []  # list with the hit spots in visible
        ## self.missed = []  # list with the missed spots in visible

        # at some point, when valid configurations are found, a list of the spots that have a value in values and sort that list

    def make_shot(self, matrix_of_opponent, planes_down):
        # this is going to be called from the service for each turn of the computer
        # 3 functions: search_one_plane, search_two_planes, search_three_planes
        #       search_one_plane called first, then search_two_planes, which uses search_one_plane, then search_three_planes,
        #       which uses search_two_planes
        self.visible_matrix = copy.deepcopy(matrix_of_opponent)  # the matrix in which we test if the plane(s) can be positioned
        self.values_matrix = [[0 for i in range(10)] for i in range(10)]  # the matrix in which we increment
        self.number_of_configurations = 0

        # mark the destroyed planes as misses to enable the program to keep going for the others
        for plane in planes_down:
            self.__remove_plane(plane[0], plane[1], plane[2])

        # create lists with the hit points and the missed points
        self.hit = []
        self.missed = []
        for i in range(10):
            for j in range(10):
                if self.visible_matrix[i][j] == 1:
                    self.hit.append([i, j])
                elif self.visible_matrix[i][j] == 0:
                    self.missed.append([i, j])

        # what we do now is to place a plane in every possible way across the board (i.e. 400 ways) and check:
        #   - if it lies outside the grid
        #   - (*)if it doesn't overlap with other planes
        #   - if it includes all(*) hit spots
        #   - if it doesn't include any missed spots
        # (*) only for more planes
        #
        # remember the location of the head of the first plane placed, so that we know the position if the
        # highest value in values_matrix is 1

        self.head_coord = []
        self.__search_one_plane(0)
        if len(self.head_coord) == 0:
            self.__search_two_planes(0)
        if len(self.head_coord) == 0:
            self.__search_three_planes()

        # actually doing the shot:
        # going through values_matrix and saving non-zero values in a list
        list_of_values = []
        for i in range(10):
            for j in range(10):
                if self.values_matrix[i][j] != 0:
                    list_of_values.append([[i, j], self.values_matrix[i][j]])

        # sorting in descending order of the values and...
        list_of_values.sort(reverse=True, key=order_values)

        # ...choosing the closest one to the half of total number of planes
        k = 0
        while k < len(list_of_values) and list_of_values[k][1] > self.number_of_configurations / 2:
            k += 1

        # make a check that the chosen point was not already shot at; shouldn't be, but you never know
        #

        # for debugging purposes
        ## print(self.number_of_configurations)
        ## print(list_of_values)
        ## for i in range(10):
        ##     print(self.values_matrix[i])
        ## if k < len(list_of_values):
        ##     print(list_of_values[k])

        # check if it is the case to return the values in head_coord
        if list_of_values[0][1] == 1:
            return self.head_coord[0], self.head_coord[1]
        return list_of_values[k][0][0], list_of_values[k][0][1]


    def __search_one_plane(self, line: int):
        for i in range(line, 10):
            for j in range(10):
                for direct in ['u', 'r', 'd', 'l']:
                    try:
                        self.__place_plane(i, j, direct)  # this places the plane in visible_matrix

                        for spot in self.missed:
                            if self.visible_matrix[spot[0]][spot[1]] == "P":  # from Plane
                                raise ConditionError

                        for spot in self.hit:
                            if self.visible_matrix[spot[0]][spot[1]] != "P":
                                raise ConditionError

                        # changing the head coordinates for the first plane found if the plane is not supposed to
                        #    have already been shot down
                        # in case it should, we should start looking for one more plane
                        # interestingly enough, this added condition was never reached during testing, as it would
                        #    have been easily noticed since it would get the algorithm stuck in an infinite loop
                        if len(self.head_coord) == 0:
                            if [i, j] not in self.hit:
                                self.head_coord = [i, j]

                        # alter values_matrix for successful placing
                        for ii in range(10):
                            for jj in range(10):
                                if self.visible_matrix[ii][jj] == "P":
                                    self.values_matrix[ii][jj] += 1

                        # increment number of possible combinations
                        self.number_of_configurations += 1

                        # for debugging purposes
                        ## print(i, j, direct)
                        ## for I in range(10):
                        ##     print(self.visible_matrix[I])

                        # take the plane out of discussion for next iteration
                        self.__remove_plane(i, j, direct)
                    except LocationError:
                        pass
                    except ConditionError:
                        self.__remove_plane(i, j, direct)

    def __search_two_planes(self, line: int):
        for i in range(line, 10):
            for j in range(10):
                for direct in ['u', 'r', 'd', 'l']:
                    try:
                        self.__place_plane(i, j, direct)  # this places the plane in visible

                        for spot in self.missed:
                            if self.visible_matrix[spot[0]][spot[1]] == "P":  # from Plane
                                raise ConditionError

                        # check that at least one hit is in the plane and at least one isn't
                        hits_in = []
                        hits_out = []
                        for spot in self.hit:
                            if self.visible_matrix[spot[0]][spot[1]] != "P":
                                hits_out.append(spot)
                            else:
                                hits_in.append(spot)
                        if len(hits_in) == 0 or len(hits_out) == 0:
                            raise ConditionError

                        # take the spot that are occupied by a possible plane out of the list
                        for spot_removed in hits_in:
                            self.hit.remove(spot_removed)

                        # start searching with the last plane
                        self.__search_one_plane(i)

                        # put the spots that were taken out back in
                        for spot_removed in hits_in:
                            self.hit.append(spot_removed)

                        # # alter values_matrix for successful placing
                        # for ii in range(10):
                        #     for jj in range(10):
                        #         if self.visible_matrix[ii][jj] == "P":
                        #             self.values_matrix[ii][jj] += 1

                        # take the plane out of discussion for next iteration
                        self.__remove_plane(i, j, direct)
                    except LocationError:
                        pass
                    except ConditionError:
                        self.__remove_plane(i, j, direct)

    def __search_three_planes(self):
        for i in range(10):
            for j in range(10):
                for direct in ['u', 'r', 'd', 'l']:
                    try:
                        self.__place_plane(i, j, direct)  # this places the plane in visible

                        for spot in self.missed:
                            if self.visible_matrix[spot[0]][spot[1]] == "P":  # from Plane
                                raise ConditionError

                        # check that at least one hit is in the plane and at least one isn't
                        hits_in = []
                        hits_out = []
                        for spot in self.hit:
                            if self.visible_matrix[spot[0]][spot[1]] != "P":
                                hits_out.append(spot)
                            else:
                                hits_in.append(spot)
                        if len(hits_in) == 0 or len(hits_out) == 0:
                            raise ConditionError

                        # take the spot that are occupied by a possible plane out of the list
                        for spot_removed in hits_in:
                            self.hit.remove(spot_removed)

                        # start searching with the second plane
                        self.__search_two_planes(i)

                        # put the spots that were taken out back in
                        for spot_removed in hits_in:
                            self.hit.append(spot_removed)

                        # # alter values_matrix for successful placing
                        # for ii in range(10):
                        #     for jj in range(10):
                        #         if self.visible_matrix[ii][jj] == "P":
                        #             self.values_matrix[ii][jj] += 1

                        # take the plane out of discussion for next iteration
                        self.__remove_plane(i, j, direct)
                    except LocationError:
                        pass
                    except ConditionError:
                        self.__remove_plane(i, j, direct)

    def __place_plane(self, lin, col: int, direction: str):
        if direction == "u":
            if lin < 3 or lin > 9 or col < 2 or col > 7:
                raise LocationError
        elif direction == "d":
            if lin < 0 or lin > 6 or col < 2 or col > 7:
                raise LocationError
        elif direction == "l":
            if lin < 2 or lin > 7 or col < 3 or col > 9:
                raise LocationError
        elif direction == "r":
            if lin < 2 or lin > 7 or col < 0 or col > 6:
                raise LocationError

        if direction == "u":
            if self.visible_matrix[lin][col] == 'P' or self.visible_matrix[lin - 1][col] == 'P' or self.visible_matrix[lin - 2][col] == 'P' or self.visible_matrix[lin - 3][col] == 'P' or self.visible_matrix[lin - 1][col - 2] == 'P' or self.visible_matrix[lin - 1][col - 1] == 'P' or self.visible_matrix[lin - 1][col + 1] == 'P' or self.visible_matrix[lin - 1][col + 2] == 'P' or self.visible_matrix[lin - 3][col - 1] == 'P' or self.visible_matrix[lin - 3][col + 1] == 'P':
                raise LocationError
        elif direction == "d":
            if self.visible_matrix[lin][col] == 'P' or self.visible_matrix[lin + 1][col] == 'P' or self.visible_matrix[lin + 2][col] == 'P' or self.visible_matrix[lin + 3][col] == 'P' or self.visible_matrix[lin + 1][col - 2] == 'P' or self.visible_matrix[lin + 1][col - 1] == 'P' or self.visible_matrix[lin + 1][col + 1] == 'P' or self.visible_matrix[lin + 1][col + 2] == 'P' or self.visible_matrix[lin + 3][col - 1] == 'P' or self.visible_matrix[lin + 3][col + 1] == 'P':
                raise LocationError
        elif direction == "l":
            if self.visible_matrix[lin][col] == 'P' or self.visible_matrix[lin][col - 1] == 'P' or self.visible_matrix[lin][col - 2] == 'P' or self.visible_matrix[lin][col - 3] == 'P' or self.visible_matrix[lin - 2][col - 1] == 'P' or self.visible_matrix[lin - 1][col - 1] == 'P' or self.visible_matrix[lin + 1][col - 1] == 'P' or self.visible_matrix[lin + 2][col - 1] == 'P' or self.visible_matrix[lin - 1][col - 3] == 'P' or self.visible_matrix[lin + 1][col - 3] == 'P':
                raise LocationError
        elif direction == "r":
            if self.visible_matrix[lin][col] == 'P' or self.visible_matrix[lin][col + 1] == 'P' or self.visible_matrix[lin][col + 2] == 'P' or self.visible_matrix[lin][col + 3] == 'P' or self.visible_matrix[lin - 2][col + 1] == 'P' or self.visible_matrix[lin - 1][col + 1] == 'P' or self.visible_matrix[lin + 1][col + 1] == 'P' or self.visible_matrix[lin + 2][col + 1] == 'P' or self.visible_matrix[lin - 1][col + 3] == 'P' or self.visible_matrix[lin + 1][col + 3] == 'P':
                raise LocationError

        if direction == "u":  # 'P' from Plane
            self.visible_matrix[lin][col] = 'P'
            self.visible_matrix[lin - 1][col] = self.visible_matrix[lin - 2][col] = self.visible_matrix[lin - 3][col] = 'P'
            self.visible_matrix[lin - 1][col - 2] = self.visible_matrix[lin - 1][col - 1] = self.visible_matrix[lin - 1][col + 1] = self.visible_matrix[lin - 1][col + 2] = 'P'
            self.visible_matrix[lin - 3][col - 1] = self.visible_matrix[lin - 3][col + 1] = 'P'
        elif direction == "d":
            self.visible_matrix[lin][col] = 'P'
            self.visible_matrix[lin + 1][col] = self.visible_matrix[lin + 2][col] = self.visible_matrix[lin + 3][col] = 'P'
            self.visible_matrix[lin + 1][col - 2] = self.visible_matrix[lin + 1][col - 1] = self.visible_matrix[lin + 1][col + 1] = self.visible_matrix[lin + 1][col + 2] = 'P'
            self.visible_matrix[lin + 3][col - 1] = self.visible_matrix[lin + 3][col + 1] = 'P'
        elif direction == "l":
            self.visible_matrix[lin][col] = 'P'
            self.visible_matrix[lin][col - 1] = self.visible_matrix[lin][col - 2] = self.visible_matrix[lin][col - 3] = 'P'
            self.visible_matrix[lin - 2][col - 1] = self.visible_matrix[lin - 1][col - 1] = self.visible_matrix[lin + 1][col - 1] = self.visible_matrix[lin + 2][col - 1] = 'P'
            self.visible_matrix[lin - 1][col - 3] = self.visible_matrix[lin + 1][col - 3] = 'P'
        elif direction == "r":
            self.visible_matrix[lin][col] = 'P'
            self.visible_matrix[lin][col + 1] = self.visible_matrix[lin][col + 2] = self.visible_matrix[lin][col + 3] = 'P'
            self.visible_matrix[lin - 2][col + 1] = self.visible_matrix[lin - 1][col + 1] = self.visible_matrix[lin + 1][col + 1] = self.visible_matrix[lin + 2][col + 1] = 'P'
            self.visible_matrix[lin - 1][col + 3] = self.visible_matrix[lin + 1][col + 3] = 'P'

    def __remove_plane(self, lin, col: int, direction: str):
        if direction == "u":
            self.visible_matrix[lin][col] = 0
            self.visible_matrix[lin - 1][col] = self.visible_matrix[lin - 2][col] = self.visible_matrix[lin - 3][col] = 0
            self.visible_matrix[lin - 1][col - 2] = self.visible_matrix[lin - 1][col - 1] = self.visible_matrix[lin - 1][col + 1] = self.visible_matrix[lin - 1][col + 2] = 0
            self.visible_matrix[lin - 3][col - 1] = self.visible_matrix[lin - 3][col + 1] = 0
        elif direction == "d":
            self.visible_matrix[lin][col] = 0
            self.visible_matrix[lin + 1][col] = self.visible_matrix[lin + 2][col] = self.visible_matrix[lin + 3][col] = 0
            self.visible_matrix[lin + 1][col - 2] = self.visible_matrix[lin + 1][col - 1] = self.visible_matrix[lin + 1][col + 1] = self.visible_matrix[lin + 1][col + 2] = 0
            self.visible_matrix[lin + 3][col - 1] = self.visible_matrix[lin + 3][col + 1] = 0
        elif direction == "l":
            self.visible_matrix[lin][col] = 0
            self.visible_matrix[lin][col - 1] = self.visible_matrix[lin][col - 2] = self.visible_matrix[lin][col - 3] = 0
            self.visible_matrix[lin - 2][col - 1] = self.visible_matrix[lin - 1][col - 1] = self.visible_matrix[lin + 1][col - 1] = self.visible_matrix[lin + 2][col - 1] = 0
            self.visible_matrix[lin - 1][col - 3] = self.visible_matrix[lin + 1][col - 3] = 0
        elif direction == "r":
            self.visible_matrix[lin][col] = 0
            self.visible_matrix[lin][col + 1] = self.visible_matrix[lin][col + 2] = self.visible_matrix[lin][col + 3] = 0
            self.visible_matrix[lin - 2][col + 1] = self.visible_matrix[lin - 1][col + 1] = self.visible_matrix[lin + 1][col + 1] = self.visible_matrix[lin + 2][col + 1] = 0
            self.visible_matrix[lin - 1][col + 3] = self.visible_matrix[lin + 1][col + 3] = 0
