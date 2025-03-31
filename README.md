# Aesthetics Toolbox v1.0.2

This project contains Python scripts to run the streamlit application "Aesthetics Toolbox" in your browser. The Toolbox includes an interface to compute a number of commonly studied quantitative image properties (QIPs) for aesthetic research and also contains many common methods for image preprocessing.

#  Scientific paper

A detailed description of the toolbox and the implemented image properties is available here: https://doi.org/10.3758/s13428-025-02632-3. If you use the Aesthetics Toolbox in your work, please consider citing the published paper.

# Cloud version with limited resources (but no installation)

You can test the toolbox without installation on the Streamlit Community Cloud: https://aesthetics-toolbox.streamlit.app/. Please note the privacy and security information below when using the cloud version.

# Local installation instructions

For local installation, download all the files from this GitHub repository to your computer. (Download the ZIP file under the green "Code" button.) Then follow the installation instructions for your operating system:

[Linux and MacOS Installation](docs/InstallationInstructions_Linux_MacOS.md) \
[Windows Installation](docs/InstallationInstructions_Windows.md) 

# Starting the Toolbox locally (after installation)

1. On MacOS and Linux, open a terminal. On Windows open an Anaconda prompt. Navigate to the downloaded folder containing the aesthetics_toolbox.py file.

2. Activate the created Python environment by typing into the terminal:
```shell
conda activate aesthetics_toolbox
```
3. Now start the toolbox with:

```shell
python -m streamlit run aesthetics_toolbox.py
 ```

# Notes on using the Toolbox

1. To restart the Toolbox, just refresh your browser. All loaded data will be removed and all active calculations will stop.

2. If you want to close the toolbox, just close the tab in your browser and the terminal or the Anaconda prompt.

3. While computations are running do not interact with the Toolbox (do not select QIPs, Sidebar, upload or delete images) This would refresh the Toolbox and all calculated data will be lost.

4. Multithreading is not supported, as it would limit platform independence. To speed up calculations, you may want to consider installing the local version, splitting the data, and running multiple instances of the toolbox.

5. The number of images you can load into the toolbox at one time is limited by the amount of RAM on your computer (or the server). Also, large images require more processing time than smaller images.

# Script version of the QIP Machine

The file QIP_machine_script.py is a pure script version (no GUI) of the QIP machine interface of the Toolbox. It can be used to run multiple local instances of the QIP machine or for deployment on an HPC.

# Supplemental material

Detailed information about the data provided in the supplemental material can be found [here](docs/Supplemental_material.md).

# Privacy and security
If you use the local installation version, all calculations and data transfers of the Toolbox will take place on your local computer. The browser is used only as an interface. No data is uploaded to the Internet. The opposite is true for the Streamlit Community Cloud version.

# Contributors
Ralf Bartho: Toolbox concept, code development, maintenance, bugfixes, Development Dataset feature <br />
Christoph Redies: Toolbox concept, supervision of the project, documentation of image properties <br />
Gregor Hayn-Leichsenring: Toolbox concept <br />
Lisa Kossmann, Johan Wagemans: Development Dataset feature <br />
Branka Spehar: Provided code to compute image properties <br />
Ronald Hübner: Provided code to compute image properties <br />
George Mather: Provided code to compute image properties <br />

