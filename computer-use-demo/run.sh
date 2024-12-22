set -e

export AWS_PROFILE=default

docker build . -t computer-use-demo:local

docker run \
    -e API_PROVIDER=bedrock \
    -e AWS_PROFILE=$AWS_PROFILE \
    -e AWS_REGION=us-west-2 \
    -v $HOME/.aws:/home/computeruse/.aws \
    -v $HOME/.anthropic:/home/computeruse/.anthropic \
    -v $(pwd)/computer_use_demo:/home/computeruse/computer_use_demo/ \
    -p 5900:5900 \
    -p 8501:8501 \
    -p 6080:6080 \
    -p 8080:8080 \
    -p 8000:8000 \
    -it computer-use-demo:local

