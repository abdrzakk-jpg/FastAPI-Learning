



from string import ascii_letters, digits
from random import choices

gen_code = lambda: "".join(choices(ascii_letters+digits, k=4))

print(f"{gen_code()}")