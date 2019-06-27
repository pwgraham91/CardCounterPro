import collections
from typing import List


def generate_initial_deck() -> List[int]:
    cards: List[int] = []
    for card in range(1, 11):
        for suit in range(4):
            cards.append(card)
    cards += [10] * 12
    return cards


def get_user_possible_outcomes(remaining_cards, user_cards):
    user_outcomes = {}
    card_outcomes = {}
    for card in remaining_cards:
        if card_outcomes.get(card):
            if user_outcomes.get(card_outcomes[card]):
                user_outcomes[card_outcomes[card]] += 1
            else:
                user_outcomes[card_outcomes[card]] = 1
        else:
            score = get_score(user_cards + [card])
            if score >= 22:
                score = 22
            card_outcomes[card] = score
            if user_outcomes.get(score):
                user_outcomes[score] += 1
            else:
                user_outcomes[score] = 1

    return user_outcomes


def determine_dealer_outcomes(remaining_cards, dealer_cards, dealer_outcomes):
    for card in remaining_cards:
        remaining_cards_copy = remaining_cards.copy()
        remaining_cards_copy.remove(card)

        dealer_cards_copy = dealer_cards.copy()
        dealer_cards_copy += [card]
        score = get_score(dealer_cards_copy)
        if score >= 22:
            score = 22
        if score < 17:
            determine_dealer_outcomes(remaining_cards_copy, dealer_cards_copy, dealer_outcomes)
        else:
            if dealer_outcomes.get(score):
                dealer_outcomes[score] += 1
            else:
                dealer_outcomes[score] = 1


def get_dealer_possible_outcomes(remaining_cards, dealer_cards):
    dealer_outcomes = {}
    determine_dealer_outcomes(remaining_cards, dealer_cards, dealer_outcomes)
    return dealer_outcomes


def get_score(user_cards: List[int]) -> int:
    sorted_cards = sorted(user_cards, reverse=True)
    user_score = 0
    for index, card in enumerate(sorted_cards):
        if card != 1:
            user_score += card
        else:
            if user_score + 11 + (1 * (len(sorted_cards) - index - 1)) > 21:
                user_score += 1
            else:
                user_score += 11
    return user_score


def build_histogram(user_outcomes):
    low_hands = 0
    high_hands = 0
    busting_hands = 0
    for key, value in collections.OrderedDict(sorted(user_outcomes.items())).items():
        # print("{}: {} {}".format(key, '-' * value, value))
        print("{}: {}".format(key, value))
        if key < 17:
            low_hands += value
        elif 17 <= key <= 21:
            high_hands += value
        else:
            busting_hands += value

    total_outcomes = low_hands + high_hands + busting_hands
    print("high_hand_chance: {}%".format(round((high_hands / total_outcomes) * 100.0, 1)))
    print("bust chance: {}%".format(round((busting_hands / total_outcomes) * 100.0, 1)))


def run_simulations(remaining_cards, seen_cards, user_cards, dealer_card):
    user_outcomes = get_user_possible_outcomes(remaining_cards, user_cards)
    print('user outcomes')
    build_histogram(user_outcomes)

    dealer_outcomes = get_dealer_possible_outcomes(remaining_cards, [dealer_card])
    print('dealer outcomes')
    build_histogram(dealer_outcomes)
    # while dealer_likely_score < 17:
    #     dealer_copy = remaining_cards.copy()
    #     dealer_copy.remove(likely_next_card)
    #     likely_next_card = median_high(dealer_copy)
    #     dealer_hand.append(likely_next_card)
    #     dealer_likely_score = get_score(dealer_hand)
    # print("dealer likely score: {}".format(dealer_likely_score))
    # print("remaining cards: {}".format(remaining_cards))

    hit_me(remaining_cards, seen_cards, user_cards, dealer_card)


def hit_me(remaining_cards, seen_cards, user_cards, dealer_card):
    hit = input("hit? (card value or n) ")
    if hit != "n":
        card = int(hit)
        remaining_cards.remove(card)
        seen_cards.append(card)
        user_cards.append(card)
        run_simulations(remaining_cards, seen_cards, user_cards, dealer_card)


def count_cards(decks: int):
    remaining_cards = []
    for i in range(decks):
        remaining_cards += generate_initial_deck()

    print("Enter the cards you see as their value (A = 1, 2 = 2, J = 10). Enter 'x' when it's your turn to play... ")

    while len(remaining_cards) > 0:
        entering_cards = True
        seen_cards = []
        while entering_cards:
            new_card = input("card: ")
            if new_card == "x":
                entering_cards = False
            else:
                card = int(new_card)
                seen_cards.append(card)
                remaining_cards.remove(card)

        user_cards = []
        print("what cards do you have? ")
        for i in range(2):
            user_cards.append(int(input("card: ")))

        dealer_card = int(input("what's the dealer's up card? "))

        run_simulations(remaining_cards, seen_cards, user_cards, dealer_card)


count_cards(1)
