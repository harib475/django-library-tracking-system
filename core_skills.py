import random
# Create a list of 10 random numbers between 1 and 20.
# Filter Numbers Below 10 (List Comprehension)
# Filter Numbers Below 10 (Using filter)


rand_list = [random.randint(1, 20) for _ in range(10)]

list_comprehension_below_10 = [num for num in rand_list if num < 10]

list_comprehension_below_10_filter = list(filter(lambda x: x < 10, rand_list))

print(rand_list,list_comprehension_below_10,list_comprehension_below_10_filter)