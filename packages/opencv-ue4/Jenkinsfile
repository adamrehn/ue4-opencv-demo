//Load the helper code for running Windows containers, since Jenkins does not yet feature native support
library identifier: 'jenkins-pipeline-utils@master', retriever: modernSCM([$class: 'GitSCMSource', remote: 'https://github.com/adamrehn/jenkins-pipeline-utils.git'])

pipeline
{
	agent none
	
	stages
	{
		stage('Build')
		{
			environment
			{
				//We need to preconfigure our conan server details in Jenkins
				JENKINS_CONAN_SERVER   = credentials('jenkins-conan-server')
				JENKINS_CONAN_USERNAME = credentials('jenkins-conan-username')
				JENKINS_CONAN_PASSWORD = credentials('jenkins-conan-password')
			}
			parallel
			{
				stage('Windows Build')
				{
					agent
					{
						//We require an agent capable of running Windows Docker containers
						label 'windows-containers'
					}
					steps
					{
						//Invoke our build script inside the container, configuring conan to upload the built package to the correct remote
						windowsContainer('adamrehn/ue4-full:4.19.1', '',
						[
							'conan remote add jenkins "%JENKINS_CONAN_SERVER%"',
							'conan user -p "%JENKINS_CONAN_PASSWORD%" -r jenkins "%JENKINS_CONAN_USERNAME%"',
							'cd packages\\opencv-ue4 && python build.py --upload=jenkins'
						])
					}
					post
					{
						cleanup {
							cleanWs()
						}
					}
				}
				stage('Linux Build')
				{
					agent
					{
						docker
						{
							//We require an agent capable of running Linux Docker containers
							label 'linux-containers'
							image 'adamrehn/ue4-full:4.19.1'
						}
					}
					steps
					{
						//Invoke our build script inside the container, configuring conan to upload the built package to the correct remote
						sh 'conan remote add jenkins "$JENKINS_CONAN_SERVER"'
						sh 'conan user -p "$JENKINS_CONAN_PASSWORD" -r jenkins "$JENKINS_CONAN_USERNAME"'
						sh 'cd packages/opencv-ue4 && python3 build.py --upload=jenkins'
					}
					post
					{
						cleanup {
							cleanWs()
						}
					}
				}
			}
		}
	}
}
