# Installation instructions MacOS

1. If you do not already have Anaconda or Miniconda installed, download and install Anaconda (use default install options):

	https://www.anaconda.com/download

2. Open a terminal on your system. If you do not know how to do this on your system, google it :-).

3. Navigate to the downloaded files in the terminal window. If you do not know how to change folders in terminal, google it :-). 

4. In the same folder where the file "requirements.txt" is, run this command in the terminal:

```shell
conda create --name SIP_machine -y
```

This should create a python enviroment with the name "SIP_machine".  


5. Activate the new environment by typing into the terminal:

```shell
conda activate SIP_machine
```

6. Install all needed python packages into the new python enviroment by:

```shell
conda install --file requirements.txt -y
```
	
7. Now launch the streamlit application from the terminal in the same folder as above:

```shell
python -m streamlit run SIP_machine.py
```


Your default browser should open the application on your local machine. It should look like this: 
![Screenshot](https://github.com/RBartho/SIPmachine/tree/main/images/toolbox_screenshot.png)
The browser is only used as an interface. No data is uploaded to the Internet.

![back](https://github.com/RBartho/SIPmachine)

