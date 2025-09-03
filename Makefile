PACKAGE_NAME = raspi-server
VERSION = 1.0
DIR = $(PACKAGE_NAME)
DEBIAN_DIR = $(DIR)/DEBIAN

.PHONY: all build clean package install

all: package

package: build
	fakeroot dpkg-deb --build $(DIR)
	@echo "Built $(DIR).deb"

build:
	# Ensure scripts are executable
	chmod 755 $(DEBIAN_DIR)/postinst || true
	chmod 755 $(DEBIAN_DIR)/prerm || true

clean:
	rm -f $(DIR).deb

install: package
	sudo dpkg -i $(DIR).deb || sudo apt -f install -y
