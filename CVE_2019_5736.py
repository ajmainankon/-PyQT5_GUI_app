import subprocess


def get_name():
	return "CVE-2019-5736"


def check():
	log = ""
	try:
		cmd = 'docker --version'
		output = subprocess.check_output(cmd, shell=True).decode()
		#print(output)
		log += "docker version :" + output
		docker_version = output.strip().split()[2].split(',')[0]
		if docker_version < '18.09.3':
			log += "Vulnerable to the runc vulnerability" + "\n"
			return True, log
		else:
			log += "Safe from the runc vulnerability" + "\n"
			return False, log
	except Exception as e:
		log += "Docker not installed" + "\n"
		log += str(e)
		return False, log
	
def fix():
	vuln, log = check()
	try:
		if vuln:
			cmd = "yes | sudo apt install apt-transport-https ca-certificates curl software-properties-common && \
				yes | curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -  && \
				yes | sudo add-apt-repository 'deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable'"
			subprocess.run(cmd, shell=True) # get latest packages available
			get_versions = "sudo apt-get update && apt-cache madison docker-ce | awk '{ print $3 }'"
			output = subprocess.check_output(get_versions, shell=True).decode()
			for line in output.split("\n"):
				if '18.09.3' in line:
					version = line
					break
			log += version + "\n"
			bump = "VERSION_STRING=" + version + " && yes | sudo apt-get install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin"
			subprocess.run(bump, shell=True)
			cmd = 'docker --version'
			output = subprocess.check_output(cmd, shell=True).decode()
			log += "Docker version upgraded to "+output +"\n"
			return True, log
		else:
			return False, log
	except Exception as e:
		log += str(e)
		return False, log

#fix()
