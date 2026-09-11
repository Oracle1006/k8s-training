pipeline {
	agent none
	environment {
		REGISTRY = 'k8straining123.azurecr.io'
		IMAGE_NAME = 'myapp'
		K8S_NAMESPACE = 'demo'
		DEPLOYMENT = 'myapp'
		CONTAINER = 'myapp'
		}	
	stages {
		stage('Checkout') {
			agent { label 'built-in' }
			steps {
				checkout scm
		      		}
			}	
		stage('Build Image') {
			agent { label 'docker-agent' }
			steps {
				sh '''
				set -e
				docker build -t ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} -t ${REGISTRY}/${IMAGE_NAME}:latest .
				'''
				}				
			}

		stage('Security Scan') {
			agent { label 'docker-agent' }
			steps {
				sh '''
				set -e
				trivy image --severity HIGH,CRITICAL --exit-code 0 ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
				'''
				}
			     }

		stage('Push Image') {
    		agent { label 'docker-agent' }
    		steps {
        		withCredentials([
            		usernamePassword(
                		credentialsId: '3875eee5-a9cb-4ab2-b4ed-68d58f66d853',
                		usernameVariable: 'ACR_USER',
                		passwordVariable: 'ACR_PASSWORD'
            		)
        		]) {
            		sh '''
                		set -e

                		echo "$ACR_PASSWORD" | docker login ${REGISTRY} \
                    		--username "$ACR_USER" \
                    		--password-stdin

                		docker push ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
                		docker push ${REGISTRY}/${IMAGE_NAME}:latest

                		docker logout ${REGISTRY}
            		'''
        		}
    		}	
		}

		stage('Deploy to Kubernetes') {
			agent { label 'built-in' }
			steps {
				withKubeConfig([
				credentialsId: 'config'
				]) 
				{
					sh '''
    					set -e

    					kubectl -n ${K8S_NAMESPACE} set image \
        					deployment/${DEPLOYMENT} \
        					${CONTAINER}=${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}

    					kubectl -n ${K8S_NAMESPACE} rollout status \
        					deployment/${DEPLOYMENT} \
        					--timeout=180s
					'''
					}
				}
			}
		}
	
	post {
		success {
			echo "Deployment succeeded."
			echo "Image: ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}"
			}
		failure {
			echo "Pipeline failed. Review the stage logs."
			}
		always {
			sh 'docker image prune -f || true'
			}
		}
    }
