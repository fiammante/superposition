import plotly.graph_objects as go
import numpy as np

# Parameters
n_particles = 1500
n_frames = 60
source_x = 0
slit_x = 5
screen_x = 10

# Slit positions
slit1_y = 2
slit2_y = -2
slit_width = 0.4

# Choose which slit a particle goes through
def choose_slit():
    return slit1_y if np.random.random() < 0.5 else slit2_y

# Generate trajectories for each particle
trajectories = []
for i in range(n_particles):
    # All electrons start from single origin
    start_y = 0
    start_z = 0
    
    # Choose slit
    slit_y = choose_slit()
    slit_z = np.random.uniform(-slit_width, slit_width)
    
    # Calculate interference pattern on screen
    # The interference pattern appears in the Y direction (perpendicular to slit separation)
    wavelength = 0.8  # Arbitrary wavelength
    d = abs(slit1_y - slit2_y)  # Distance between slits (separation in Y)
    L = screen_x - slit_x  # Distance from slits to screen
    
    # For interference fringes in Y direction:
    # Position of bright fringes: y = m * λ * L / d
    # where m is the order number
    
    # Generate position based on interference probability
    # Sample from interference intensity distribution
    y_center = (slit1_y + slit2_y) / 2  # Center between slits
    
    # Create weighted random position based on interference intensity
    # Intensity = cos²(π * d * y / (λ * L))
    attempts = 0
    max_attempts = 100
    while attempts < max_attempts:
        # Random y position on screen
        y_candidate = np.random.uniform(y_center - 4, y_center + 4)
        
        # Calculate intensity at this position
        intensity = np.cos(np.pi * d * (y_candidate - y_center) / (wavelength * L)) ** 2
        
        # Accept position with probability proportional to intensity
        if np.random.random() < intensity:
            final_y = y_candidate
            break
        attempts += 1
    else:
        # Fallback if no position accepted
        final_y = y_center
    
    final_z = np.random.normal(0, 0.3)
    
    # Trajectory in 3 segments
    trajectory = {
        'x': [source_x, slit_x, screen_x],
        'y': [start_y, slit_y, final_y],
        'z': [start_z, slit_z, final_z],
        'slit': slit_y
    }
    trajectories.append(trajectory)

# Create animation frames
frames = []
for frame_idx in range(n_frames):
    n_visible = int((frame_idx + 1) / n_frames * n_particles)
    
    x_coords = []
    y_coords = []
    z_coords = []
    colors = []
    
    for i in range(n_visible):
        traj = trajectories[i]
        progress = min(1.0, (frame_idx + 1) / n_frames + i / n_particles)
        
        if progress < 0.33:
            # Before slit
            t = progress / 0.33
            x = source_x + t * (slit_x - source_x)
            y = traj['y'][0] + t * (traj['y'][1] - traj['y'][0])
            z = traj['z'][0] + t * (traj['z'][1] - traj['z'][0])
        elif progress < 0.66:
            # Between slit and screen
            t = (progress - 0.33) / 0.33
            x = slit_x + t * (screen_x - slit_x)
            y = traj['y'][1] + t * (traj['y'][2] - traj['y'][1])
            z = traj['z'][1] + t * (traj['z'][2] - traj['z'][1])
        else:
            # On screen
            x = screen_x
            y = traj['y'][2]
            z = traj['z'][2]
        
        x_coords.append(x)
        y_coords.append(y)
        z_coords.append(z)
        colors.append('rgb(255, 69, 0)')
    
    frames.append(go.Frame(
        data=[go.Scatter3d(
            x=x_coords,
            y=y_coords,
            z=z_coords,
            mode='markers',
            marker=dict(size=1, color=colors, opacity=0.7),
            name='Electrons'
        )],
        name=str(frame_idx)
    ))

# Initial figure
fig = go.Figure(
    data=[go.Scatter3d(
        x=[], y=[], z=[],
        mode='markers',
        marker=dict(size=1, opacity=0.7)
    )],
    frames=frames
)

# Add static elements - Barrier with slits
# Top section of barrier (light blue)
y_barrier = np.linspace(-5, slit2_y - slit_width, 20)
z_barrier = np.linspace(-3, 3, 20)
Y_top, Z_top = np.meshgrid(y_barrier, z_barrier)
X_top = np.ones_like(Y_top) * slit_x

fig.add_trace(go.Surface(
    x=X_top, y=Y_top, z=Z_top,
    colorscale=[[0, 'rgb(173, 216, 230)'], [1, 'rgb(173, 216, 230)']],
    showscale=False,
    opacity=0.8,
    name='Barrier'
))

# Middle section of barrier (light blue)
y_barrier_mid = np.linspace(slit2_y + slit_width, slit1_y - slit_width, 20)
z_barrier_mid = np.linspace(-3, 3, 20)
Y_mid, Z_mid = np.meshgrid(y_barrier_mid, z_barrier_mid)
X_mid = np.ones_like(Y_mid) * slit_x

fig.add_trace(go.Surface(
    x=X_mid, y=Y_mid, z=Z_mid,
    colorscale=[[0, 'rgb(173, 216, 230)'], [1, 'rgb(173, 216, 230)']],
    showscale=False,
    opacity=0.8,
    showlegend=False
))

# Bottom section of barrier (light blue)
y_barrier_bot = np.linspace(slit1_y + slit_width, 5, 20)
z_barrier_bot = np.linspace(-3, 3, 20)
Y_bot, Z_bot = np.meshgrid(y_barrier_bot, z_barrier_bot)
X_bot = np.ones_like(Y_bot) * slit_x

fig.add_trace(go.Surface(
    x=X_bot, y=Y_bot, z=Z_bot,
    colorscale=[[0, 'rgb(173, 216, 230)'], [1, 'rgb(173, 216, 230)']],
    showscale=False,
    opacity=0.8,
    showlegend=False
))

# Detection screen
y_screen = np.linspace(-5, 5, 30)
z_screen = np.linspace(-3, 3, 30)
Y_screen, Z_screen = np.meshgrid(y_screen, z_screen)
X_screen = np.ones_like(Y_screen) * screen_x

fig.add_trace(go.Surface(
    x=X_screen, y=Y_screen, z=Z_screen,
    colorscale=[[0, 'rgba(200,200,200,0.3)'], [1, 'rgba(200,200,200,0.3)']],
    showscale=False,
    opacity=0.3,
    name='Screen'
))

# Layout configuration
fig.update_layout(
    title="Double-Slit Experiment - Wave-Particle Duality (3D)",
    scene=dict(
        xaxis=dict(range=[-2, 12], title="Distance"),
        yaxis=dict(range=[-6, 6], title="Vertical Position"),
        zaxis=dict(range=[-4, 4], title="Depth"),
        camera=dict(
            eye=dict(x=-1.5, y=-1.5, z=0.8)
        ),
        aspectmode='manual',
        aspectratio=dict(x=2, y=1, z=0.8)
    ),
    updatemenus=[{
        'type': 'buttons',
        'showactive': False,
        'y': 0.9,
        'x': 0.1,
        'buttons': [
            {
                'label': 'Play',
                'method': 'animate',
                'args': [None, {
                    'frame': {'duration': 100, 'redraw': True},
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
    }],
    sliders=[{
        'active': 0,
        'steps': [
            {
                'args': [[f.name], {
                    'frame': {'duration': 0, 'redraw': True},
                    'mode': 'immediate',
                    'transition': {'duration': 0}
                }],
                'label': str(k),
                'method': 'animate'
            }
            for k, f in enumerate(fig.frames)
        ],
        'x': 0.1,
        'len': 0.9,
        'xanchor': 'left',
        'y': 0,
        'yanchor': 'top'
    }],
    width=1000,
    height=700,
    uirevision='constant'  # Preserves camera state
)

# Add JavaScript to update camera position in title
fig.update_layout(
    updatemenus=[{
        'type': 'buttons',
        'showactive': False,
        'y': 0.9,
        'x': 0.1,
        'buttons': [
            {
                'label': 'Play',
                'method': 'animate',
                'args': [None, {
                    'frame': {'duration': 100, 'redraw': True},
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

fig.show()

