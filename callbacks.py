# callbacks.py

# ==========================================
#               Imports
# ==========================================
from dash.dependencies import Input, Output
import tensorflow_datasets as tfds
import tensorflow as tf
from dash import html
from datasets import RL_data_sets
from utils import tensor_to_data_uri
from collections.abc import Iterable
from PIL import Image
import dash_bootstrap_components as dbc


# ==========================================
#           Helper Functions
# ==========================================
def truncate_text(text, unique_id):
    truncated_text = html.P(
        text,
        id="truncated-text" + str(unique_id),
        style={
            'width': '300px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'whiteSpace': 'nowrap',
            'cursor': 'pointer',
            'padding': '5px'
        }
    )
    tooltip = dbc.Tooltip(
        text,
        target="truncated-text" + str(unique_id),
        placement="top"
    )
    return html.Div([truncated_text, tooltip])


def process_step_key(step_sub, name, cell_id):
    column = []

    try:
        keys = step_sub.keys()
    except:
        if name == 'action':
            column.append(html.H4(name, style={'textDecoration': 'underline'}))
            truncated_text = truncate_text(str(step_sub.numpy()), 'action' + str(cell_id))
            column.append(truncated_text)
        elif name == 'reward':
            column.append(html.H4(name, style={'textDecoration': 'underline'}))
            column.append(html.H5(str(step_sub.numpy())))
        elif name == 'natural_language_embedding' or name == 'language_embedding':
            pass
        else:
            column.append(html.H5(name + ': ' + str(step_sub.numpy())))
            column.append(html.H5(str(step_sub.numpy())))
        column.append(html.P(''))
        return column

    column.append(html.H4(name, style={'textDecoration': 'underline'}))
    for key in keys:
        if key == 'natural_language_embedding' or key == 'language_embedding':
            continue
        else:
            column.append(html.H5(key))
            if len(step_sub[key].shape) == 3:
                image_tensor = tf.convert_to_tensor(step_sub[key])
                try:
                    data_uri = tensor_to_data_uri(image_tensor)
                    column.append(html.Img(src=data_uri, style={"width": "100%", "height": "auto", "marginBottom": "10px"}))
                except Exception as e:
                    print(f'Error processing image: {e}')
            elif step_sub[key].dtype == tf.string:
                column.append(html.P(step_sub[key].numpy().decode('utf-8')))
            elif step_sub[key].dtype == tf.float32:
                value = step_sub[key].numpy()
                if isinstance(value, Iterable):
                    formatted_values = [f"{x:.1f}, " for x in value]
                    formatted_values = truncate_text(formatted_values, key + str(cell_id))
                else:
                    formatted_values = [f"{value:.1f}"]
                column.append(html.P(formatted_values))

    column.append(html.P(''))
    column.append(html.P(''))

    return column


# ==========================================
#            Callback Registrations
# ==========================================
def register_callbacks(app):
    @app.callback(
        Output('columns-container', 'children'),
        Output('language-instruction', 'children'),
        [Input('episode-dropdown', 'value'),
         Input('data-set-dropdown', 'value')]
    )
    def update_columns(episode_number, data_set):
        task_instructions = 'Instruction = None'
        builder = tfds.builder_from_directory(builder_dir=data_set)
        ds = builder.as_dataset(split=f"train[{episode_number}:{episode_number + 1}]")

        try:
            episode = next(iter(ds))
        except StopIteration:
            return html.Div("No episodes found for the selected dataset and episode number.")

        steps = list(episode["steps"])
        num_columns = len(steps)

        if not steps:
            return html.Div("No steps found in the selected episode.")

        html_for_cells = []

        desired_order = ['observation', 'action', 'reward']

        list_of_keys = list(steps[0].keys())  # it is assumed that all steps have the same structure
        ordered = [item for item in desired_order if item in list_of_keys]
        remaining = [item for item in list_of_keys if item not in desired_order]
        reordered_list = ordered + remaining

        if 'language_instruction' in list_of_keys:
            task_instructions = 'Instruction =' + steps[0]['language_instruction'].numpy().decode('utf-8')
            reordered_list.remove('language_instruction')
        for index, step in enumerate(steps):
            row = []
            row.append(html.H4(f"Frame {index + 1}"))

            for key in reordered_list:
                subset = process_step_key(step[key], key, index)
                row = row + subset

            html_for_cells.append(html.Div(
                children=row,
                style={
                    "flex": "0 0 auto",
                    "width": "300px",
                    "margin": "10px",
                    "padding": "10px",
                    "border": "1px solid #ccc",
                    "border-radius": "5px",
                    "display": "flex",
                    "flexDirection": "column",
                    "background-color": "#f9f9f9",
                },
                key=f"column-{index}"
            ))
        return html_for_cells, task_instructions

    @app.callback(
        [Output('episode-dropdown', 'options'),
         Output('episode-dropdown', 'value')],
        [Input('data-set-dropdown', 'value')]
    )
    def update_episode_options(selected_dataset):
        # Initialize the TFDS builder for the selected dataset
        builder = tfds.builder_from_directory(
            builder_dir=selected_dataset
        )
        builder.download_and_prepare()

        # Get the number of episodes (assuming each example in 'train' is an episode)
        num_episodes = builder.info.splits['train'].num_examples

        # Generate episode options dynamically
        episode_options = [
            {'label': f'Episode {i}', 'value': i}
            for i in range(1, num_episodes + 1)
        ]

        # Set the default selected episode to the first one
        default_value = 1 if num_episodes >= 1 else None

        return episode_options, default_value
