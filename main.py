from player import Player

print("Howdy, world!\n")

# Player Test code
p1 = Player("Alice")
p2 = Player("Bob")

print("Initial Player States:")
print(p1)
print(p2)

p1.change_points(10)
p2.change_points(5)
p1.change_points(-3)

p1.add_card(3)
p2.add_cards([5, 7, 9])

print()
print("After changes:")
print(p1)
print(p2)

print(f"Player #{p2.get_ID()}'s Cards:\n\t{p2.get_cards()}")



