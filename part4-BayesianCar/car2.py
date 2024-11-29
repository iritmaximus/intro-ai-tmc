from random import random

TUPLE_COUNT = 100_000


def calculate_prob(tuples: list, parameters: list[int], n: int = TUPLE_COUNT):
    count = 0
    for entry in tuples:
        is_counted = True
        for index, field in enumerate(entry):
            if parameters[index] == -1:
                continue

            if parameters[index] == field:
                continue
            
            is_counted = False

        if is_counted:
            count += 1

    return count / n


def generate_tuples(parameters: list[int], n: int = TUPLE_COUNT):
    print(parameters)
    tuples = []

    while n>0:
        battery = True if 0.9 > random() else False
        gas = True if 0.95 > random() else False
        if battery:
            radio = True if 0.9 > random() else False
            ignition = True if 0.95 > random() else False

        if not battery:
            radio = True if 0.1 > random() else False
            ignition = True if 0.05 > random() else False

        if gas and ignition:
            starts = True if 0.99 > random() else False
        else: 
            starts = False

        if starts:
            moves = True if 0.99 > random() else False

        if not starts: 
            moves = False

        tuples.append((battery, radio, ignition, gas, starts, moves)) 
        n -= 1

    return tuples



if __name__ == "__main__":
    # P(X | Y, Z, Å) = P(X, Y, Z, Å) / P(Y, Z, Å)
    parameters1 = [-1, 1, -1, 1, 0, -1] # P(R, G, -S)
    parameters1d = [1, 1, -1, 1, 0, -1] # P(B, R, G, -S)

    parameters2 = [-1, 1, 1, 1, -1, -1] # P(R, I, G)
    parameters2d = [-1, 1, 1, 1, 1, -1] # P(S, R, I, G)

    parameters3 = [-1, 0, 1, 1, -1, -1] # P(-R, I, G)
    parameters3d = [-1, 0, 1, 1, -1, 1] # P(S, -R, I, G)

    tuples1 = generate_tuples(parameters1)
    tuples1d = generate_tuples(parameters1d)

    tuples2 = generate_tuples(parameters2)
    tuples2d = generate_tuples(parameters2d)

    tuples3 = generate_tuples(parameters3)
    tuples3d = generate_tuples(parameters3d)

    probs1 = calculate_prob(tuples1, parameters1)
    probs1d = calculate_prob(tuples1d, parameters1d)

    probs2 = calculate_prob(tuples2, parameters2)
    probs2d = calculate_prob(tuples2d, parameters2d)

    probs3 = calculate_prob(tuples3, parameters3)
    probs3d = calculate_prob(tuples3d, parameters3d)

    print(probs1d/probs1)
    print(probs2d/probs2)
    print(probs3d/probs3)
