class Recipe:
    def __init__(self, *initial_data, **kwargs):
        self.title = None
        self.authors = None
        self.skill_level = None
        self.recipe_yield = None
        self.ingredients = None
        self.directions = None

        for recipe_dict in initial_data:
            assert isinstance(recipe_dict, dict)
            for k, v in recipe_dict.items():
                setattr(self, k, v)

        for k, v in kwargs.items():
            setattr(self, k, v)