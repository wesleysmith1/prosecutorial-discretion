# variable ordering
# v, 
# s, 
# c, 
# q_i, 
# q_g, 
# g_i, 
# g_g, 
# w_upperbarbar, 
# b_lowerbar

# this configuration gets injected into main/__innit__.py/models.Constants

pooling = (5, 4, 1, .25, .5, .25, .5, 10, 0)
# high_crime_value = (7.5, 4, 1, .25, .5, .25, .5, 10, 0)
truncated_wealth = (5, 4, 1, .25, .5, .25, .5, 6.15 ,0)
restricted_plea_bargain = (5, 4, 1, .25, .5, .25, .5, 10, 3)

# define treatment 
config = truncated_wealth