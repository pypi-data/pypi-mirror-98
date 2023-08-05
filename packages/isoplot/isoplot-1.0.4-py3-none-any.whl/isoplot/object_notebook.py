"""Module for controlling the Isoplot notebook"""

import io
import datetime
import os
import logging
from pathlib import Path

import ipywidgets as widgets

from isoplot.dataprep import IsoplotData
from isoplot.plots import StaticPlot, InteractivePlot, Map

mod_logger = logging.getLogger(f"isoplot.isoplot_notebook")

class IsoplotNb:

    def __init__(self, verbose=False):

        # Get home directory
        self.home = Path(os.getcwd())

        # Initiate child logger for class instances
        self.logger = logging.getLogger(f"isoplot.isoplot_notebook.IsoplotNb")
        handler = logging.StreamHandler()

        if verbose:
            handler.setLevel(logging.DEBUG)
        else:
            handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)

        if not self.logger.hasHandlers():
            self.logger.addHandler(handler)

        # Initiate all the widgets
        self.uploader = widgets.FileUpload(
        accept='',  # Accepted file extension e.g. '.txt', '.pdf', 'image/*', 'image/*,.pdf'
        multiple=False  # True to accept multiple files upload else False
        )

        self.mduploader = widgets.FileUpload(accept="",
                                             multiple=False)

        self.metadatabtn = widgets.Button(description='Create Template')

        self.datamerge_btn = widgets.Button(description='Submit Template')

        self.displayer = widgets.Output()

        # Initiate object that will control data
        self.data_object = None

    def metadatabtn_eventhandler(self, event):

        self.logger.info("Loading file...")

        uploaded_filename = next(iter(uploader.value))
        content = uploader.value[uploaded_filename]['content']
        with open('myfile', 'wb') as f: f.write(content)

        self.data_object = IsoplotData(io.BytesIO(content))
        self.data_object.get_data()
        self.data_object.generate_template()

        self.logger.info("Done!")

    # TODO
    def get_data_from_upload_btn(self, button):
        """
        :return:
        :rtype:
        """

        # Récupération des datas mis en ligne par le bouton upload
        try:
            data = next(iter(button.value))
        except StopIteration:
            return f"No file loaded in {button}"

        data_content = button.value[data]['content']
        with open('myfile', 'wb') as f:
            f.write(data_content)
        # Entrons les datas dans un dataframe
        try:
            self.logger.debug(f"Reading file from {button.description} as excel")
            real_data = pd.read_excel(io.BytesIO(data_content))
        except Exception as e:
            self.logger.debug('There was a problem reading file')
            self.logger.debug(e)
            try:
                self.logger.info("Trying to load as csv")
                real_data = pd.read_csv(io.BytesIO(data_content), sep=";")
            except Exception as e:
                self.logger.error("There was a problem reading file")
                self.logger.error(e)
            else:
                return real_data
        else:
            return real_data