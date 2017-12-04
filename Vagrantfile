# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/xenial64"
  
  config.vm.provider "virtualbox" do |vb|
    vb.name = 'imgmatch.dev'
  end
  
  # Set machine name
  config.vm.define :imgmatch do |imgmatch|
  end

  # Network config
  config.vm.network :private_network, ip: "192.168.100.100"
  
  # Install python
  config.vm.provision "shell" do |s|
    s.inline = "apt-get update -y"
  end
  config.vm.provision "shell" do |s|
    s.inline = "apt install -y python"
  end

  # config.vm.provision :shell, path: "bootstrap.sh"
  # Run ansible Playbook
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbooks/imgmatch.yml"
    ansible.become = true
  end
end
