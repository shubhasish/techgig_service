pipeline{

agent any

stages {
 stage ('Build'){

        steps {
            script{

            sh 'docker build -t hellowolrd .'

            }
        }

 }
 stage ('Image Test') {

        steps {
          script{

          sh "docker run -d --name hello_world -p 5000:5000 helloworld"
          sh "sleep 2"
          sh "curl -X GET http://localhost:5000/techgig/api/hello"
          sh "sleep 1"
          sh "curl -X GET http://localhost:5000/techgig/healthCheck"
          sh "docker stop hello_world"
          sh "docker rm hello_world"
          sh "docker tag helloworld shubhashish/codegladiator:latest"
          sh "docker tag helloworld shubhashish/codegladiator:${env.BRANCH_NAME}-${env.BUILD_ID}"

          }

        }


 }
 stage ('Push'){

        steps {
          withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerhub_id',
usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']]){
          sh "docker login -u $USERNAME -p $PASSWORD"
          sh "docker push shubhashish/codegladiator:latest"

          }
        }

 }

stage ('Deploy') {
        agent {
          dockerfile{
            filename 'Dockerfile'
            dir 'deployment'

          }
        }
        steps {
            withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'aws_id',
usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']]){
          sh "python deployment/deployer.py env=dev access_id=$USERNAME access_key=$PASSWORD region=us-east-1 version=${env.BRANCH_NAME}-${env.BUILD_ID}"

          }


        }

}

stage ('Cleanup') {
    steps{
        script{
        sh "docker rmi shubhashish/codegladiator:latest"
        sh "docker rmi shubhashish/codegladiator:${env.BRANCH_NAME}-${env.BUILD_ID}"
        sh "docker rmi helloworld"

        }

    }

}

}


}