import numpy as np
import json
import zipfile
from PIL import Image
from os import path
import logging
import h5py
from datetime import datetime
from synbols.stratified_splits import make_default_splits


def load_npz(file_path):
    """Load the dataset from compressed numpy format (npz)."""
    dataset = np.load(file_path, allow_pickle=True)
    return dataset['x'], dataset['mask'], dataset['y']


def write_npz(file_path, generator):
    x, mask, y = zip(*list(generator))
    x = np.stack(x)
    mask = np.stack(mask)

    logging.info("x: %s, %s, mask: %s, %s",
                 x.shape,
                 x.dtype,
                 mask.shape,
                 mask.dtype)
    logging.info("Saving dataset in %s.", file_path)
    np.savez(file_path, x=x, y=y, mask=mask)


class H5Stack:
    def __init__(self,
                 file,
                 name,
                 n_samples,
                 chunk_size=10,
                 compression="gzip"):
        self.dset = None
        self.file = file
        self.name = name
        self.n_samples = n_samples
        self.chunk_size = chunk_size
        self.compression = compression
        self.i = 0

    def add(self, x):

        # create it based on x's information
        if self.dset is None:

            if isinstance(x, str):
                shape = ()
                dtype = h5py.string_dtype(encoding='ascii')
            else:
                shape = x.shape
                dtype = x.dtype

            self.dset = self.file.create_dataset(
                self.name,
                (self.n_samples,) + shape,
                dtype=dtype,
                maxshape=(self.n_samples,) + shape,
                chunks=(self.chunk_size,) + shape,
                compression=self.compression)

        dset = self.dset
        if self.i >= dset.shape[0]:
            dset.resize(dset.shape[0] + self.chunk_size, 0)

        dset[self.i] = x
        self.i += 1


# chunk, compressed, no-n_samples:
#    write speed = 8 ms / image (including creation of image)
# no-chunk, compressed, n_samples:
#    write speed = 113 ms / image (including creation of image)
# chunk, compressed, n_samples: write speed = 8 ms / image

# chunked(100), read speed = 0.15 ms / image

def add_splits(fd, split_dict, random_seed):
    for split_name, split in split_dict.items():
        ds = fd.create_dataset("split/%s" % split_name, data=split)
        ds.attrs['timestamp'] = datetime.now().strftime("%Y-%b-%d_%H:%M:%S")
        ds.attrs['seed'] = random_seed


def write_h5(file_path,
             dataset_generator,
             n_samples,
             split_function=None,
             ratios=(0.6, 0.2, 0.2),
             random_seed=42):
    with h5py.File(file_path, 'w', libver='latest') as fd:
        x_stack = H5Stack(fd, 'x', n_samples)
        mask_stack = H5Stack(fd, 'mask', n_samples)
        y_stack = H5Stack(fd, 'y', n_samples)

        for i, (x, mask, y) in enumerate(dataset_generator):
            x_stack.add(x)
            mask_stack.add(mask)
            attr_str = json.dumps(y)
            # logging.info("attr_str len = %d", len(attr_str))
            y_stack.add(attr_str)

        attr_list = [json.loads(attr) for attr in fd['y']]

        if split_function is None:
            split_function = make_default_splits

        add_splits(fd,
                   split_function(attr_list, ratios, random_seed),
                   random_seed)


def load_h5(file_path):
    """Load the dataset from h5py format

    Args:
        file_path: path to the hdf5 dataset

    Returns:
        x: array of shape (n_samples, width, height, n_channels), \
    containing images
        mask: array of shape (n_samples, width, height, n_symbols), \
    containing the mask of each symbol in the image
        attributes: list of length n_samples, containing a dictionary \
    of attributes for each images
        splits: dict of different type of splits for this dataset. \
    Each split is a list of mask for each subset.
    """

    with h5py.File(file_path, 'r') as fd:
        y = [json.loads(attr) for attr in fd['y']]

        splits = {}
        if 'split' in fd.keys():
            for key in fd['split'].keys():
                splits[key] = np.array(fd['split'][key])

        return np.array(fd['x']), np.array(fd['mask']), y, splits


def load_attributes_h5(file_path):
    """Load the dataset from h5py format

    Args:
        file_path: path to the hdf5 dataset

    Returns:
        attributes: list of length n_samples, \
    containing a dictionary of attributes for each images
        splits: dict of different type of splits for this dataset. \
    Each split is a binary array of shape \
    (n_samples, n_subset) representing a specific partition.
    """
    with h5py.File(file_path, 'r') as fd:
        y = [json.loads(attr) for attr in fd['y']]
        # y = list(fd['y'])
        splits = {}
        if 'split' in fd.keys():
            for key in fd['split'].keys():
                splits[key] = np.array(fd['split'][key])

        return y, splits


def load_minibatch_h5(file_path, indices):
    with h5py.File(file_path, 'r') as fd:
        x = np.array(fd['x'][indices])
        mask = np.array(fd['mask'][indices])
    return x, mask


def load_dataset_jpeg_sequential(file_path, max_samples=None):
    logging.info("Opening %s" % file_path)
    with zipfile.ZipFile(file_path) as zf:

        name_list = zf.namelist()

        x, y = None, None

        n_samples = 0

        for name in name_list:
            with zf.open(name) as fd:

                prefix, ext = path.splitext(name)
                if ext == '.jpeg':
                    img = Image.open(fd)
                    x = np.array(img)
                    prefix_jpeg = prefix

                    if n_samples % 1000 == 0:
                        logging.info("loading sample %d" % n_samples)

                if ext == '.json':
                    y = json.load(fd)
                    prefix_json = prefix

                if x is not None and y is not None:
                    assert prefix_jpeg == prefix_json
                    yield x, y
                    x, y = None, None
                    n_samples += 1
                    if max_samples is not None and n_samples >= max_samples:
                        break


def pack_dataset(generator):
    """Turn a the output of a generator of (x,y) pairs \
    into a numpy array containing the full dataset
    """
    x, mask, y = zip(*generator)
    return np.stack(x), np.stack(mask), y


def write_jpg_zip(directory, generator):
    """Write the dataset in a zipped directory using \
    jpeg and json for each image.
    """
    with zipfile.ZipFile(directory + '.zip', 'w') as zf:
        for i, (x, x2, y) in enumerate(generator):
            name = "%s/%07d" % (directory, i)
            with zf.open(name + '.jpeg', 'w') as fd:
                Image.fromarray(x).save(fd, 'jpeg', quality=90)
            if x2 is not None:
                with zf.open(name + '_gt.jpeg', 'w') as fd:
                    Image.fromarray(x2).save(fd, 'jpeg', quality=90)
            zf.writestr(name + '.json', json.dumps(y))
