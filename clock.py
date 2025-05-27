import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyArrow

def create_clock(ax, start_age, end_age, highlights=None, current_age=None):
    """Create a styled clock with age progression"""
    # Set up polar plot
    ax.set_theta_offset(np.pi/2)
    ax.set_theta_direction(-1)
    ax.grid(False)
    ax.set_facecolor('floralwhite')

    # Remove polar grid lines
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.spines['polar'].set_visible(False)

    # Calculate positions
    total_years = end_age - start_age
    hours = np.arange(12)
    angles = np.linspace(0, 2*np.pi, 12, endpoint=False)
    ages = [start_age + (i * total_years/12) for i in range(12)]

    # Add clock decorations
    # 1. Outer bezel
    ax.plot(angles, [1.1]*12, color='darkgoldenrod', lw=2, zorder=3)

    # 2. Hour markers
    for angle, hour in zip(angles, hours):
        ax.vlines(angle, 0.95, 1.05, color='saddlebrown', linewidth=2, zorder=4)

    # 3. Center hub
    ax.plot(0, 0, 'o', markersize=10, color='black', zorder=5)

    # 4. Clock hands (static position)
    ax.quiver(0, 0, 0, 1, color='black', scale_units='xy', scale=1, width=0.01, zorder=6)
    ax.quiver(0, 0, np.pi/6, 0.7, color='darkred', scale_units='xy', scale=1, width=0.008, zorder=5)

    # Add age labels
    for angle, age in zip(angles, ages):
        text_angle = np.degrees(angle) % 360
        ax.text(angle, 1.15, f'{int(age)}',
                ha='center', va='center',
                rotation=text_angle-90 if text_angle > 90 else text_angle+270,
                fontsize=12, fontweight='bold', color='darkgreen')

    # Add highlighted ranges
    if highlights:
        for label, start, end, color in highlights:
            start_angle = -((start - start_age)/total_years) * 2*np.pi + np.pi/2
            end_angle = -((end - start_age)/total_years) * 2*np.pi + np.pi/2
            ax.barh(1, width=end_angle - start_angle, left=start_angle,
                    color=color, alpha=0.4, height=0.3, zorder=2)

            # Add annotation
            mid_angle = (start_angle + end_angle)/2
            ax.text(mid_angle, 0.7, label, rotation=np.degrees(-mid_angle)-90,
                    ha='center', va='center', color=color, fontsize=12,
                    bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    # Current age indicator
    if current_age:
        age_frac = np.log(current_age/start_age)/np.log(end_age/start_age)
        arrow_angle = -age_frac * 2*np.pi + np.pi/2
        ax.add_patch(FancyArrow(arrow_angle, 1.1, 0, -0.3,
                    width=0.02, color='crimson', zorder=10,
                    head_width=0.15, head_length=0.1))

# Create figure
fig = plt.figure(figsize=(14, 7), facecolor='linen')

# First Clock (5-19 years)
ax1 = fig.add_subplot(121, projection='polar')
create_clock(ax1, 5, 19, highlights=[
    ('Middle school', 11, 17, 'limegreen'),
])
ax1.set_title('Childhood to Adolescence\n(5-19 Years)', fontsize=14, pad=30, color='darkblue')

# Second Clock (19-72 years)
ax2 = fig.add_subplot(122, projection='polar')
create_clock(ax2, 19, 72, highlights=[
    ('Master\'s', 21, 24, 'dodgerblue'),
    ('PhD', 24, 28, 'limegreen')
])
ax2.set_title('Adulthood to Senior\n(19-72 Years)', fontsize=14, pad=30, color='darkred')

# Add decorative text
fig.text(0.5, 0.05, 'Life Clocks Visualization', ha='center',
         fontsize=18, color='maroon', fontweight='bold')

plt.tight_layout(pad=4)
plt.show()
