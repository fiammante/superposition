import numpy as np
import plotly.graph_objects as go
from scipy.special import sph_harm_y

# Install required packages (run once):
# pip install kaleido plotly-orca psutil pillow

# Create spherical coordinates
theta = np.linspace(0, 2 * np.pi, 150)  # azimuthal angle
phi = np.linspace(0, np.pi, 150)        # polar angle
theta, phi = np.meshgrid(theta, phi)

# Base sphere radius
r_base = 1

# Tetrahedral symmetry parameters
l = 3  # degree
m_values = [-3, 3]  # orders for tetrahedral symmetry

# Animation parameters
num_frames = 60
amplitude = 0.5  # Oscillation amplitude
spin_speed = 0.5  # Rotation speed multiplier (0.5 = half speed)

# Calculate spherical harmonics (constant for all frames)
Y_3m3 = sph_harm_y(-3, 3, phi, theta)
Y_3p3 = sph_harm_y(3, 3, phi, theta)
Y_tet = Y_3m3 + Y_3p3
Y_tet_real = np.real(Y_tet)

# Calculate the maximum radius to set fixed axis limits
max_radius = r_base + amplitude * np.max(np.abs(Y_tet_real))

# Function to create RGBA colorscale with variable alpha
def create_transparent_colorscale(base_colorscale, min_alpha=0.3, max_alpha=0.9):
    """Create a colorscale with transparency"""
    # Get colors from matplotlib-style colorscale
    if base_colorscale == 'Viridis':
        colors = ['#440154', '#31688e', '#35b779', '#fde724']
    elif base_colorscale == 'Plasma':
        colors = ['#0d0887', '#7e03a8', '#cc4778', '#f89540', '#f0f921']
    else:
        colors = ['#0d0887', '#7e03a8', '#cc4778', '#f89540', '#f0f921']
    
    # Create colorscale with alpha values
    n_colors = len(colors)
    colorscale = []
    for i, color in enumerate(colors):
        position = i / (n_colors - 1)
        alpha = min_alpha + (max_alpha - min_alpha) * position
        # Convert hex to rgba
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            rgba = f'rgba({r},{g},{b},{alpha})'
            colorscale.append([position, rgba])
    
    return colorscale

# Rotation matrix around Z axis
def rotate_z(x, y, z, angle):
    """Rotate points around Z axis"""
    x_rot = x * np.cos(angle) - y * np.sin(angle)
    y_rot = x * np.sin(angle) + y * np.cos(angle)
    z_rot = z
    return x_rot, y_rot, z_rot

# Create transparent colorscales
colorscale1 = create_transparent_colorscale('Viridis', min_alpha=0.4, max_alpha=0.9)
colorscale2 = create_transparent_colorscale('Plasma', min_alpha=0.4, max_alpha=0.9)

# Create frames for animation
frames = []
for i in range(num_frames):
    # Time variable for oscillation
    t = i * 2 * np.pi / num_frames
    
    # Rotation angles (opposite directions)
    angle1 = spin_speed * t  # Clockwise rotation
    angle2 = -spin_speed * t  # Counter-clockwise rotation
    
    # First sphere - original phase with oscillation
    r_perturbation1 = amplitude * Y_tet_real * np.cos(t)
    r1 = r_base + r_perturbation1
    
    # Convert to Cartesian coordinates for sphere 1
    x1 = r1 * np.sin(phi) * np.cos(theta)
    y1 = r1 * np.sin(phi) * np.sin(theta)
    z1 = r1 * np.cos(phi)
    
    # Rotate sphere 1
    x1_rot, y1_rot, z1_rot = rotate_z(x1, y1, z1, angle1)
    
    # Second sphere - 180° phase shift with oscillation
    r_perturbation2 = amplitude * Y_tet_real * np.cos(t + np.pi)
    r2 = r_base + r_perturbation2
    
    # Convert to Cartesian coordinates for sphere 2
    x2 = r2 * np.sin(phi) * np.cos(theta)
    y2 = r2 * np.sin(phi) * np.sin(theta)
    z2 = r2 * np.cos(phi)
    
    # Rotate sphere 2 (opposite direction)
    x2_rot, y2_rot, z2_rot = rotate_z(x2, y2, z2, angle2)
    
    frames.append(go.Frame(
        data=[
            go.Surface(
                x=x1_rot, y=y1_rot, z=z1_rot,
                colorscale=colorscale1,
                showscale=False,
                surfacecolor=Y_tet_real,
                cmin=Y_tet_real.min(),
                cmax=Y_tet_real.max(),
                name='Sphere 1'
            ),
            go.Surface(
                x=x2_rot, y=y2_rot, z=z2_rot,
                colorscale=colorscale2,
                showscale=False,
                surfacecolor=Y_tet_real,
                cmin=Y_tet_real.min(),
                cmax=Y_tet_real.max(),
                name='Sphere 2'
            )
        ],
        name=str(i)
    ))

# Create initial frame
t = 0
angle1 = 0
angle2 = 0

# Sphere 1
r_perturbation1 = amplitude * Y_tet_real * np.cos(t)
r1 = r_base + r_perturbation1
x1 = r1 * np.sin(phi) * np.cos(theta)
y1 = r1 * np.sin(phi) * np.sin(theta)
z1 = r1 * np.cos(phi)
x1_rot, y1_rot, z1_rot = rotate_z(x1, y1, z1, angle1)

# Sphere 2 (180° phase shift)
r_perturbation2 = amplitude * Y_tet_real * np.cos(t + np.pi)
r2 = r_base + r_perturbation2
x2 = r2 * np.sin(phi) * np.cos(theta)
y2 = r2 * np.sin(phi) * np.sin(theta)
z2 = r2 * np.cos(phi)
x2_rot, y2_rot, z2_rot = rotate_z(x2, y2, z2, angle2)

# Create figure with animation
fig = go.Figure(
    data=[
        go.Surface(
            x=x1_rot, y=y1_rot, z=z1_rot,
            colorscale=colorscale1,
            showscale=False,
            surfacecolor=Y_tet_real,
            cmin=Y_tet_real.min(),
            cmax=Y_tet_real.max(),
            name='Sphere 1'
        ),
        go.Surface(
            x=x2_rot, y=y2_rot, z=z2_rot,
            colorscale=colorscale2,
            showscale=False,
            surfacecolor=Y_tet_real,
            cmin=Y_tet_real.min(),
            cmax=Y_tet_real.max(),
            name='Sphere 2'
        )
    ],
    frames=frames
)

# Add animation controls with fixed axis ranges
fig.update_layout(
    title='Spinning Spheres with Tetrahedral Symmetry',
    scene=dict(
        xaxis=dict(
            title='X',
            range=[-max_radius * 1.1, max_radius * 1.1],
            autorange=False
        ),
        yaxis=dict(
            title='Y',
            range=[-max_radius * 1.1, max_radius * 1.1],
            autorange=False
        ),
        zaxis=dict(
            title='Z',
            range=[-max_radius * 1.1, max_radius * 1.1],
            autorange=False
        ),
        aspectmode='cube',
        camera=dict(
            eye=dict(x=1.8, y=1.8, z=1.8)
        ),
        bgcolor='rgba(240, 240, 240, 1)'
    ),
    width=900,
    height=900,
    updatemenus=[{
        'type': 'buttons',
        'showactive': False,
        'x': 0.1,
        'y': 0.9,
        'buttons': [
            {
                'label': 'Play',
                'method': 'animate',
                'args': [None, {
                    'frame': {'duration': 240, 'redraw': True},
                    'fromcurrent': True,
                    'mode': 'immediate',
                    'transition': {'duration': 0}
                }]
            },
            {
                'label': 'Pause',
                'method': 'animate',
                'args': [[None], {
                    'frame': {'duration': 0, 'redraw': False},
                    'mode': 'immediate',
                    'transition': {'duration': 0}
                }]
            }
        ]
    }]
)

# Show the figure
fig.show()

# ============================================
# SAVE ANIMATION TO MP4
# ============================================

print("Saving animation frames...")

# Method 1: Using PIL to create frames and then ffmpeg
from PIL import Image
import io
import os

# Create a directory for frames
if not os.path.exists('frames'):
    os.makedirs('frames')

# Save each frame as an image
for i in range(num_frames):
    t = i * 2 * np.pi / num_frames
    angle1 = spin_speed * t
    angle2 = -spin_speed * t
    
    # First sphere
    r_perturbation1 = amplitude * Y_tet_real * np.cos(t)
    r1 = r_base + r_perturbation1
    x1 = r1 * np.sin(phi) * np.cos(theta)
    y1 = r1 * np.sin(phi) * np.sin(theta)
    z1 = r1 * np.cos(phi)
    x1_rot, y1_rot, z1_rot = rotate_z(x1, y1, z1, angle1)
    
    # Second sphere
    r_perturbation2 = amplitude * Y_tet_real * np.cos(t + np.pi)
    r2 = r_base + r_perturbation2
    x2 = r2 * np.sin(phi) * np.cos(theta)
    y2 = r2 * np.sin(phi) * np.sin(theta)
    z2 = r2 * np.cos(phi)
    x2_rot, y2_rot, z2_rot = rotate_z(x2, y2, z2, angle2)
    
    # Create figure for this frame
    fig_frame = go.Figure(
        data=[
            go.Surface(
                x=x1_rot, y=y1_rot, z=z1_rot,
                colorscale=colorscale1,
                showscale=False,
                surfacecolor=Y_tet_real,
                cmin=Y_tet_real.min(),
                cmax=Y_tet_real.max()
            ),
            go.Surface(
                x=x2_rot, y=y2_rot, z=z2_rot,
                colorscale=colorscale2,
                showscale=False,
                surfacecolor=Y_tet_real,
                cmin=Y_tet_real.min(),
                cmax=Y_tet_real.max()
            )
        ]
    )
    
    fig_frame.update_layout(
        scene=dict(
            xaxis=dict(range=[-max_radius * 1.1, max_radius * 1.1], autorange=False),
            yaxis=dict(range=[-max_radius * 1.1, max_radius * 1.1], autorange=False),
            zaxis=dict(range=[-max_radius * 1.1, max_radius * 1.1], autorange=False),
            aspectmode='cube',
            camera=dict(eye=dict(x=1.8, y=1.8, z=1.8)),
            bgcolor='rgba(240, 240, 240, 1)'
        ),
        width=900,
        height=900,
        showlegend=False
    )
    
    # Save frame as PNG
    fig_frame.write_image(f'frames/frame_{i:03d}.png')
    print(f"Saved frame {i+1}/{num_frames}")

print("\nFrames saved! Now converting to MP4...")
print("Run this command in your terminal:")
print("ffmpeg -r 20 -i frames/frame_%03d.png -vcodec libx264 -pix_fmt yuv420p -crf 18 spheres_animation.mp4")