LOCAL_NAME=smile-innovation/chatbot/countrybot-oversnips
AWS_NAME=274275471339.dkr.ecr.us-east-1.amazonaws.com/smile-innovation/chatbot/countrybot-oversnips:latest

default: local

local:
	@docker build -t ${LOCAL_NAME} .

aws:
	@$(aws ecr get-login --no-include-email --region us-east-1)
	@docker tag ${LOCAL_NAME} ${AWS_NAME}
	@docker push ${AWS_NAME}
