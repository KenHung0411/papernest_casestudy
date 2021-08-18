### Files explaination
- app.py entrance of everything
- dbService.py connect to db and convert into pandas dataframe
- ftpService.py connect to ftp server and convert into pandas dataframe
- mail.py connect to smtp server and send the mail to a target
- ./output/result.csv the final result


### How to run:
In order to run the code
1. virtualenv your_env
2. soouce your_env/bin/activate
3. pip install -r requirement.txt
4. edit the variable.sh file accrodingly (in production this will be in .gitignore)
5. source variable.sh
6. python app.py