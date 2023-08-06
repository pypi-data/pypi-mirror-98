Vagrant.configure("2") do |config|

  config.vm.define "windows" do |windows|
    windows.vm.box = "gusztavvargadr/windows-server"
    windows.vm.hostname = "windows"
    windows.vm.network "private_network", ip: "172.17.17.39", :netmask => "255.255.255.0"
    windows.vm.provider "virtualbox" do |v|
      v.name = "windows"
      v.memory = 2048
      v.cpus = 2
    end
    windows.vm.boot_timeout = 600
    windows.vm.provision "shell", path: "vagrant-bootstrap.ps1", privileged: true
  end

end
