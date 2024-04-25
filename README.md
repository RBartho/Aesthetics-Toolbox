# Aesthetics Toolbox

This project contains Python scripts to run a streamlit application "SIP machine" in your browser. This application can compute a number of commonly studied SIPs (statistical image properties) for aesthetic research.

# Installation instructions

Download all the files from this GitHub repository to your computer. (Download the ZIP file under the green "Code" button.) Then follow the installation instructions for your operating system:

[Linux Installation](docs/InstallationInstructions_Linux.md) \
[MacOS Installation](docs/InstallationInstructions_MacOS.md)  \
[Windows Installation](docs/InstallationInstructions_Windows.md) 

# Starting the application (after installation)

1. On MacOS and Linux open a terminal, on Windows open a Anaconda Prompt. Navigate to the downloaded folder containing the SIP_machine.py file.

2. Activate the created Python environment by typing into the terminal
```shell
conda activate SIP_machine
```
3. Now start the application with:

```shell
python -m streamlit run SIP_machine.py
 ```

# Notes on using the application

1. If you want to restart the app, just refresh your browser. All loaded data will be removed and all active calculations will stop.

2. If you want to close the app, just close the tab in your browser and the terminal or Anaconda Prompt.

3. While SIP-computations are running do not interact with the application (e.g. selecting SIPs, Sidebar, uploading or deleting images) This would refresh the application and all progress will be lost.

4. Multithreading is not supported as it would limit platform independence. To speed up calculations, you may want to consider splitting the data and running multiple instances of the application.

5. The number of images you can load into the application at one time is limited by the amount of RAM your computer has. Also, large images require much more processing time than smaller images.

# Privacy and security
All calculations and data transfers of the application take place on your local computer. The browser is only used as an interface. No data is uploaded to the Internet.
