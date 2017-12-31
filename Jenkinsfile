pipeline{

agent any

stages {
 stage ('Build'){

        steps {
            script{
            def full_name=env.JOB_NAME.split('/')
            def job_name=full_name[0]
            sh "docker build -t ${job_name}:${env.BRANCH_NAME} ."

            }
        }

 }
 stage ('Testing') {

        steps {
          script{

          def full_name = env.JOB_NAME.split('/')
          def job_name = full_name[0]
          sh "docker run -d --name ${job_name}_${env.BRANCH_NAME} -p 5000:5000 ${job_name}:${env.BRANCH_NAME}"
          sh "sleep 2"
          sh "curl -X GET http://localhost:5000/techgig/api/hello"
          sh "sleep 1"
          sh "curl -X GET http://localhost:5000/techgig/healthCheck"
          sh "docker stop ${job_name}_${env.BRANCH_NAME}"
          sh "docker rm ${job_name}_${env.BRANCH_NAME}"
          sh "docker tag ${job_name}:${env.BRANCH_NAME} shubhashish/${job_name}:latest"
          sh "docker tag ${job_name}:${env.BRANCH_NAME} shubhashish/${job_name}:${env.BRANCH_NAME}-${env.BUILD_ID}"

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
             script{
                     def ful_name = env.JOB_NAME.split('/')
                     def job_name = full_name[0]
                     sh "echo {full_name}"
                     withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerhub_id',usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']]){
                     sh "echo {full_name}"
                     sh "docker login -u $USERNAME -p $PASSWORD"
                     sh "docker push shubhashish/${job_name}:latest"
                     sh "docker push shubhashish/${job_name}:${env.BRANCH_NAME}-${env.BUILD_ID}"
}
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

            withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'aws_id', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']]){
             sh "python deployment/deployer.py env=${env.BRANCH_NAME} access_id=$USERNAME access_key=$PASSWORD region=us-east-1 version=${env.BRANCH_NAME}-${env.BUILD_ID}"

          }

}
        }

}

stage ('Cleanup') {
    steps{
        script{
        def full_name = env.JOB_NAME.split('/')
        def job_name = full_name[0]

        sh "docker rmi shubhashish/${job_name}:latest"
        sh "docker rmi shubhashish/${job_name}:${env.BRANCH_NAME}-${env.BUILD_ID}"
        sh "docker rmi ${job_name}:${env.BRANCH_NAME}"

        }

    }

}

}


}