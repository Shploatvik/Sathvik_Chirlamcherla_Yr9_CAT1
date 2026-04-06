import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Figure 1 with the button
fig1, ax1 = plt.subplots()
ax_button = fig1.add_axes([0.7, 0.05, 0.1, 0.075])
my_button = Button(ax_button, 'Click Me')

# Function to hide the button
def hide_my_button(event):
    my_button.ax.set_visible(False)    # Hide the axes container
    my_button.ax.patch.set_visible(False) # Hide the background
    my_button.label.set_visible(False)    # Hide the text label
    fig1.canvas.draw()                # Refresh the first figure

# Figure 2 with a trigger to hide Figure 1's button
fig2, ax2 = plt.subplots()
ax_trigger = fig2.add_axes([0.7, 0.05, 0.1, 0.075])
trigger_button = Button(ax_trigger, 'Hide Other')
trigger_button.on_clicked(hide_my_button)

plt.show()
