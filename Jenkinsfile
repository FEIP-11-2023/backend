pipeline {
    agent any

    environment {
        PATH = "$PATH:/usr/local/bin"
        gpg_secret = credentials("gpg-secret")
        gpg_trust = credentials("gpg-ownertrust")
        gpg_passphrase = credentials("gpg-passphrase")
    }

    stages {
        stage("Deploy Prod") {
            when {
                branch "master"
            }
            steps {
                sh """
                    gpg --batch --import $gpg_secret
                    gpg --import-ownertrust $gpg_trust
                    git secret reveal -p '$gpg_passphrase'
                """
                echo "Deploying and Building..."
//                 notifyEvents message: "#News_Backend 🛠 Building New Container...", token: '7yi9o1VBd3mz-JP2JhQOICo3Y5zgPHGk'
                sh "docker-compose build"
//                 notifyEvents message: "#News_Backend ⛔️️ Stopping Previous Container...", token: '7yi9o1VBd3mz-JP2JhQOICo3Y5zgPHGk'
                echo "Starting new containers..."
//                 notifyEvents message: "#News_Backend 🐳 Upping New Container...", token: '7yi9o1VBd3mz-JP2JhQOICo3Y5zgPHGk'
                sh "docker-compose up -d"
                echo "Deployed!"
            }
        }
    }
}