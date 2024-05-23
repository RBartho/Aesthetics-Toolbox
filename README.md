# Aesthetics Toolbox

### (This is still a beta version and should be used with caution. Bugfixes have not been completed. No warranties.)

This project contains Python scripts to run a streamlit application "Aesthetics Toolbox" in your browser. This application can compute a number of commonly studied QIPs (quantitative image properties) for aesthetic research.

# Cloud version with limited resources (but no installation)

You can try the toolbox without installation on the streamlit community cloud: https://aesthetics-toolbox.streamlit.app/ Please note the privacy and security information below when using the cloud version.

# Local installation instructions

For local installation download all the files from this GitHub repository to your computer. (Download the ZIP file under the green "Code" button.) Then follow the installation instructions for your operating system:

[Linux Installation](docs/InstallationInstructions_Linux_MacOS.md) \
[Windows Installation](docs/InstallationInstructions_Windows.md) 

# Starting the toolbox local (after installation)

1. On MacOS and Linux open a terminal, on Windows open a Anaconda Prompt. Navigate to the downloaded folder containing the aesthetics_toolbox.py file.

2. Activate the created Python environment by typing into the terminal
```shell
conda activate aesthetics_toolbox
```
3. Now start the application with:

```shell
python -m streamlit run aesthetics_toolbox.py
 ```

# Notes on using the application

1. If you want to restart the app, just refresh your browser. All loaded data will be removed and all active calculations will stop.

2. If you want to close the app, just close the tab in your browser and the terminal or Anaconda Prompt.

3. While computations are running do not interact with the application (e.g. selecting QIPs, Sidebar, uploading or deleting images) This would refresh the application and all progress will be lost.

4. Multithreading is not supported as it would limit platform independence. To speed up calculations, you may want to consider installing the local version, splitting the data and running multiple instances of the application.

5. The number of images you can load into the application at one time is limited by the amount of RAM your computer (or the server) has. Also, large images require much more processing time than smaller images.

# Privacy and security
If you use the local installation version, all calculations and data transfers of the application take place on your local computer. The browser is used only as an interface. No data is uploaded to the Internet. The opposite is true for the Streamlit Community Cloud version.

# Contributors
Ralf Bartho: Toolbox concept, code development, maintenance, bugfixes <br />
Christoph Redies: Toolbox concept, supervision of the project, documentation of image properties <br />
Gregor Hayn-Leichsenring: Advice on the development of the toolbox <br />
Branka Spehar: Provided code to compute image properties <br />
Ronald Hübner: Provided code to compute image properties <br />
George Mather: Provided code to compute image properties <br />
