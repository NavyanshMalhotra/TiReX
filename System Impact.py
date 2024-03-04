import random
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata
import plotly.graph_objs as go

# system_leakage = 0.1 # 0->1 Leakage of material from the ciruclar system to account for losses 
# recycling_yield = 0.8 # 0->1 Yield of grade-locked recycling technology 
# new_aircraft_demand = 100 # Demand quantity for new aircrafts
# old_aircrafts_at_eol = 50 # Number of planes being decommsioned  
# ti_value = 0.15 # 0->1 Mass of ti_alloy of interest as a percentage of total mass of plane 
# mass_plane = 100 # Total mass of plane 



#supply_demand_gap = total_demand_ti_mass - total_recycled_ti_mass

class scenario():
    def __init__(self):
        self.system_leakage = self.system_leakage()
        self.recycling_yield = self.recycling_yield()
        self.new_aircraft_demand = self.new_aircraft_demand()
        self.old_aircrafts_at_eol = self.old_aircrafts_at_eol()
        self.ti_value = self.ti_value()
        self.mass_plane = self.mass_plane()

    def system_leakage(self):
        return random.randint(15,25) / 100
        
    def recycling_yield(self):
        return random.randint(80,85) / 100

    def new_aircraft_demand(self):
        demand_2024 = 1300
        cagr = random.randint(85,95) / 1000
        return demand_2024 * ((1+cagr)**20)

    def old_aircrafts_at_eol(self):
        return random.randint(850,1150)
    
    def ti_value(self):
        return random.randint(14,16) / 100
            
    def mass_plane(self):
        return 195700

    def system_gain(self):
        system_gain = 1 # Calculated gain

        decommisioned_ti_mass = self.old_aircrafts_at_eol * self.mass_plane * self.ti_value    
        total_recycled_ti_mass = decommisioned_ti_mass * self.system_leakage * self.recycling_yield
        total_demand_ti_mass = self.new_aircraft_demand * self.ti_value * self.mass_plane

        current_cycle_ti = total_recycled_ti_mass
        cumalative_cycle_ti = current_cycle_ti

        while (current_cycle_ti > 0.001): 
            current_cycle_ti = current_cycle_ti * min(((1 - self.system_leakage) * self.recycling_yield), 1)
            cumalative_cycle_ti = cumalative_cycle_ti + current_cycle_ti


        system_gain = cumalative_cycle_ti / total_recycled_ti_mass

        return system_gain

#sc1 = scenario()
#print(f"Demand and Recycled Supply gap: {supply_demand_gap}, as compared to a virgin demand of {total_demand_ti_mass}. Saving {total_demand_ti_mass-supply_demand_gap}")
#print(f"Each kg of the titanium alloy has a gain of {sc1.system_gain()}x through the system with a leakage of {sc1.system_leakage} and recycling yield of {sc1.recycling_yield}") 

scenarios = [scenario() for _ in range(5)] 

system_gains = [scenario.system_gain() for scenario in scenarios]
system_leakages = [scenario.system_leakage for scenario in scenarios]
recycling_yields = [scenario.recycling_yield for scenario in scenarios]

for i, scenario in enumerate(scenarios):
    print(f"Each kg of the titanium alloy has a gain of {scenario.system_gain()}x through the system with a leakage of {scenario.system_leakage} and recycling yield of {scenario.recycling_yield}") 

""" fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.set_xlabel('Scenario')
ax1.set_ylabel('System Gain', color='tab:blue')
ax1.plot(system_gains, color='tab:blue', label='System Gain')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylabel('System Leakage', color='tab:red')
ax2.plot(system_leakages, color='tab:red', label='System Leakage')
ax2.tick_params(axis='y', labelcolor='tab:red')

ax3 = ax1.twinx()  # instantiate a third axes that shares the same x-axis
ax3.spines['right'].set_position(('outward', 60))  # Move the third axis to the right
ax3.set_ylabel('Recycling Yield', color='tab:green')
ax3.plot(recycling_yields, color='tab:green', label='Recycling Yield')
ax3.tick_params(axis='y', labelcolor='tab:green')

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.title('System Gain, Leakage, and Recycling Yield for Each Scenario')
plt.show() """

""" fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot with color coordination based on system_gain
sc = ax.scatter(system_leakages, recycling_yields, system_gains, c=system_gains, cmap='viridis', marker='o')

# Setting labels
ax.set_xlabel('System Leakage')
ax.set_ylabel('Recycling Yield')
ax.set_zlabel('System Gain')

# Adding a color bar
cbar = plt.colorbar(sc)
cbar.set_label('System Gain')

plt.title('3D Scatter Plot of System Gain, Leakage, and Recycling Yield')
plt.show()  """


""" system_leakages = np.array(system_leakages)
recycling_yields = np.array(recycling_yields)
system_gains = np.array(system_gains)

trace = go.Scatter3d(
    x=system_leakages,
    y=recycling_yields,
    z=system_gains,
    mode='markers',
    marker=dict(
        size=5,
        color=system_gains,  # Color by system_gain
        colorscale='Viridis',  # Color scale
        opacity=0.8,
        colorbar=dict(
            title='System Gain',
            x=0.8,  # Moves the colorbar closer to the plot, adjust as needed
            len=0.85,  # Adjusts the length of the colorbar (percentage of plot height)
            thickness=15,  # Adjusts the thickness of the colorbar
        )
    ),
    # Custom text for each marker
    text=[f'System Leakage: {leak:.2f}, Recycling Yield: {yield_:.2f}, System Gain: {gain:.2f}' 
          for leak, yield_, gain in zip(system_leakages, recycling_yields, system_gains)],
    hoverinfo='text'  # Show only the custom text
)

data = [trace]

layout = go.Layout(
    margin=dict(l=0, r=0, b=0, t=0),
    scene=dict(
        xaxis=dict(title='System Leakage'),
        yaxis=dict(title='Recycling Yield'),
        zaxis=dict(title='System Gain'),
    )
)

fig = go.Figure(data=data, layout=layout)
fig.show() """

plt.figure(figsize=(10, 8))
plt.scatter(system_leakages, recycling_yields, c=system_gains, cmap='viridis', s=50)
plt.colorbar(label='System Gain')
plt.xlabel('System Leakage')
plt.ylabel('Recycling Yield')
plt.title('System Gain vs. System Leakage and Recycling Yield')
plt.grid(True)
plt.show()   

print(f'Number of scenarios: {len(scenarios)}')
print(f'Mean of system gains: {np.mean(system_gains)}')
print(f'Stadard deviation of system gains: {np.std(system_gains)}')
print(f'Maximum system gain: {np.max(system_gains)}')
print(f'Minimum system gain: {np.min(system_gains)}')