import numpy as np
import typing
import matplotlib.pyplot as plt
import copy


def func(x_1: float, x_2: float, x_3: float, x_4: float) -> float:
    return x_1 * x_4 * (x_2 + x_3) + x_3


def crossover(
    first_cell: typing.Tuple[float, float, int, int],
    second_cell: typing.Tuple[float, float, int, int],
) -> typing.Tuple[
    typing.Tuple[float, float, int, int], typing.Tuple[float, float, int, int]
]:
    first_crossed_cell = first_cell[0], first_cell[1], second_cell[2], second_cell[3]
    second_crossed_cell = second_cell[0], second_cell[1], first_cell[2], first_cell[3]
    return first_crossed_cell, second_crossed_cell


def check_constraints(
    variables: typing.List[typing.Tuple[int, int, float, float]]
) -> bool:
    const_1 = variables[0] * variables[1] * variables[2] * variables[3] - 25
    const_2 = (
        variables[1] ** 2 + variables[1] ** 2 + variables[2] ** 2 + variables[3] ** 2
    )
    if const_1 > 0 and const_2 > 39.8 and const_2 < 40.2:
        return True
    return False


def mutate(
    cell: typing.Tuple[float, float, int, int]
) -> typing.Tuple[float, float, int, int]:
    PROB_OF_MUT = 0.05
    if np.random.random() < PROB_OF_MUT:
        Done = False
        while not Done:
            print("finding valid params")
            mutated_vals: typing.List[typing.Union[int, float]] = []
            for i in range(len(cell)):
                if i <= 1:
                    done = False
                    while not done:
                        print("getting valid continous vars")
                        mutation_amount = 5 * np.random.random()
                        new_value = cell[i] + float(mutation_amount)
                        if not new_value > 5 and not new_value < 1:
                            done = True
                            mutated_vals.append(new_value)
                else:
                    new_int_value = np.random.choice([1, 2, 3, 4, 5])
                    mutated_vals.append(new_int_value)
            if check_constraints(mutated_vals):
                print("returning mutated values")
                return (
                    mutated_vals[0],
                    mutated_vals[1],
                    mutated_vals[2],
                    mutated_vals[3],
                )
    else:
        print("returning ch")
        return cell


def gen_init_choices():
    done = False
    while not done:
        x_1_2 = 4 * np.random.random_sample(2) - 1
        x_3_4 = np.random.randint(1, 5, size=2)
        variables = [x_1_2[0], x_1_2[1], x_3_4[0], x_3_4[1]]
        if check_constraints(variables):
            return (x_1_2[0], x_1_2[1], x_3_4[0], x_3_4[1])


if __name__ == "__main__":
    generation = []
    SIZE_OF_GEN = 6
    for i in range(SIZE_OF_GEN):
        citizen = gen_init_choices()
        generation.append(citizen)
    counts = []
    best_vals = []

    for i in range(500):
        print(i)
        for j in generation:
            print(j)
        fitness_of_gen = [func(x[0], x[1], x[2], x[3]) for x in generation]
        generation_sorted = [x for _, x in sorted(zip(fitness_of_gen, generation))]

        mid = int(len(generation_sorted) / 2)
        # slice save only the most fit
        preserved_citizens = generation_sorted[:mid]
        # copy reserved citizens
        new_generation = copy.deepcopy(preserved_citizens)
        # saving first and last citizen to add one more child at the end to keep
        # list at 50
        # crossover preserved citizens
        first_cit = preserved_citizens[0]
        last_cit = preserved_citizens[-1]
        for l in range(0, len(preserved_citizens) - 1, 2):
            child_1, child_2 = crossover(
                preserved_citizens[l], preserved_citizens[l + 1]
            )
            new_generation.append(child_1)
            new_generation.append(child_2)
        child_1, child_2 = crossover(first_cit, last_cit)
        new_generation.append(child_1)
        fitness_of_new_generation = [func(x[0], x[1], x[2], x[3]) for x in generation]
        # sorted_func = sorted(fitness_of_new_generation)
        new_gen_sorted = [
            x for _, x in sorted(zip(fitness_of_new_generation, new_generation))
        ]
        best_cit = new_gen_sorted[0]
        mut_gen = []
        for k in range(len(new_gen_sorted)):
            if k >= 1:
                mut_gen.append(mutate(new_gen_sorted[k]))
            else:
                mut_gen.append(new_gen_sorted[k])
        best_val = func(best_cit[0], best_cit[1], best_cit[2], best_cit[3])
        counts.append(i)
        best_vals.append(best_val)
        generation = mut_gen
    print(counts)
    print(best_vals)
    plt.plot(counts, best_vals)
    plt.savefig("Problem_2")
