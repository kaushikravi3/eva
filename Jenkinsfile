pipeline {
  agent {
    dockerfile {
      filename 'docker/eva_jenkins.Dockerfile'
    }

  }
  stages {
    stage('Setup and Install Packages') {
      parallel {
        stage('Setup Virtual Environment') {
          steps {
            sh '''python3 -m venv env37
. env37/bin/activate
pip install --upgrade pip
pip install scikit-build
pip install cython
pip install -e ."[dev]"'''
          }
        }

        stage('Generate Parser Files') {
          steps {
            sh 'sh script/antlr4/generate_parser.sh'
          }
        }

      }
    }

    stage('CUDA GPU Check') {
      steps {
        sh '''. env37/bin/activate
python3 -c "import torch; torch.cuda.current_device()"'''
      }
    }

    stage('Run Tests') {
      steps {
        sh '''. env37/bin/activate
sh script/test/test.sh'''
      }
    }

    stage('Coverage Check') {
      steps {
        sh '''. env37/bin/activate
coveralls'''
      }
    }
  }
}
