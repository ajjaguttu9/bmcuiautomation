To run this pytest the configuration 

1. browser_name argument should be given in the arguments along with script file and working directly as project directory
   eg: --browser_name = "chrome"
2. The testdata folder is having two files
    i. config.ini - which is having amazon credentials, fill accordingly
    ii. AmazonUI_Test.xlsx - which is test data file from where i took the data
3. In utilities folder chromedriver.exe is placed which is compatible with 117 and newer chrome versions