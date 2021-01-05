import csv


def collect_rating(inp_string: str):
    """
    Auxiliary function ofr retrieving numerical data
    from a string containing player's rating.
    :param inp_string:
    :return: int
    """
    my_digits = list()
    for char in inp_string:
        if char.isdigit():
            my_digits.append(char)
    return int("".join(my_digits))


def collect_result(inp_string: str):
    """
    Auxiliary function for retrieving the result of a game, i.e.
    0.5 - 0.5: draw;
    0 - 1: black won;
    1 - 0; white won;
    :param inp_string: str
    :return: list
    """
    my_tuple = list()
    if "result" in inp_string.lower():
        if "1/2" in inp_string:
            return [0.5, 0.5]
        for char in inp_string:
            if char.isdigit():
                my_tuple.append(int(char))
        return my_tuple


def collect_castling_mate_data(inp_string: str):
    """
    Auxiliary function for retrieving castling data from a given string,
    line from the .pgn file containing chess game data.
    :param inp_string: str
    :return: int
    """
    my_data = list()
    if "checkmated" in inp_string:
        my_data.append(1)
        my_data.append(0) # game was not ended on time
        my_data.append(0)
    elif "time" in inp_string:
        my_data.append(0)
        my_data.append(1)
        my_data.append(0)
    elif "resigns" in inp_string:
        my_data.append(0)
        my_data.append(0)
        my_data.append(1)
    else:
        for _ in range(3):  # case when game is not victorious for either side - draw
            my_data.append(0)

    if " O-O " in inp_string and " O-O-O " in inp_string:
        my_data.append(1)
        my_data.append(0)
    else:
        my_data.append(0)
        my_data.append(1)
    return my_data


def read_pgn_file(inp_file):
    """
    Reads the input .pgn file, which contains data
    on chess games with given ratings,
    :param inp_file: string
    :return:
    """
    my_pgn_file = open(inp_file).readlines()
    with open('chess_games.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["White rating", "Black rating",
                         "White result", "Black result", "Victory by checkmate", "Victory by time",
                         "Victory by resignation", "Opposite side castling", "Other development"])
        i = 0
        while i < len(my_pgn_file):
            try:
                result = collect_result(my_pgn_file[i + 17])
                rating_list = [collect_rating(my_pgn_file[i + 5]), collect_rating(my_pgn_file[i + 6])]
                game_data_list = collect_castling_mate_data(my_pgn_file[i + 19])
                line_data = rating_list + result + game_data_list
                writer.writerow(line_data)
                i += 1
            except (TypeError, ValueError) as e:
                while i < len(my_pgn_file) and not my_pgn_file[i].startswith("[Event"):
                    i += 1
            except IndexError:
                break


if __name__ == "__main__":
    read_pgn_file("datasets/ficsgamesdb_202001_blitz2000_nomovetimes_177584.pgn")
