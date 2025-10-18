# # Create temporary directory for frames
if not os.path.exists('frames'):
     os.makedirs('frames')
# 
# # Export each frame as an image
static_traces = [trace for trace in fig.data if isinstance(trace, go.Surface)]
# 
for i, frame in enumerate(fig.frames):
    # Create a new figure with current frame data
    all_traces = list(frame.data) + static_traces
    frame_fig = go.Figure(data=all_traces)
    # Copy layout from original figure (preserves camera, axes, scene settings)
    frame_fig.update_layout(
        title=fig.layout.title,
        scene=fig.layout.scene,
        width=fig.layout.width,
        height=fig.layout.height
    )     
 
    '''frame_fig.update_layout(
          updatemenus=[],
          sliders=[]
    )'''
#     
    # Save frame as image
    frame_fig.write_image(f"frames/frame_{i:03d}.png", width=1000, height=700)
    print(f"Saved frame {i+1}/{len(fig.frames)}")
# 
# # Use ffmpeg to create MP4 from frames
# # Requires ffmpeg installed: https://ffmpeg.org/download.html
os.system('ffmpeg -y -framerate 10 -i frames/frame_%03d.png -c:v libx264 -pix_fmt yuv420p double_slit_experiment.mp4')
# 
print("MP4 video created: double_slit_experiment.mp4")