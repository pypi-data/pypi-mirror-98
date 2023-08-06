# -*- coding: utf-8 -*-
##########################################################################
# NSAp - Copyright (C) CEA, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Module that provides functions to prepare the MINST dataset.
"""

# Imports
import os
import json
import logging
import torchvision
import torchvision.transforms as transforms
from collections import namedtuple
from collections import OrderedDict
import numpy as np
import pandas as pd
import urllib
from pynet.datasets import Fetchers


# Global parameters
Item = namedtuple("Item", ["input_path", "output_path", "metadata_path"])
logger = logging.getLogger("pynet")


@Fetchers.register
def fetch_minst(datasetdir):
    """ Fetch/prepare the MINST dataset for pynet.

    Parameters
    ----------
    datasetdir: str
        the dataset destination folder.

    Returns
    -------
    item: namedtuple
        a named tuple containing 'input_path', and 'metadata_path'.
    """
    logger.info("Loading minst dataset.")
    if not os.path.isdir(datasetdir):
        os.mkdir(datasetdir)
    desc_path = os.path.join(datasetdir, "pynet_minst.tsv")
    input_path = os.path.join(datasetdir, "pynet_minst_inputs.npy")
    if not os.path.isfile(desc_path):
        transform = transforms.Compose([
            transforms.ToTensor()
        ])
        logger.info("Getting train dataset.")
        trainset = torchvision.datasets.MNIST(
            root=datasetdir,
            train=True,
            download=True,
            transform=transform)
        logger.info("Getting test dataset.")
        testset = torchvision.datasets.MNIST(
            root=datasetdir,
            train=False,
            download=True,
            transform=transform)
        metadata = dict((key, []) for key in ("label", ))
        data = []
        for loader in (trainset, testset):
            for arr, label in loader:
                logger.debug("Processing {0} {1}...".format(label, arr.shape))
                data.append(arr.numpy())
                metadata["label"].append(label)
        data = np.asarray(data)
        np.save(input_path, data)
        df = pd.DataFrame.from_dict(metadata)
        df.to_csv(desc_path, sep="\t", index=False)
    return Item(input_path=input_path, output_path=None,
                metadata_path=desc_path)
