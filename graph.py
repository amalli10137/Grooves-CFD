import matplotlib.pyplot as plt

reynolds_numbers = [175.77399438202235, 214.12048314606747, 251.99447191011242, 136.95315168539307, 289.5252471910112, 320.87084831460686, 308.388926966292, 314.63266853932623, 302.08924719101174, 97.44269662921357]
neg_decay = [0.06847819453527003, 0.053512325255463976, 0.037647582495130213, 0.08005889036644045, 0.02080146886798285, 0.005140303173631356, 0.011821148137158037, 0.007607062225031058, 0.014560979405140253, 0.08764046685172594]
decay_rates = [-decay for decay in neg_decay]

plt.figure(figsize=(10, 6))
plt.ylim(min(decay_rates) - 0.02, max(decay_rates) + 0.02)  
plt.scatter(reynolds_numbers, decay_rates, color='blue', label='Data points')
plt.xlabel('Reynolds Number')
plt.ylabel('Decay Rate (-b in Ae^-bt)')
plt.title('Reynolds Number vs Decay Rate')
plt.legend(loc="upper left")



plt.grid(True)



plt.savefig('RE_vs_decay.png')