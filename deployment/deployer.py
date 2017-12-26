import boto3
import yaml
import os
import sys

################# Constants

s3_bucket = "ecs.deployment"

########## Functions
def print_deployment(env,service_name,version,memoryconfig,cpuconfig):
    print "###########################################################"
    print "Environment:\t%s"%env
    print "Service Name:\t%s"%service_name
    print "Service Version:\t%s"%version
    print "Minimum Memory:\t%s"%memoryconfig[0]
    print "Maximum Memory:\t%s"%memoryconfig[1]
    print "Cpu:\t%s"%cpuconfig
    print "##########################################################\n\n"


def uploadFile(client):
    file_list = set(os.listdir(os.path.dirname(os.path.abspath(__file__))))

    file_list.remove(os.path.basename(__file__))
    for file in file_list:
        upload_result = client.s3Upload(file)
        if upload_result:
            pass
        else:
            print upload_result
            os._exit(1)
class client:
    def __init__(self,type,access_id,access_key):
        self.client = boto3.client(type,aws_access_key_id=access_id,aws_secret_access_key=access_key)

    def check_s3(self,path):
        try:
            self.client.get_object(Bucket=s3_bucket,Key=path)
            return True
        except Exception as e:
            if "key does not exist" in e.message:
                return False
            else:
                return e.message

    def create_bucket(self,path):
        try:
            self.client.put_object(Bucket=s3_bucket,Body="",Key=path)
            return True
        except Exception as e:
            return e.message
    def s3Upload(self,file):
        try:
            file_path = os.path.dirname(os.path.abspath(__file__)) + '/' + file
            self.client.upload_file(Bucket=s3_bucket,Filename=file_path,Key=(bucket_path+file))
            return True
        except Exception as e:
            return e.message

    def doesStackExist(self,stackName):
        try:
            self.client.describe_stacks(StackName=stackName)
            return True
        except Exception as e:
            if "Stack with id %s does not exist" % stack_name in e.message:
                return False
            else:
                return e.message

    def create_stack(self,stackName):
        try:
            stack = self.client.create_stack(StackName=stackName,TemplateURL=deployment_path,Parameters=parameters,Capabilities=['CAPABILITY_NAMED_IAM'])
            return (True,stack)
        except Exception as e:
            return (False,e.message)

    def update_stack(self,stackName):
        try:
            stack = self.client.update_stack(StackName=stackName,TemplateURL=deployment_path,Parameters=parameters,Capabilities=['CAPABILITY_NAMED_IAM'])
            return (True,stack)
        except Exception as e:
            return (False,e.message)

### Input

arguments = sys.argv
dict = {}
for x in range(1,len(arguments)):
    arg = arguments[x].split('=')
    dict[arg[0]] = arg[1]

print "\nStarting Application deployemnt to %s\n"%dict['env']
print "Searching for 'deployment.yaml' in your deployment folder."
deployment_file = os.path.dirname(os.path.abspath(__file__)) + "/deployment.yaml"
if os.path.isfile(deployment_file):

    print "deployment.yaml found !!!\n"

    stream = open(deployment_file,"r+")
    yaml = yaml.safe_load(stream)

    service_name = yaml['Parameters']['Application']['Default']
    container_definitions = yaml['Resources']['TaskDefinition']['Properties']['ContainerDefinitions'][0]
    version = 'latest'
    min_memory = container_definitions['MemoryReservation']
    max_memory = container_definitions['Memory']
    cpu= container_definitions["Cpu"]
    print_deployment(dict['env'],service_name,version,(min_memory,max_memory),cpu)




    stack_name = "%s-%s"%(dict['env'],service_name)
    s3_link = "https://s3.amazonaws.com/"
    bucket_path = 'deployment/%s/%s/'%(dict['env'],service_name)
    s3_path = s3_link+bucket_path

#########
    deployment_path = "https://s3.amazonaws.com/%s/deployment/%s/%s/deployment.yaml"%(s3_bucket,dict['env'],service_name)
############################
    parameters = [{'ParameterKey':'Cluster','ParameterValue':dict['env']}]

########################
    s3_client = client('s3',access_id=dict['access_id'],access_key=dict['access_key'])
    print "Checking your deployment folder in s3 bucket %s\n"%s3_bucket
    check_result = s3_client.check_s3(bucket_path)

    if check_result == True:
        print "Deployment folder found"
        print "Uploading all required yaml files to s3"
        uploadFile(s3_client)
    elif check_result == False:
        print "No Deployment folder found. Creating a new one for you."
        create_result = s3_client.create_bucket(bucket_path)
        if create_result:
            print "Uploading all required yaml files"
            uploadFile(s3_client)
        else:
            print create_result
            os._exit(1)
    elif "credentials" in check_result:
        print check_result
        print "\n\nCredentials not supported\""
        os._exit(1)
    else:
        print check_result
        os._exit(1)


    cloudformation_client = client('cloudformation',access_id=dict['access_id'],access_key=dict['access_key'])

    getStack = cloudformation_client.doesStackExist(stack_name)

    if getStack==True:
        print "Service already present in the cluster. Upgrading new configurations\n"
        update_result = cloudformation_client.update_stack(stack_name)
        if update_result[0]:
            print "New configurations updated\n"
            print "Check you stack.Stack Id: %s"%update_result[1]['StackId']

        else:
            print update_result[1]
            os._exit(1)
    elif getStack==False:
        print "Deploying your Application\n"
        create_result = cloudformation_client.create_stack(stack_name)
        if create_result[0]:
            print "Application Deployed\n"
            print "Check you stack.Stack Id: %s" % create_result[1]['StackId']
        else:
            print create_result[1]
            os._exit(1)
else:
    print "No file found"
    os._exit(1)