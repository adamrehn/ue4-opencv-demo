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
				JENKINS_CONAN_SERVER = credentials('jenkins-conan-server')
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
						//Invoke our build script inside the container, configuring conan to retrieve our dependency packages from the correct remote
						windowsContainer('adamrehn/ue4-full:4.19.1', '-m 8GB',
						[
							'conan remote add jenkins "%JENKINS_CONAN_SERVER%"',
							'cd project\\OpenCVDemo',
							'ue4 uat BuildCookRun -noP4 -clientconfig=Shipping -serverconfig=Shipping -cook -allmaps -build -stage -prereqs -pak -archive -archivedirectory="%cd%\\dist"',
							'7z a OpenCVDemo.Win64.zip .\\dist'
						])
					}
					post
					{
						success {
							archiveArtifacts artifacts: 'project/OpenCVDemo/OpenCVDemo.Win64.zip'
						}
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
						//Invoke our build script inside the container, configuring conan to retrieve our dependency packages from the correct remote
						sh 'conan remote add jenkins "$JENKINS_CONAN_SERVER"'
						sh 'cd project/OpenCVDemo && ue4 uat BuildCookRun -noP4 -clientconfig=Shipping -serverconfig=Shipping -cook -allmaps -build -stage -prereqs -pak -archive -archivedirectory="`pwd`/dist"'
						sh 'cd project/OpenCVDemo && zip -r OpenCVDemo.Linux.zip ./dist'
					}
					post
					{
						success {
							archiveArtifacts artifacts: 'project/OpenCVDemo/OpenCVDemo.Linux.zip'
						}
						cleanup {
							cleanWs()
						}
					}
				}
			}
		}
	}
}
