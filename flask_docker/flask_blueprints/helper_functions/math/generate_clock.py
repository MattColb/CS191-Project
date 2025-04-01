import matplotlib.pyplot as plt
import numpy as np
import io

def draw_clock(time):
    """Generates an analog clock image with the given hour and minute."""
    
    hour, minute = time.split(":")
    hour = int(hour)
    minute = int(minute)

    # Convert hour to 12-hour format and map to 360 degrees (each hour is 30 degrees)
    hour_angle = (hour % 12 + minute / 60) * 30  
    minute_angle = minute * 6  # Each minute is 6 degrees

    # Convert angles to radians
    hour_angle = np.radians(90 - hour_angle)
    minute_angle = np.radians(90 - minute_angle)

    # Create figure
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

    # Draw clock face
    circle = plt.Circle((0, 0), 1, color="black", fill=False, linewidth=3)
    ax.add_patch(circle)

    # Draw hour markers
    for i in range(12):
        angle = np.radians(90 - i * 30)
        x1, y1 = np.cos(angle) * 0.85, np.sin(angle) * 0.85
        x2, y2 = np.cos(angle) * 0.95, np.sin(angle) * 0.95
        ax.plot([x1, x2], [y1, y2], color="black", linewidth=2)

    # Draw hour hand
    ax.plot([0, np.cos(hour_angle) * 0.5], [0, np.sin(hour_angle) * 0.5], 
            color="black", linewidth=4)

    # Draw minute hand
    ax.plot([0, np.cos(minute_angle) * 0.8], [0, np.sin(minute_angle) * 0.8], 
            color="black", linewidth=3)

    # Draw center dot
    ax.scatter(0, 0, color="black", s=50)

    # Save and show the image
    plt.axis("off")

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format="png", bbox_inches="tight", dpi=200)
    plt.close()

    img_bytes.seek(0)  # Move to the beginning of the byte stream
    return img_bytes
