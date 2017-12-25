pipeline{

agent any

stages {
 stage ('Build'){

        steps {
            script{
            sh 'echo ${env.BRANCH_NAME}'
            sh 'whoami'
            sh 'docker build -t test .'
            }
        }

 }
 stage ('Image Test') {

        steps {
          script{

          sh "docker run -d --name hello_world -p 5000:5000 test"
          sh "sleep 2"
          sh "curl -X GET http://localhost:5000/techgig/api/hello"
          sh "docker stop hello_world"
          sh "docker rm hello_world"
          sh "docker tag test shubhashish/codegladiator:latest"

          }

        }


 }
 stage ('Push'){
        when {
          branch 'master'
        }
        steps {
          withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerhub_id',
usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']]){
          sh "docker login -u $USERNAME -p $PASSWORD"
          sh "docker push shubhashish/codegladiator:latest"

          }
        }

 }

stage ('Deploy') {

        steps {
            echo "Deploy"

        }

}

}


}