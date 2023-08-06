# Copyright © 2019. Allen Institute.  All rights reserved.

import pandas as pd
import os
import numpy as np
import json
import glob
import sys
import time

# Copyright © 2019. Allen Institute.  All rights reserved.

# import h5py as h5
import numpy as np


class Epoch:
    """
    Represents a data epoch with a start time (in seconds), an end time (in seconds), and a name

    Optionally includes a start_index and an end_index

    """

    def __init__(self, name, start_time, end_time):

        """
        name : str
            Name of epoch
        start_time : float
            Start time in seconds
        end_time : float
            End time in seconds (can be Inf to use the full file)
        """

        self.start_time = start_time
        self.end_time = end_time
        self.name = name
        self.start_index = None
        self.end_index = None

    def convert_to_index(self, timestamps):

        """ Converts start/end times to start/end indices

        Input:
        ------
        timestamps : numpy.ndarray (float)
            Array of timestamps for each sample

        """

        self.start_index = np.argmin(np.abs(timestamps - self.start_time))

        if self.end_time != np.Inf:
            self.end_index = np.argmin(np.abs(timestamps - self.end_time))
        else:
            self.end_index = timestamps.size

    def __str__(self):
        return str(self.name) + ": " + str((self.start_time, self.end_time))

    def __repr__(self):
        return str(self)


def find_range(x, a, b, option='within'):
    """
    Find indices of data within or outside range [a,b]

    Inputs:
    -------
    x - numpy.ndarray
        Data to search
    a - float or int
        Minimum value
    b - float or int
        Maximum value
    option - String
        'within' or 'outside'

    Output:
    -------
    inds - numpy.ndarray
        Indices of x that fall within or outside specified range

    """

    if option == 'within':
        return np.where(np.logical_and(x >= a, x <= b))[0]
    elif option == 'outside':
        return np.where(np.logical_or(x < a, x > b))[0]
    else:
        raise ValueError('unrecognized option paramter: {}'.format(option))


def rms(data):
    """
    Computes root-mean-squared voltage of a signal

    Input:
    -----
    data - numpy.ndarray

    Output:
    ------
    rms_value - float

    """

    return np.power(np.mean(np.power(data.astype('float32'), 2)), 0.5)


def write_probe_json(output_file, channels, offset, scaling, mask, surface_channel, air_channel, vertical_pos,
                     horizontal_pos):
    """
    Writes a json file containing information about one Neuropixels probe.

    Inputs:
    -------
    output_file : file path
        Location for writing the json file
    channels : numpy.ndarray (384 x 0)
        Probe channel numbers
    offset : numpy.ndarray (384 x 0)
        Offset of each channel from zero
    scaling : numpy.ndarray (384 x 0)
        Relative noise level on each channel
    mask : numpy.ndarray (384 x 0)
        1 if channel contains valid data, 0 otherwise
    surface_channel : Int
        Index of channel at brain surface
    air_channel : Int
        Index of channel at interface between saline/agar and air
    vertical_pos : numpy.ndarray (384 x 0)
        Distance (in microns) of each channel from the probe tip
    horizontal_pos : numpy.ndarray (384 x 0)
        Distance (in microns) of each channel from the probe edge

    Outputs:
    --------
    output_file.json (written to disk)

    """

    with open(output_file, 'w') as outfile:
        json.dump(
            {
                'channel': channels.tolist(),
                'offset': offset.tolist(),
                'scaling': scaling.tolist(),
                'mask': mask.tolist(),
                'surface_channel': surface_channel,
                'air_channel': air_channel,
                'vertical_pos': vertical_pos.tolist(),
                'horizontal_pos': horizontal_pos.tolist()
            },

            outfile,
            indent=4, separators=(',', ': ')
        )


def read_probe_json(input_file):
    """
    Reads a json file containing information about one Neuropixels probe.

    Inputs:
    -------
    input_file : file path
        Location of file to read

    Outputs:
    --------
    mask : numpy.ndarray (384 x 0)
        1 if channel contains valid data, 0 otherwise
    offset : numpy.ndarray (384 x 0)
        Offset of each channel from zero
    scaling : numpy.ndarray (384 x 0)
        Relative noise level on each channel
    surface_channel : Int
        Index of channel at brain surface
    air_channel : Int
        Index of channel at interface between saline/agar and air

    """

    with open(input_file) as data_file:
        data = json.load(data_file)

    scaling = np.array(data['scaling'])
    mask = np.array(data['mask'])
    offset = np.array(data['offset'])
    surface_channel = data['surface_channel']
    air_channel = data['air_channel']

    return mask, offset, scaling, surface_channel, air_channel


def write_cluster_group_tsv(IDs, quality, output_directory):
    """
    Writes a tab-separated cluster_group.tsv file

    Inputs:
    -------
    IDs : list
        List of cluster IDs
    quality : list
        Quality ratings for each unit (same size as IDs)
    output_directory : String
        Location to save the file

    Outputs:
    --------
    cluster_group.tsv (written to disk)

    """

    cluster_quality = []
    cluster_index = []

    for idx, ID in enumerate(IDs):

        cluster_index.append(ID)

        if quality[idx] == 0:
            cluster_quality.append('unsorted')
        elif quality[idx] == 1:
            cluster_quality.append('good')
        else:
            cluster_quality.append('noise')

    df = pd.DataFrame(data={'cluster_id': cluster_index, 'group': cluster_quality})

    print('Saving data...')

    df.to_csv(os.path.join(output_directory, 'cluster_group.tsv'), sep='\t', index=False)


def read_cluster_group_tsv(filename):
    """
    Reads a tab-separated cluster_group.tsv file from disk

    Inputs:
    -------
    filename : String
        Full path of file

    Outputs:
    --------
    IDs : list
        List of cluster IDs
    quality : list
        Quality ratings for each unit (same size as IDs)

    """

    info = np.genfromtxt(filename, dtype='str')
    cluster_ids = info[1:, 0].astype('int')
    cluster_quality = info[1:, 1]

    return cluster_ids, cluster_quality


def load(folder, filename):
    """
    Loads a numpy file from a folder.

    Inputs:
    -------
    folder : String
        Directory containing the file to load
    filename : String
        Name of the numpy file

    Outputs:
    --------
    data : numpy.ndarray
        File contents

    """

    return np.load(os.path.join(folder, filename))


def load_kilosort_data(folder,
                       sample_rate=None,
                       convert_to_seconds=True,
                       use_master_clock=False,
                       include_pcs=False,
                       template_zero_padding=21):
    """
    Loads Kilosort output files from a directory

    Inputs:
    -------
    folder : String
        Location of Kilosort output directory
    sample_rate : float (optional)
        AP band sample rate in Hz
    convert_to_seconds : bool (optional)
        Flags whether to return spike times in seconds (requires sample_rate to be set)
    use_master_clock : bool (optional)
        Flags whether to load spike times that have been converted to the master clock timebase
    include_pcs : bool (optional)
        Flags whether to load spike principal components (large file)
    template_zero_padding : int (default = 21)
        Number of zeros added to the beginning of each template

    Outputs:
    --------
    spike_times : numpy.ndarray (N x 0)
        Times for N spikes
    spike_clusters : numpy.ndarray (N x 0)
        Cluster IDs for N spikes
    spike_templates : numpy.ndarray (N x 0)
        Template IDs for N spikes
    amplitudes : numpy.ndarray (N x 0)
        Amplitudes for N spikes
    unwhitened_temps : numpy.ndarray (M x samples x channels)
        Templates for M units
    channel_map : numpy.ndarray
        Channels from original data file used for sorting
    cluster_ids : Python list
        Cluster IDs for M units
    cluster_quality : Python list
        Quality ratings from cluster_group.tsv file
    pc_features (optinal) : numpy.ndarray (N x channels x num_PCs)
        PC features for each spike
    pc_feature_ind (optional) : numpy.ndarray (M x channels)
        Channels used for PC calculation for each unit

    """

    if use_master_clock:
        spike_times = load(folder, 'spike_times_master_clock.npy')
    else:
        spike_times = load(folder, 'spike_times.npy')

    spike_clusters = load(folder, 'spike_clusters.npy')
    spike_templates = load(folder, 'spike_templates.npy')
    amplitudes = load(folder, 'amplitudes.npy')
    templates = load(folder, 'templates.npy')
    unwhitening_mat = load(folder, 'whitening_mat_inv.npy')
    channel_map = load(folder, 'channel_map.npy')

    if include_pcs:
        pc_features = load(folder, 'pc_features.npy')
        pc_feature_ind = load(folder, 'pc_feature_ind.npy')

    templates = templates[:, template_zero_padding:, :]  # remove zeros
    spike_clusters = np.squeeze(spike_clusters)  # fix dimensions
    spike_times = np.squeeze(spike_times)  # fix dimensions

    if convert_to_seconds and sample_rate is not None:
        spike_times = spike_times / sample_rate

    unwhitened_temps = np.zeros((templates.shape))

    for temp_idx in range(templates.shape[0]):
        unwhitened_temps[temp_idx, :, :] = np.dot(np.ascontiguousarray(templates[temp_idx, :, :]),
                                                  np.ascontiguousarray(unwhitening_mat))

    try:
        cluster_ids, cluster_quality = read_cluster_group_tsv(os.path.join(folder, 'cluster_group.tsv'))
    except OSError:
        cluster_ids = np.unique(spike_clusters)
        cluster_quality = ['unsorted'] * cluster_ids.size

    if not include_pcs:
        return spike_times, spike_clusters, spike_templates, amplitudes, unwhitened_temps, channel_map, cluster_ids, cluster_quality
    else:
        return spike_times, spike_clusters, spike_templates, amplitudes, unwhitened_temps, channel_map, cluster_ids, cluster_quality, pc_features, pc_feature_ind


def get_spike_positions(spike_clusters, pc_features, pc_feature_ind, channel_locations=None,
                        vertical_channel_spacing=10):
    """
    Calculates the estimated position (in microns - x, y) of individual spikes

    If channel_locations are not used, it assumes a linear channel layout, and equal vertical spacing between channels;
    for a Neuropixels probe, it does not account for the fact that the probe is staggered.

    This implementation is based on Matlab code from github.com/cortex-lab/spikes

    Input:
    -----
    spike_clusters : numpy.ndarray (N x 0)
        Cluster IDs for N spikes
    pc_features : numpy.ndarray (N x channels x num_PCs)
        PC features for each spike
    pc_feature_ind  : numpy.ndarray (M x channels)
        Channels used for PC calculation for each unit
    channel_locations: numpy.ndarray (num_channels x 2)
        Locations of all channels of the probe. If None, vertical_channel_spacing is used
    vertical_channel_spacing : float
        Vertical channel spacing in microns (assumed to be equal for all channels)

    Output:
    ------
    spike_depths : numpy.ndarray (N x 0)
        Distance (in microns) from each spike waveform from the probe tip

    """
    pc_features_drift = np.copy(pc_features)
    pc_features_drift = pc_features_drift[:, 0, :]  # ????
    pc_features_drift[pc_features_drift < 0] = 0
    pc_power = pow(pc_features_drift, 2)
    spike_feat_ind = pc_feature_ind[spike_clusters, :]
    if channel_locations is not None:
        com = np.array([np.sum((channel_locations[spike_feat_ind][:, :, 0] * pc_power), 1) / np.sum(pc_power, 1),
                        np.sum((channel_locations[spike_feat_ind][:, :, 1] * pc_power), 1) / np.sum(pc_power, 1)]).T
    else:
        spike_depths = np.sum(spike_feat_ind * pc_power, 1) / np.sum(pc_power, 1)
        com = np.zeros((len(pc_features_drift), 2))
        com[:, 1] = spike_depths * vertical_channel_spacing

    return com


def get_spike_amplitudes(spike_templates, templates, amplitudes):
    """
    Calculates the amplitude of individual spikes, based on the original template
    plus a scaling factor

    This implementation is based on Matlab code from github.com/cortex-lab/spikes

    Inputs:
    -------
    spike_templates : numpy.ndarray (N x 0)
        Template IDs for N spikes
    templates : numpy.ndarray (M x samples x channels)
        Unwhitened templates for M units
    amplitudes : numpy.ndarray (N x 0)
        Amplitudes for N spikes

    Outputs:
    --------
    spike_amplitudes : numpy.ndarray (N x 0)
        Amplitudes for N spikes

    """

    template_amplitudes = np.max(np.max(templates, 1) - np.min(templates, 1), 1)

    spike_amplitudes = template_amplitudes[spike_templates] * amplitudes

    return np.squeeze(spike_amplitudes)


def printProgressBar(iteration, total, prefix='', suffix='', decimals=0, length=40, fill='▒'):
    """
    Call in a loop to create terminal progress bar

    Code from https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console

    Inputs:
    -------
    iteration - Int
        Current iteration
    total - Int
        Total iterations
    prefix - Str (optional)
        Prefix string
    suffix - Str (optional)
        Suffix string
    decimals - Int (optional)
        Positive number of decimals in percent complete
    length - Int (optional)
        Character length of bar
    fill - Str (optional)
        Bar fill character

    Outputs:
    --------
    None

    """

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '░' * (length - filledLength)
    sys.stdout.write('\r%s %s %s%% %s' % (prefix, bar, percent, suffix))
    sys.stdout.flush()

    if iteration == total:
        print()
