rd /s <project>\.lib
// Linux: rm -rf <project>/.lib

mkdir <project>\.lib
// Linux: \ -> /

virtualenv test

cd test

Scripts\activate.bat
// Linux: source ./bin/activate

pip install -r <project>\requirements.txt

xcopy /E Lib\site-packages <project>\.lib
// Linux: cp -r ./lib/python2.7/site-packages/ <project>/.lib

Scripts\deactivate.bat
// Linux: 結束終端機

cd <project>
// Windows: 請確定磁碟機路徑正確

set
// Linux: export
// 設定環境變數 AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

python server.py
// Linux: sudo su