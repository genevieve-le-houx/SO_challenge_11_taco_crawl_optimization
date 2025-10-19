import csv
import itertools
import math
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple

from dataclasses_json import dataclass_json, config



@dataclass_json
@dataclass
class TacoSpot:
    number: int = field(metadata=config(field_name="TacoSpot"))
    x: int
    y: int
    tastiness: int = field(metadata=config(field_name="Tastiness"))


starting_spot = TacoSpot(0, 0, 0, 0)


def get_taco_spots(filepath: Path) -> List[TacoSpot]:
    data: List[TacoSpot] = []

    with open(filepath, "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            data.append(TacoSpot.from_dict(line))

    return data


def get_distance_between_spots(spot1: TacoSpot, spot2: TacoSpot) -> float:
    return math.sqrt((spot1.x - spot2.x)**2 + (spot1.y - spot2.y)**2)


def get_permutation_score(permutation: Tuple[TacoSpot, ...]) -> Tuple[float, int, float]:
    total_tastiness = sum(x.tastiness for x in permutation)

    # One start at (0, 0) so add this distance first
    total_distance = get_distance_between_spots(permutation[0], starting_spot)

    # Add the distance of the others
    for i, taco_spot in enumerate(permutation[1:], 1):
        total_distance += get_distance_between_spots(taco_spot, permutation[i - 1])

    return total_tastiness / total_distance, total_tastiness, total_distance


def get_best_permutation(permutations: List[Tuple[TacoSpot, ...]]) -> Tuple[Tuple[TacoSpot, ...], float, int, float]:
    scores, tastiness, distance = zip(*map(get_permutation_score, permutations))

    max_score_index = scores.index(max(scores))

    return (
        permutations[max_score_index], scores[max_score_index], tastiness[max_score_index],
        distance[max_score_index]
    )


def main():
    tic = time.time()
    data = get_taco_spots(Path("tacos_data.csv"))

    permutations = list(itertools.permutations(data, 8))
    best_routing, max_score, tastiness, distance = get_best_permutation(permutations)

    print(f"Best routing: {[x.number for x in best_routing]}")
    print(f"Tastiness: {tastiness}")
    print(f"Total distance: {distance}")
    print(f"Tastiness per distance: {max_score}")

    tac = time.time()

    print(f"Got results in {tac - tic} seconds")


if __name__ == '__main__':
    main()