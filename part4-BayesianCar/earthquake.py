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
        burglary_day = True if 1/365 > random() else False
        earthquake_day = True if 1/111 > random() else False

        if burglary_day and earthquake_day:
            alarm = True if 0.97 > random() else False
        elif not burglary_day and not earthquake_day:
            alarm = True if 0.0095 > random() else False
        else:
            if burglary_day:
                alarm = True if 0.92 > random() else False
            if earthquake_day:
                alarm = True if 0.82 > random() else False


        tuples.append((burglary_day, earthquake_day, alarm)) 
        n -= 1

    return tuples



if __name__ == "__main__":
    # P(X | Y, Z, Å) = P(X, Y, Z, Å) / P(Y, Z, Å)
    # P(A | B)
    parameters1 = [-1, -1, 1] # P(A)
    parameters1d = [1, -1, 1] # P(A, B)

    # P(B | A, E)
    parameters2 = [-1, 1, 1] # P(A, E)
    parameters2d = [1, 1, 1] # P(B, A, E)

    tuples1 = generate_tuples(parameters1)
    tuples1d = generate_tuples(parameters1d)

    tuples2 = generate_tuples(parameters2)
    tuples2d = generate_tuples(parameters2d)

    probs1 = calculate_prob(tuples1, parameters1)
    probs1d = calculate_prob(tuples1d, parameters1d)

    probs2 = calculate_prob(tuples2, parameters2)
    probs2d = calculate_prob(tuples2d, parameters2d)

    print(probs1d/probs1)
    print(probs2d/probs2)
