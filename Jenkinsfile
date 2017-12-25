pipeline{

agent any

stages {
 stage ('Build'){

        steps {
            def app = docker.build('test_image')
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