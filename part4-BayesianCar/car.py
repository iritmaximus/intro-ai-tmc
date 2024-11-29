from random import random

TUPLE_COUNT = 100_000


def generate_probs_from_car(parameters: list[int]):
    parameters_parsed: list[bool] = []
    for x in parameters:
        if x == -1:
            parameters_parsed.append(True)
        elif x == 1:
            parameters_parsed.append(True)
        else:
            parameters_parsed.append(False)

    battery = parameters_parsed[0]
    radio = parameters_parsed[1]
    ignition = parameters_parsed[2]
    gas_par = parameters_parsed[3]
    starts = parameters_parsed[4]
    moves = parameters_parsed[5]


    bat = gas = rad = ign = mov = sta = 0.0
    (bat := 0.9) if battery else (bat := 0.1)
    (gas := 0.95) if gas_par else (gas := 0.05)

    if battery and radio:
        rad = 0.9
    elif not battery and not radio:
        rad = 1.0
    elif battery or radio:
        (rad := 0.1) if battery else (rad := 0.0)

    if battery and ignition:
        ign = 0.95
    elif not battery and not ignition:
        ign = 1.0
    elif battery or ignition:
        (ign := 0.05) if battery else (ign := 0.0)

    if starts and moves:
        mov = 0.99
    elif not starts and not moves:
        mov = 1.0
    elif starts or ignition:
        (mov := 0.01) if starts else (mov := 0.99)

    if starts and not (ignition and gas_par):
        sta = 1.0
    elif not starts and not (ignition and gas_par):
        sta = 0.0
    elif ignition and gas_par:
        (sta := 0.99) if starts else (sta := 0.01)

    return { "battery": bat, "radio": rad, "ignition": ign, "gas": gas, "starts": sta, "moves": mov }


def generate_tuples_from_probs(probs: dict, n: int):
    tuples = []

    while n>0:
        entry = []
        for key in probs.keys():
            random_val = random()
            entry.append(True) if probs[key] > random_val else entry.append(False)
        tuples.append(entry)
        n -= 1

    return tuples


def count_fiels_from_tuples(tuples: list[list[bool]], fields: list[int]):
    """
    fields:
    -1 means doesn't matter
    0 means False
    1 means True
    """
    count_positive = 0
    for entry in tuples:
        is_positive = True
        for entry_field, field in zip(entry, fields):
            if field == -1:
                continue

            (field := True) if field == 1 else (field := False)

            if entry_field != field:
                is_positive = False
                continue


        if is_positive:
            count_positive += 1

    return count_positive / TUPLE_COUNT


if __name__ == "__main__":
    parameters1 = [-1, 1, -1, 1, 0, -1]
    parameters2 = [-1, 1, 1, 1, -1, -1]
    parameters3 = [-1, 0, 1, 1, -1, -1]
    probabilities1 = generate_probs_from_car(parameters1)
    probabilities2 = generate_probs_from_car(parameters2)
    probabilities3 = generate_probs_from_car(parameters3)
    print(parameters1, probabilities1)
    print(parameters2, probabilities2)
    print(parameters3, probabilities3)

    tuples1 = generate_tuples_from_probs(probabilities1, TUPLE_COUNT)
    #print(tuples1)
    #print()
    tuples2 = generate_tuples_from_probs(probabilities2, TUPLE_COUNT)
    #print(tuples2)
    #print()
    tuples3 = generate_tuples_from_probs(probabilities3, TUPLE_COUNT)
    #print(tuples3)

    print(count_fiels_from_tuples(tuples1, parameters1))
    print(count_fiels_from_tuples(tuples2, parameters2))
    print(count_fiels_from_tuples(tuples3, parameters3))

    # P(B | R,G,¬S) => -1, 1, -1, -1, 0, -1
    # P(S | R,I,G)  => -1, 1, 1, 1, -1, -1
    # P(S | ¬R,I,G) => -1, 0, 1, 1, -1, -1
