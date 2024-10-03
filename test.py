import plotly.graph_objects as go

def plot_multiple_pinouts(pin_sets):
    # Create an empty list for the scatter plots and shapes
    data = []
    shapes = []
    max_pins = 0

    # Generate the scatter traces for each pin set
    for pin_labels, x_coordinates, label in pin_sets:
        # Validate input lengths
        if len(pin_labels) % 2 != 0:
            raise ValueError("The number of pin labels must be even.")
        if len(x_coordinates) != 2:
            raise ValueError("Exactly two x-coordinates must be provided.")
        
        # Split the pins into two columns
        left_pins = pin_labels[0::2]
        right_pins = pin_labels[1::2]

        # Create y-axis positions for the pins
        y_positions = list(range(len(pin_labels) // 2, 0, -1))

        # Create scatter traces for left and right columns with hollow circles
        left_column = go.Scatter(
            x=[x_coordinates[0]] * len(left_pins),
            y=y_positions,
            text=left_pins,
            mode='markers',
            textposition='middle left',
            marker=dict(
                size=20,                # Size of the marker (circle)
                color='rgba(0,0,0,0)',  # Transparent fill to make it hollow
                line=dict(
                    width=2,            # Border width
                    color='green'       # Border color (green)
                )
            ),
            showlegend=False
        )

        right_column = go.Scatter(
            x=[x_coordinates[1]] * len(right_pins),
            y=y_positions,
            text=right_pins,
            mode='markers',
            textposition='middle right',
            marker=dict(
                size=20,                # Size of the marker (circle)
                color='rgba(0,0,0,0)',  # Transparent fill to make it hollow
                line=dict(
                    width=2,            # Border width
                    color='green'       # Border color (green)
                )
            ),
            showlegend=False
        )

        # Generate number labels for the pins
        number_labels = go.Scatter(
            x=[x_coordinates[0]] * len(left_pins) + [x_coordinates[1]] * len(right_pins),
            y=y_positions + y_positions,
            text=[str(i) for i in range(1, len(pin_labels) + 1, 2)] + [str(i) for i in range(2, len(pin_labels) + 1, 2)],
            mode='text',
            textposition='middle center',
            showlegend=False
        )

        # Update max_pins for determining the height of the plot
        max_pins = max(max_pins, len(pin_labels) // 2)

        # Create the border shape with rounded corners and an empty middle
        border_shape = dict(
            type="rect",
            xref="x",
            yref="y",
            x0=x_coordinates[0] - 0.25,  # Adjust based on x-coordinate
            y0=0,                       # Start of the border
            x1=x_coordinates[1] + 0.25,   # Adjust based on x-coordinate
            y1=len(pin_labels) / 2 + 1, # End of the border dynamically based on number of pins
            line=dict(
                color="black",
                width=2,  # Increase the border width for better visibility
            ),
            fillcolor="rgba(0,0,0,0)",  # Transparent fill to leave middle empty
            opacity=1,
            layer="below",  # Ensure the border is behind the pins
            editable=False
        )

        # Add the component label on top of the border
        component_label = go.Scatter(
            x=[(x_coordinates[0] + x_coordinates[1]) / 2],  # Centered on the border
            y=[len(pin_labels) / 2 + 1.50],                    # Above the border
            text=[label],                                    # Component name
            mode='text',
            textposition='middle center',
            showlegend=False
        )

        # Add the scatter plots and shapes to the data and shapes lists
        data.extend([left_column, right_column, number_labels, component_label])
        shapes.append(border_shape)

    # Create a layout for the plot
    layout = go.Layout(
        title="Multiple Component Pinouts",
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[0, 5]),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[0, max_pins + 2]),
        height=600,
        width=600,
        margin=dict(l=10, r=10, t=50, b=50),
        plot_bgcolor='white',
        shapes=shapes  # Add all border shapes to the layout
    )

    # Create figure and add all scatter plots
    fig = go.Figure(data=data, layout=layout)

    # Show the plot
    fig.show()

# Example usage with multiple components
raspberry_pi_pins = [
    "3.3V", "5V", "GPIO 2 (SDA1)", "5V", "GPIO 3 (SCL1)", "GND", "GPIO 4 (GPCLK0)",
    "GPIO 14 (TXD)", "GND", "GPIO 15 (RXD)", "GPIO 17", "GPIO 18 (PCM_CLK)", 
    "GPIO 27", "GND", "GPIO 22", "GPIO 23", "3.3V", "GPIO 24", "GPIO 10 (MOSI)",
    "GND", "GPIO 9 (MISO)", "GPIO 25", "GPIO 11 (SCLK)", "GPIO 8 (CE0)", "GND",
    "GPIO 7 (CE1)", "ID_SD", "ID_SC", "GPIO 5", "GND", "GPIO 6", "GPIO 12 (PWM0)",
    "GND", "GPIO 13 (PWM1)", "GPIO 19 (PCM_FS)", "GPIO 16", "GPIO 26", "GPIO 20 (PCM_DIN)",
    "GND", "GPIO 21 (PCM_DOUT)"
]

arduino_pins = [
    "5V", "GND", "GPIO 0", "GPIO 1", "GPIO 2", "GPIO 3", "GPIO 4", "GPIO 5",
    "GND", "GPIO 6", "GPIO 7", "GPIO 8", "GPIO 9", "GPIO 10", "GND", "GPIO 11",
    "GPIO 12", "GPIO 13", "GND", "GPIO 14", "GPIO 15", "GPIO 16", "GND", "GPIO 17"
]

# Call the function to plot multiple pinouts
plot_multiple_pinouts([
    (raspberry_pi_pins, [2, 2.5], "Raspberry Pi"),  # Raspberry Pi pinout
    (arduino_pins, [4, 4.5], "Arduino")              # Arduino pinout
])
