import h5py
import matplotlib.pyplot as plt
import numpy as np
import ipywidgets as widgets
from ipywidgets import interactive_output, HBox, VBox
from IPython.display import display

class TomographyReconstruction:
    def __init__(self, dataset_path, size_ui = 10):
        self.dataset_path = dataset_path
        self.size_ui = size_ui
        self.load_data()
        self.create_widgets()
        self.setup_callbacks()
        self.create_ui()

    def load_data(self):
        with h5py.File(self.dataset_path, 'r') as f:
            self.data = f['/data'][:]

    def display_slice(self, slice_index, axis, vmin_percent, vmax_percent):
        if axis == 'X':
            max_index = self.data.shape[0] - 1
            slice_data = self.data[slice_index, :, :]
        elif axis == 'Y':
            max_index = self.data.shape[1] - 1
            slice_data = self.data[:, slice_index, :]
        elif axis == 'Z':
            max_index = self.data.shape[2] - 1
            slice_data = self.data[:, :, slice_index]

        self.slice_slider.max = max_index
        self.slice_slider.value = slice_index

        data_min = np.min(self.data)
        data_max = np.max(self.data)
        vmin = data_min + (data_max - data_min) * (vmin_percent / 100)
        vmax = data_max - (data_max - data_min) * ((100 - vmax_percent) / 100)

        plt.figure(figsize=(self.size_ui, self.size_ui))
        plt.imshow(slice_data, cmap='gray', vmin=vmin, vmax=vmax)
        plt.show()

    def create_widgets(self):
        self.slice_slider = widgets.IntSlider(min=0, max=self.data.shape[0]-1, step=1, value=500, description='Slice Index')
        self.axis_selector = widgets.RadioButtons(options=['X', 'Y', 'Z'], value='X', description='Axis')
        self.vmin_slider = widgets.FloatSlider(min=0, max=99, value=0, step=0.1, description='Black %')
        self.vmax_slider = widgets.FloatSlider(min=1, max=100, value=100, step=0.1, description='White %')

    def setup_callbacks(self):
        self.vmin_slider.observe(self.update_vmax_range, names='value')
        self.vmax_slider.observe(self.update_vmin_range, names='value')

    def update_vmin_range(self, change):
        vmax = change['new']
        self.vmin_slider.max = vmax - 1

    def update_vmax_range(self, change):
        vmin = change['new']
        self.vmax_slider.min = vmin + 1

    def update_display(self, slice_index, axis, vmin_percent, vmax_percent):
        self.display_slice(slice_index, axis, vmin_percent, vmax_percent)

    def create_ui(self):
        output = interactive_output(self.update_display, {'slice_index': self.slice_slider, 'axis': self.axis_selector, 'vmin_percent': self.vmin_slider, 'vmax_percent': self.vmax_slider})
        ui = VBox([output, self.slice_slider, self.vmin_slider, self.vmax_slider])
        ui_with_axis = HBox([ui, self.axis_selector])
        display(ui_with_axis)
