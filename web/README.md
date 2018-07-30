## How to run

Go where `manage.py` is and run `bash run.sh`. This time that file is under **_base** which is the django project name. App name is **artia**. If you are using *virtualenvwrapper*, you can easily make virtual python environment by specifying virtual environment name like `bash run.sh artia-web-tool`.

Default admin name is **admin** and password is changable by editing *superuserpass.txt*.

If You wnat to clean all, run `bash run.sh clean`. Fail error about removing directory is normal. After cleaning cmd, you chould run `bash run.sh` in virualenv. This command does not remove virtualenv.

## How to use

With running development server, you can see Bart Simpson and Lisa Simpson at home. This time user management is wroking, but any anonymous user can use all features of website like uploading file, requesting POST with json coordinates and so on.

### First Step: Upload file to process

Click `컷 올리기`, and you can upload file with descriptions. You can upload multiple files. Leave Coordinates field empty. This field will be filled in next step by clicking on image. If upload file process succeed, you can see all your files you've uploaded. Click file you've just uploaded. mark some points for you to cut and click the button *Save*, then server will print coordinates what you sent.

## requirement

Check out `_base/requirement.txt`
