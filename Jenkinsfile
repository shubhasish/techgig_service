pipeline{

agent any

stages {
 stage ('Build'){

        steps {
            script{
            sh 'whoami'
            sh 'docker build -t test .'
            }
        }

 }
 stage ('Image Test') {

        steps {
          script{
          sh "docker run -d -name hello_world -p 5000:5000 test"
          sh "curl -X GET http://localhost:5000/techgig/api/hello"
          sh "docker rm hello_world"

          }

        }


 }
 stage ('Push'){

        steps {
          echo "Docker Push"
        }

 }

stage ('Deploy') {

        steps {
            echo "Deploy"

        }

}

}


}