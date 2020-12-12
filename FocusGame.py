# Name: Vincent Rastello
# Date: 11-27-20
# Description: This is a program for creating a game of Domination. Follow this link to see a description:
# https://www.youtube.com/watch?v=DVRVQM9lo9E. My data structure will consist of three classes: Player, Board
# and FocusGame. Player and Board will not communicate with each other. FocusGame will communicate with both,
# FocusGame will act as the brain for this data structure.


class Player:
    """This represents the player, class responsibilities include: holding, displaying and adding reserve and
    captured pieces. Has attribute name and color."""

    def __init__(self, name, color):
        """Initializes player with name and color, sets reserved and captured to empty lists."""

        self._color = color
        self._name = name
        self._reserved = []
        self._captured = []

    def get_color(self):
        """returns color"""
        return self._color

    def get_name(self):
        """returns name"""
        return self._name

    def show_reserve_list(self):
        """returns count of pieces in reserve list for player"""
        return len(self._reserved)

    def show_captured_list(self):
        """returns count of opponent pieces captured"""
        return len(self._captured)

    def add_reserve(self, piece):
        """adds reserve piece to reserve list"""
        self._reserved.append(piece)

    def add_capture(self, piece):
        """adds captured piece to captured list"""
        self._captured.append(piece)

    def remove_reserve(self):
        """removes reserved piece, if none returns False"""
        del self._reserved[0]


class Board:
    """Represents the game board, class responsibilities are: setting data structure for board, initializing board
    values, holding, displaying, adding, removing and counting pieces at specified locations."""

    def __init__(self, r, g):
        """Sets up board data structure and initializes starting game pieces, pieces accessed using tuples
        with row and column (a,b)"""
        self._board = [ [ [r], [r], [g], [g], [r], [r] ],
                        [ [g], [g], [r], [r], [g], [g] ],
                        [ [r], [r], [g], [g], [r], [r] ],
                        [ [g], [g], [r], [r], [g], [g] ],
                        [ [r], [r], [g], [g], [r], [r] ],
                        [ [g], [g], [r], [r], [g], [g] ] ]

    def show_list(self, pos):
        """returns list of pieces at position, using tuple to index to position, returns False if invalid position"""
        if 0 <= pos[0] <= 5 and 0 <= pos[1] <= 5:
            return self._board[pos[0]][pos[1]]
        return False

    def add_piece(self, pos, val):
        """adds given piece using method show_pieces to access list at position"""
        self.show_list(pos).append(val)

    def count_pieces(self, pos):
        """returns count of elements in list at given position on board"""
        return len(self.show_list(pos))


class FocusGame:
    """This represents the game, uses composition to utilize classes Board and Player. Responsibilities are:
    moving pieces, validating move, resolving add reserve and captured pieces after move, checking for win condition,
    moving reserved pieces."""

    def __init__(self, player_1, player_2):
        """Initializes game with players as Player objects, board as Board object and turn to None. Parameters are
        name and color of player in a tuple."""
        self._player1 = Player(player_1[0], player_1[1])
        self._player2 = Player(player_2[0], player_2[1])
        self._player_list = [self._player1, self._player2]
        self._turn = None
        self._winner = None
        self._board = Board(self._player1.get_color(), self._player2.get_color())

    def get_turn(self):
        """Returns private data _turn, is color, this is set after first successful move. Any color can go first."""
        return self._turn

    def get_player_from_name(self, player_name):
        """Returns player object from player name."""
        for player in self._player_list:
            if player_name == player.get_name():
                return player

    def show_pieces(self, pos):
        """Returns list from Board object at specified location, uses tuple (row, column) as parameter"""
        return self._board.show_list(pos)

    def show_reserve(self, player_name):
        """Returns reserve list of player, takes player name as parameter."""
        return self.get_player_from_name(player_name).show_reserve_list()

    def show_captured(self, player_name):
        """Returns capture list of player, takes player name as parameter."""
        return self.get_player_from_name(player_name).show_captured_list()

    def valid_location(self, pos1, pos2, num):
        """Validates if pos1 and pos2 are within bounds, validates if move is in four cardinal directions only,
        validates if destination is equal to number of pieces moved."""
        if self.show_pieces(pos1) is False or self.show_pieces(pos2) is False:
            return False
        if self._board.count_pieces(pos1) < num or num <= 0:
            return False
        if pos1[0] == pos2[0] and pos2[1] == pos1[1] - num:
            return True
        if pos1[0] == pos2[0] and pos2[1] == pos1[1] + num:
            return True
        if pos1[1] == pos2[1] and pos2[0] == pos1[0] - num:
            return True
        if pos1[1] == pos2[1] and pos2[0] == pos1[0] + num:
            return True
        return False

    def resolve_move(self, pos2, player_name):
        """parameters: destination position in tuple, and player name, resolves moving pieces to reserved or captured,
        sets turn to next player."""
        player = self.get_player_from_name(player_name)
        if self._board.count_pieces(pos2) > 5:
            num = self._board.count_pieces(pos2) - 5
            for piece in range(num):
                val = self.show_pieces(pos2)[piece]
                if val == player.get_color():
                    player.add_reserve(val)
                else:
                    player.add_capture(val)

            self.show_pieces(pos2)[:] = self.show_pieces(pos2)[num:]

        if self.show_captured(player_name) >= 6:
            self._winner = player_name + " Wins"

        if player is self._player1:
            self._turn = self._player2.get_color()
        else:
            self._turn = self._player1.get_color()

        if self._winner is not None:
            return self._winner
        return "successfully moved"

    def move_piece(self, player_name, pos1, pos2, num):
        """parameters: player name, starting location tuple, ending location tuple, number of pieces moved. Moves
        piece or pieces from starting location to ending location. Validates if valid position, turn, number of
        pieces, top piece is current players, resolves reserved or captured pieces from move, checks win condition
        and sets turn to next player."""

        if self._winner is not None:
            return self._winner
        if not self.valid_location(pos1, pos2, num):
            return False

        player = self.get_player_from_name(player_name)
        source_height = self._board.count_pieces(pos1)

        if self.show_pieces(pos1)[source_height - 1] != player.get_color():
            return False
        if self.get_turn() is not None and self.get_turn() != player.get_color():
            return False

        lower = source_height - num
        for piece in range(lower, source_height):
            val = self.show_pieces(pos1)[piece]
            self._board.add_piece(pos2, val)

        self.show_pieces(pos1)[:] = self.show_pieces(pos1)[:lower]

        return self.resolve_move(pos2, player_name)

    def reserved_move(self, player_name, pos2):
        """parameters are destination location tuple, and player name. Validates destination location then if player
        has reserve pieces. Adds piece to location specified and resolves adding captured pieces, reserve pieces and
        checks win condition."""
        player = self.get_player_from_name(player_name)

        if self._winner is not None:
            return self._winner
        if self.show_pieces(pos2) is False:
            return False
        if self.show_reserve(player_name) == 0:
            return False
        if self.get_turn() is not None and self.get_turn() != player.get_color():
            return False

        player.remove_reserve()
        val = player.get_color()
        self._board.add_piece(pos2, val)
        return self.resolve_move(pos2, player_name)


















