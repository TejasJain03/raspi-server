PACKAGE_NAME = raspi-server
VERSION = 1.0
BUILD_DIR = .
DEBIAN_DIR = $(BUILD_DIR)/DEBIAN
OUTPUT = $(PACKAGE_NAME)_$(VERSION).deb

.PHONY: all build clean package install

all: package

package: build
	fakeroot dpkg-deb --build $(BUILD_DIR) $(OUTPUT)
	@echo "Built $(OUTPUT)"

build:
	# Ensure scripts are executable
	chmod 755 $(DEBIAN_DIR)/postinst || true
	chmod 755 $(DEBIAN_DIR)/prerm || true

clean:
	rm -f $(OUTPUT)

install: package
	sudo dpkg -i $(OUTPUT) || sudo apt -f install -y
