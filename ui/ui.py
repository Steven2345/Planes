from services.service import Service, PlacementError, ShotError, GameOver
import time
from os import system


class UI:
    def __init__(self):
        while True:
            again = self.run_game()
            if not again:
                break

    def run_game(self):
        # ui would not instantiate Service upon init, but rather in a start method, so that with each "play again"
        # the service would be reinitialised
        self.services = Service()

        system("cls")

        # initialise game
        print("\n"
              "In the beginning, the user inputs the position and orientation of the planes.\n"
              "The 3 planes should not overlap or lie outside the grid.\n"
              "Instructions for the placement of planes should look like 'C 5 left'.\n"
              "Once the game begins, the user will introduce the coordinates of the targets in the form 'E 8'.\n"
              "If necessary, the game can be stopped at any point using the instruction 'abort'.")
        input("Press any key to continue...")
        abort = False
        for i in range(3):
            system("cls")
        
            if abort:
                break
            ok = True
            while ok:
                self._print_user_matrices()
                try:
                    ok = False
                    info = input("\nGive coordinates and direction (expected format: C 5 left): ")
                    if info == "abort":
                        abort = True
                        break

                    info = info.split()

                    if len(info) != 3:
                        raise ZeroDivisionError("Invalid input")

                    info[1] = int(info[1])
                    info[0] = info[0].upper()

                    if info[0] not in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
                        raise ZeroDivisionError("First coordinate is invalid")
                    if info[1] not in range(1, 11):
                        raise ZeroDivisionError("Second coordinate is invalid")
                    if info[2] not in ["up", "down", "left", "right"]:
                        raise ZeroDivisionError("Direction is invalid")

                    self.services.receive_plane_from_user(ord(info[0]) - ord('A'), info[1] - 1, info[2][0])
                except PlacementError as err:
                    ok = True
                    print(err)
                except ValueError:
                    ok = True
                    print("Second coordinate is invalid")
                except ZeroDivisionError as err:
                    ok = True
                    print(err)

        if abort:  # game was aborted during initialisation
            while True:
                print('\n'
                      '1. Try again\n'
                      '0. Exit')
                option = input("> ")
                if option == "1":
                    value = True
                    break
                elif option == "0":
                    value = False
                    break
                else:
                    print("Invalid option selected")
        else:
            # play game
            system("cls")
            
            while True:
                self._print_user_matrices()
                try:
                    # user makes move
                    target = input("\nChoose target: ")
                    system("cls")
                    
                    if target == "abort":
                        break
                    target = target.split()

                    if len(target) != 2:
                        raise ZeroDivisionError("Invalid coordinates")

                    target[0] = target[0].upper()
                    target[1] = int(target[1])

                    if target[0] not in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
                        raise ZeroDivisionError("First coordinate is invalid")
                    if target[1] not in range(1, 11):
                        raise ZeroDivisionError("Second coordinate is invalid")

                    print(self.services.shot("user", ord(target[0]) - ord('A'), target[1] - 1) + "\n")

                    self._print_user_matrices()
                    print("\n\nTurn of the computer:")
                    time.sleep(2)
                    
                    system("cls")

                    # computer makes move
                    l, c = self.services.call_computer_shot()
                    print(chr(l + ord('A')), c + 1)
                    print(self.services.shot("computer", l, c))

                    # game over condition
                except ZeroDivisionError as err:
                    print(err)
                except ShotError:
                    print("Target has already been shot at!")
                except GameOver as message:
                    self._print_user_matrices()
                    print("\n" + str(message))
                    input("Press any key...")
                    break

            """
            ## testing
            ## c 5 left
            ## g 1 right
            ## e 7 down
            ## e 5
            ## f 6
            ## !f 4
            ## f 5
            ## e 4
            ## g 4
            ## f 3
            ## f 7
            while True:
                self._print_user_matrices()

                mat = self.services.computer.make_shot(self.services.matrix_computer_user)
                for i in range(10):
                    print(mat[i])

                try:
                    # user makes move
                    target = input("\nChoose target: ")
                    if target == "abort":
                        break
                    target = target.split()

                    if len(target) != 2:
                        raise ZeroDivisionError("Invalid coordinates")

                    target[0] = target[0].upper()
                    target[1] = int(target[1])

                    if target[0] not in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
                        raise ZeroDivisionError("First coordinate is invalid")
                    if target[1] not in range(1, 11):
                        raise ZeroDivisionError("Second coordinate is invalid")

                    print(self.services.shot("computer", ord(target[0]) - ord('A'), target[1] - 1))

                    # game over condition
                except ZeroDivisionError as err:
                    print(err)
                except ShotError:
                    print("Target has already been shot at!")
            """


            # game over menu
            while True:
                print('\n'
                      '1. Play again\n'
                      '0. Exit')
                option = input("> ")
                if option == "1":
                    value = True
                    break
                elif option == "0":
                    value = False
                    break
                else:
                    print("Invalid option selected")

        del self.services # necessary or not??
        return value

    def _print_user_matrices(self):
        # services = Service()

        # self.services.receive_plane_from_user(1, 2, "d")
        # self.services.receive_plane_from_user(7, 6, "l")
        # self.services.receive_plane_from_user(4, 6, "r")

        string = "\n                      Your grid                                                      Opponent's grid"
        print(string)

        string = "    "  # first matrix
        for i in range(10):
            string = string + "|" + " " + str(i + 1) + "  "
        string += "          "  # second matrix
        string += "    "
        for i in range(10):
            string = string + "|" + " " + str(i + 1) + "  "

        print(string)
        for i in range(10):
            string = ""  # first matrix
            for j in range(11):
                string += "----+"
            string += "          "  # second matrix
            for j in range(11):
                string += "----+"
            print(string)

            string = "  " + chr(ord('A') + i) + " "  # first matrix
            for j in range(10):
                if self.services.matrix_user_user[i][j] != 0:  # it's a plane
                    if self.services.matrix_computer_user[i][j] == 1:  # plane hit
                        string += "| XX "
                    else:  # plane unscathed
                        string += "|oooo"
                else:  # outside any plane
                    if self.services.matrix_computer_user[i][j] == 0:  # missed hit
                        string += "| .. "
                    else:
                        string += "|    "
            string += " "

            string += "          "  #  second matrix
            string += "  " + chr(ord('A') + i) + " "
            for j in range(10):
                if self.services.matrix_user_computer[i][j] == -1:
                    string += "|    "
                elif self.services.matrix_user_computer[i][j] == 1:
                    string += "|XXXX"
                elif self.services.matrix_user_computer[i][j] == 0:
                    string += "| .. "

            print(string)


        # string = "   "
        # for i in range(10):
        #     string = string + " " + str(i + 1) + " "
        # print(string)
        # for i in range(10):
        #     string = " " + chr(ord('A') + i) + " "
        #     for j in range(10):
        #         if services.matrix_user_user[i][j] != 0:
        #             string += "|||"
        #         else:
        #             string += "   "
        #     print(string)


if __name__ == "__main__":
    ui = UI()
