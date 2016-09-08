## LAB-SNSPC ##

Lambda API Backend - Search Naver Shopping Product Code

### Introduction ###

쇼핑몰 상품코드와 매칭되는 네이버 쇼핑의 상품코드를 검색하는 API Gateway lambda backend<br />
검색된 결과는 csv 파일로 다운로드

### Version ###
- Python: 2.7.6

### Utility ###
- python-lambda
	- Python-lambda is a toolset for developing and deploying serverless Python code in AWS Lambda.
	- [https://github.com/nficano/python-lambda](https://github.com/nficano/python-lambda)

### Installation ###
- install virtualenv <br />
```
sudo pip install virtualenv
```
- activate virtual env <br /> 
```
source venv/bin/activate
```
- install python package <br />
```
pip install -r requirements.txt
```

### Message Flow ###
![](https://docs.google.com/drawings/d/1Izfq5YqPr7txhh106aMk5wUpz4mQ7FIhgoo6Q6PgDvM/pub?w=1231&h=843)

### Configuration ###
- config.yaml: python-lambda utility configuration file
	- region: lambda fucntion region
	- function_name: lambda function name
	- handler: lambda function handler
	- role: lambda function role
	- description: lambda function description
	- aws_access_key_id: aws access key
	- aws_secret_access_key: aws sercet key
	- timeout: lambda function timeout seconds
	- memory_size: lambda memory size
- config.py: lambda function configuration file
	- s3_bucket: s3 bucket name for upload result csv
	- s3_file_prefix: s3 object prefix
	- naver_api_url: naver open api endpoint url
	- naver_api_key: naver open api key
- event.json: lambda function event values (for test)

### lambda Test ###
- ```lambda invoke -v```

### lambda deployment ###
- ```lambda deploy```
