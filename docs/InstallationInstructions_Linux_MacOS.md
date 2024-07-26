# Installation instructions for Linux and MacOS

1. If you do not already have Anaconda or Miniconda installed, download and install Anaconda (use all default install options):

	https://www.anaconda.com/download

2. Open a terminal on your system. If you do not know how to do this in your operating system, google it :-).

3. Change to the folder that contains the "requirements.txt" file that you downloaded from Github (by using the "cd" command). If you do not know how to change folders in a terminal, google it :-). 

4. In the folder that contains the file "requirements.txt", run the following command in the terminal:

```shell
conda create --name aesthetics_toolbox -y
```

This should create a python enviroment with the name "aesthetics_toolbox".  


5. Activate the new environment by typing into the terminal:

```shell
conda activate aesthetics_toolbox
```

6. Install all needed python packages into the new python enviroment by:

```shell
conda install --file requirements.txt -y
```
	
7. Now launch the Streamlit application from the terminal in the same folder as above:

```shell
python -m streamlit run aesthetics_toolbox.py
```

Your default browser should open the application on your local machine. It should look like this: 
![Screenshot](https://github.com/RBartho/Aesthetics-Toolbox/tree/main/images/toolbox_screenshot.png).
The browser is used as an interface only. No data is uploaded to the Internet.

![Back](https://github.com/RBartho/Aesthetics-Toolbox)
