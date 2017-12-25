pipeline{

agent any

stages {
 stage ('Build'){

        steps {
            script{
            sh 'docker build -t test .'
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