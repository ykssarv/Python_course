"""Pancakes."""


def make_n_pancakes(n: int, ingredients: list) -> int:
    """Make n p."""
    dough = make_dough(ingredients)
    xd = 0
    while xd < n and can_make_pancake(dough):
        dough = make_a_pancake(dough)
        xd += 1
    return xd


def make_dough(ingredients: list) -> int:
    """You mu."""
    recipe = {
        "egg": 1,
        "milk": 5,
        "flour": 4,
        "sugar": 2,
        "butter": 1
    }
    ingredients_dict = {}

    for ingredient in recipe.keys():
        x = ingredients.count(ingredient)
        ingredients_dict[ingredient] = x
        ingredients_dict[ingredient] = ingredients_dict[ingredient] // recipe[ingredient]
    y = min(ingredients_dict.values()) * 7
    return y


def can_make_pancake(dough: float) -> bool:
    """Making one pancake takes 0.8 dl pancake dough."""
    if dough >= 0.8:
        return True
    else:
        return False


def make_a_pancake(dough: float) -> float:
    """Make a pancake. Making one pancake takes 0.8 dl dough."""
    dough -= 0.8
    dough = round(dough, 2)
    return dough
