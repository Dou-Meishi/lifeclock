import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyArrow


def get_percentage_on_log_interval(current, *, start, end):
    """Calculate position fraction on logarithmic scale"""
    return np.log(current / start) / np.log(end / start)


def get_num_from_percentage_on_log_interval(per, *, start, end):
    """The inverse of get_percentage_on_log_interval."""
    return np.exp(per * np.log(end / start) + np.log(start))


def create_clock(ax, start_age, end_age, highlights=None, current_age=None):
    """Create a styled clock with age progression"""
    # Set up polar plot
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.grid(False)
    ax.set_facecolor("floralwhite")

    # Remove polar grid lines
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.spines["polar"].set_visible(False)

    # Calculate positions
    hours = np.arange(1, 13)  # ends at 12 o'clock
    angles = hours / len(hours) * 2 * np.pi
    ages = get_num_from_percentage_on_log_interval(
        hours / len(hours),
        start=start_age,
        end=end_age,
    )

    # Add clock decorations
    # 1. Outer bezel
    ax.plot([0] + list(angles), [1.1] * 13, color="darkgoldenrod", lw=2, zorder=3)

    # 2. Hour markers
    for angle, hour in zip(angles, hours):
        ax.vlines(angle, 0.95, 1.05, color="saddlebrown", linewidth=2, zorder=4)

    # 3. Center hub
    ax.plot(0, 0, "o", markersize=10, color="black", zorder=5)

    # 4. Clock hands
    if current_age:
        per = get_percentage_on_log_interval(
            current=current_age, start=start_age, end=end_age
        )
        hour_hand = 2 * np.pi * per
        minute_hand = 2 * np.pi * ((per * 12) % 1.0)
        print(per, hour_hand, minute_hand)

        ax.quiver(
            0,
            0,
            0.35 * np.cos(-minute_hand + np.pi / 2),
            0.35 * np.sin(-minute_hand + np.pi / 2),
            color="black",
            #            scale_units="xy",
            scale=1,
            width=0.01,
            zorder=6,
        )
        ax.quiver(
            0,
            0,
            0.25 * np.cos(-hour_hand + np.pi / 2),
            0.25 * np.sin(-hour_hand + np.pi / 2),
            color="darkred",
            #            scale_units="xy",
            scale=1,
            width=0.008,
            zorder=5,
        )

    # the zero clock corresponds to the end age
    ax.text(
        0,
        1.20,
        f"{int(end_age):2d} | {int(start_age):2d}",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="darkgreen",
    )
    # Add age labels
    for angle, age in zip(angles[:-1], ages[:-1]):
        ax.text(
            angle,
            1.20,
            f"{float(age):.1f}",
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
            color="darkgreen",
        )

    # Add highlighted ranges
    if highlights:
        legend_handles, legend_labels = [], []
        for label, region_start, region_end, color in highlights:
            start_angle = (
                get_percentage_on_log_interval(
                    current=region_start, start=start_age, end=end_age
                )
                * 2
                * np.pi
            )
            end_angle = (
                get_percentage_on_log_interval(
                    current=region_end, start=start_age, end=end_age
                )
                * 2
                * np.pi
            )
            ax.barh(
                1,
                width=end_angle - start_angle,
                left=start_angle,
                color=color,
                alpha=0.4,
                height=0.3,
                zorder=2,
            )

            legend_handles.append(
                plt.Rectangle((0, 0), 1, 1, facecolor=color, alpha=0.4)
            )
            legend_labels.append(label)

        # Add legend outside the plot
        ax.legend(
            legend_handles,
            legend_labels,
            loc="upper left",
            bbox_to_anchor=(1.05, 1),
            title="Life Stages",
            frameon=False,
            fontsize=12,
        )


def get_color_from_bar(loc: float, cmap_name: str = "Set1"):
    cmap = plt.get_cmap(cmap_name)
    return cmap(np.clip(loc, 0.0, 1.0))


# Create figure
fig = plt.figure(figsize=(14, 7), facecolor="linen")

# First Clock (5-19 years)
ax1 = fig.add_subplot(121, projection="polar")
create_clock(
    ax1,
    5,
    19,
    highlights=[
        ("Middle school", 11, 17, get_color_from_bar(0.1)),
        ("Undergraduate", 17, 19, get_color_from_bar(0.3)),
    ],
)
ax1.set_title(
    "Childhood to Adolescence\n(5-19 Years)", fontsize=14, pad=30, color="darkblue"
)

# Second Clock (19-72 years)
ax2 = fig.add_subplot(122, projection="polar")
create_clock(
    ax2,
    19,
    72,
    highlights=[
        ("Undergraduate", 19, 21, get_color_from_bar(0.3)),
        ("Master's", 21, 24, get_color_from_bar(0.5)),
        ("PhD", 24, 28, get_color_from_bar(0.7)),
    ],
    current_age=26,
)
ax2.set_title(
    "Adulthood to Senior\n(19-72 Years)", fontsize=14, pad=30, color="darkred"
)

# Add decorative text
fig.text(
    0.5,
    0.05,
    "Life Clocks Visualization",
    ha="center",
    fontsize=18,
    color="maroon",
    fontweight="bold",
)

plt.tight_layout(pad=4)
plt.show()

output_path = "./My_life_clock.svg" 
fig.savefig(output_path)
print(output_path)
