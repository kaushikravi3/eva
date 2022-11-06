pipeline {
  agent none
  
  options{
     buildDiscarder(logRotator(numToKeepStr: '8', daysToKeepStr: '20'))
  }
  
  environment {
    HOME = pwd(tmp:true)
  }
  
  stages {
  
    stage('Setup and Install Packages') {
      parallel {
        stage('Setup Virtual Environment') {
          agent {
      dockerfile {
        filename 'docker/jenkins.Dockerfile'
        args '--gpus all'
      }
    }
          steps {
            sh '''python3 -m venv env37
                  . env37/bin/activate
                  pip install --upgrade pip
                  pip install scikit-build
                  pip install cython
                  pip install -e ."[dev]"
              '''
          }
        }
        stage('Generate Parser Files') {
          agent any
          steps {
            sh 'sh script/antlr4/generate_parser.sh'
          }
        }
      }
    }

    stage('CUDA GPU Check') {
    agent {
      dockerfile {
        filename 'docker/jenkins.Dockerfile'
        args '--gpus all'
      }
    }
      steps {
          sh '''. env37/bin/activate
                python3 -c "import torch; torch.cuda.current_device()"
             '''
      }
    }

    stage('Run Tests') {
    agent {
      dockerfile {
        filename 'docker/jenkins.Dockerfile'
        args '--gpus all'
      }
    }
      steps {
        sh '''. env37/bin/activate
              sh script/test/test.sh
           '''
       }
     }

    stage('Coverage Check') {
    agent {
      dockerfile {
        filename 'docker/jenkins.Dockerfile'
        args '--gpus all'
      }
    }
      steps {
        sh '''. env37/bin/activate
          coveralls'''
      }
    }
  }
}
