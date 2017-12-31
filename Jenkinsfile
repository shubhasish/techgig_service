pipeline{

agent any

stages {
 stage ('Build'){

        steps {
            script{
            def full_name=env.JOB_NAME.split('/')
            def job_name=full_name[0]

            sh "docker build -t ${job_name} ."

            }
        }

 }
 stage ('Testing') {

        steps {
          script{
          sh "echo ${env.HELLO}"
          sh "docker run -d --name hello_world_${env.BRANCH_NAME} -p 5000:5000 helloworld:${env.BRANCH_NAME}"
          sh "sleep 2"
          sh "curl -X GET http://localhost:5000/techgig/api/hello"
          sh "sleep 1"
          sh "curl -X GET http://localhost:5000/techgig/healthCheck"
          sh "docker stop hello_world_${env.BRANCH_NAME}"
          sh "docker rm hello_world_${env.BRANCH_NAME}"
          sh "docker tag helloworld:${env.BRANCH_NAME} shubhashish/codegladiator:latest"
          sh "docker tag helloworld:${env.BRANCH_NAME} shubhashish/codegladiator:${env.BRANCH_NAME}-${env.BUILD_ID}"

          }

        }


 }
 stage ('Push'){
        when {
            anyOf{
                branch 'dev'
                branch 'staging'
                branch 'master'
             }
        }
        steps {
          withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerhub_id',
usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']]){
          sh "docker login -u $USERNAME -p $PASSWORD"
          sh "docker push shubhashish/codegladiator:latest"
          sh "docker push shubhashish/codegladiator:${env.BRANCH_NAME}-${env.BUILD_ID}"

          }
        }

 }

stage ('Deploy') {
        when {
            anyOf{
                branch 'dev'
                branch 'staging'
                branch 'master'
             }
        }

        agent {
          dockerfile{
            filename 'Dockerfile'
            dir 'deployment'

          }
        }
        steps {
            script{
              if (env.BRANCH_NAME == 'master') {
                                                    environment{
                                                    DEPLOY_TO = "production"
                                                    }
                                            } else {
                                                    DEPLOY_TO = "${env.BRANCH_NAME}"
                                            }


            }


            withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'aws_id',
usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']]){
          sh "python deployment/deployer.py env=${env.BRANCH_NAME} access_id=$USERNAME access_key=$PASSWORD region=us-east-1 version=${env.BRANCH_NAME}-${env.BUILD_ID}"

          }


        }

}

stage ('Cleanup') {
    steps{
        script{
        sh "docker rmi shubhashish/codegladiator:latest"
        sh "docker rmi shubhashish/codegladiator:${env.BRANCH_NAME}-${env.BUILD_ID}"
        sh "docker rmi helloworld:${env.BRANCH_NAME}"

        }

    }

}

}


}