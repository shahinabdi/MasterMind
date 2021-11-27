import random
import collections

length = 4
guesses = 12

pattern = [random.choice('123456789') for _ in range(length)]
print(pattern)


counted = collections.Counter(pattern)


def game():
    guess = input('Guess: ')
    guess_count = collections.Counter(guess)

    close = sum(min(counted[k], guess_count[k]) for k in counted)
    exact = sum(p == g for p, g in zip(pattern, guess))

    close -= exact
    print('Exact: {}. Close: {}.'.format(exact, close))
    return exact != length


for attempt in range(guesses):
    if not game():
        print("Yes Win!")
        break
    else:
        print('Gusses remaining: ', guesses - 1 - attempt)
else:
    print('Game over. The code was {}'.format(''.join(pattern)))
