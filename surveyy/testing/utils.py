from typing import List

def compare_data(correct: dict[str, List[str]], user: dict[str, List[str]]) -> dict[str, List[str]]:
    intersection = {}

    for key in user.keys():
        if key not in correct:
            continue

        if user[key] == correct[key]:
            intersection[key] = correct[key]

    print(f'correct: {correct}')
    print(f'user: {user}')
    print(f'intersection: {intersection}')

    return intersection
