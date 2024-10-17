import streamlit as st
import plotly.graph_objects as go
import json

# Load pin data from JSON file
def load_pin_data(file_path='components_data/pin_data.json'):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to plot pinout components on the grid
def plot_pinout_component(x_coordinates, y_positions, pin_labels, label):
    left_pins = pin_labels[0::2]
    right_pins = pin_labels[1::2]

    # Scatter traces for left and right columns
    left_column = go.Scatter(
        x=[x_coordinates[0]] * len(left_pins),
        y=y_positions,
        text=left_pins,
        mode='markers',
        textposition='middle left',
        marker=dict(size=20, color='rgba(0,0,0,0)', line=dict(width=2, color='green')),
        showlegend=False
    )

    right_column = go.Scatter(
        x=[x_coordinates[1]] * len(right_pins),
        y=y_positions,
        text=right_pins,
        mode='markers',
        textposition='middle right',
        marker=dict(size=20, color='rgba(0,0,0,0)', line=dict(width=2, color='green')),
        showlegend=False
    )

    component_label = go.Scatter(
        x=[(x_coordinates[0] + x_coordinates[1]) / 2],
        y=[max(y_positions) + 1],  # Position above the pins
        text=[label],
        mode='text',
        showlegend=False
    )

    return [left_column, right_column, component_label]

# Initialize session state for storing placed components
def init_session_state():
    if 'placed_components' not in st.session_state:
        st.session_state.placed_components = []

# Main Streamlit app
def main():
    st.set_page_config(layout="wide")
    st.title("Drag-and-Drop Raspberry Pi and Arduino Components")

    # Load pin data
    pin_data = load_pin_data()

    # Initialize session state
    init_session_state()

    # Sidebar with buttons for available components
    st.sidebar.header("Available Components")
    for component_name in pin_data.keys():
        if st.sidebar.button(f"Place {component_name}"):
            # Add the selected component to the session state
            st.session_state.placed_components.append(component_name)

    # Initialize Plotly figure
    fig = go.Figure()
    shapes = []  # Store border shapes for each component

    # Start position for x-coordinates and spacing
    x_start = 2  # Starting x-coordinate for the first component
    x_spacing = 4  # Spacing between components in x-direction

    # Add placed components to the grid dynamically
    for i, component in enumerate(st.session_state.placed_components):
        pin_labels = pin_data[component]
        num_pins = len(pin_labels) // 2  # Calculate number of pins per column
        y_positions = list(range(num_pins, 0, -1))  # Y-positions for pins

        # X-coordinates for left and right columns of the component
        x_coordinates = [x_start + i * x_spacing, x_start + i * x_spacing + 0.5]

        # Add the component's pins to the figure
        fig.add_traces(plot_pinout_component(x_coordinates, y_positions, pin_labels, component))

        # Add a border (rectangle) around the component's pins
        shapes.append(dict(
            type="rect",
            x0=x_coordinates[0] - 0.5, y0=min(y_positions) - 0.5,
            x1=x_coordinates[1] + 0.5, y1=max(y_positions) + 0.5,
            line=dict(color="blue", width=2)
        ))

    # Set layout properties
    fig.update_layout(
        title="Component Placement",
        xaxis=dict(range=[0, 15], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[0, 10], showgrid=False, zeroline=False, showticklabels=False),
        height=600, width=800,
        plot_bgcolor='white',  # Background color to white
        shapes=shapes  # Add the shapes (borders) to the layout
    )

    # Display the Plotly figure
    st.plotly_chart(fig, use_container_width=True)

# Run the Streamlit app
if __name__ == "__main__":
    main()
