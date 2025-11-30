pipeline {
agent any
stages {
  stage('Build') {
    steps {
      echo 'Building...'
      // Here you can define commands for your build
    }
  }
stage('Test') {
  steps {
    echo 'Testing'
    // Here you can define commands for your tests
  }
}
stage('Deploy') {
  steps {
    echo 'Deploying....'
    // Here you can define commands for your deployment
  }
}
}
}

post{
  //the conditions here will execute after the build is done

  always{
    //this action will happen always regardless of the build reuslt
    echo 'Post build condition running'
  }
  failure{
    //this action will only happen if the build has failed
    echo 'Post Action if build Failed'
  }
}
}
