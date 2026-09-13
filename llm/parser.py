def asssign(self):
        if approx_value is not None:
            nutr_min = self.approx_value * 0.9
            nutr_max = self.approx_value * 1.1
        else:
            nutr_min = self.stated_min
            nutr_max = self.stated_max
        return(nutr_min, nutr_max)

    @model_validator(mode = 'after')
    def assign_boundaries(self):
        boundaries = [(min_calories, max_calories, calorie_boundary),
                    (min_protein, max_protein, protein_boundary),
                    (min_carbs, max_carbs, carbs_boundary),
                    (min_fat, max_fat, fat_boundary)]
        for nutr_min, nutr_max, boundary in boundaries:
            boundary = assign(self, nutr_min, nutr_max)