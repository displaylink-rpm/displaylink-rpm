VERSION=1.4.1
DAEMON_VERSION=1.3.52
DOWNLOAD_ID=744 # This id number comes off the link on the displaylink website
RELEASE=1

.PHONY: srpm rpm

TARGETS = i386/displaylink-$(VERSION)-$(RELEASE).i386.rpm x86_64/displaylink-$(VERSION)-$(RELEASE).x86_64.rpm displaylink-$(VERSION)-$(RELEASE).src.rpm

all: $(TARGETS)

clean:
	rm -f $(TARGETS) v$(VERSION).tar.gz

DisplayLink\ USB\ Graphics\ Software\ for\ Ubuntu\ $(DAEMON_VERSION).zip:
	wget --post-data="fileId=$(DOWNLOAD_ID)&accept_submit=Accept" -O DisplayLink\ USB\ Graphics\ Software\ for\ Ubuntu\ $(DAEMON_VERSION).zip http://www.displaylink.com/downloads/file?id=$(DOWNLOAD_ID)

v$(VERSION).tar.gz:
	wget -O v$(VERSION).tar.gz https://github.com/DisplayLink/evdi/archive/v$(VERSION).tar.gz

rpm: i386/displaylink-$(VERSION)-$(RELEASE).i386.rpm x86_64/displaylink-$(VERSION)-$(RELEASE).x86_64.rpm

i386/displaylink-$(VERSION)-$(RELEASE).i386.rpm: DisplayLink\ USB\ Graphics\ Software\ for\ Ubuntu\ $(DAEMON_VERSION).zip v$(VERSION).tar.gz displaylink.spec
	rpmbuild -bb --define "_topdir `pwd`" --define "_sourcedir `pwd`" --define "_rpmdir `pwd`" --define "_specdir `pwd`" --define "_srcrpmdir `pwd`" --define "_buildrootdir `mktemp -d /var/tmp/displayportXXXXXX`" --define "_builddir `mktemp -d /var/tmp/displayportXXXXXX`" --define "_release $(RELEASE)" --define "_daemon_version $(DAEMON_VERSION)" --define "_version $(VERSION)" --define "_tmppath `mktemp -d /var/tmp/displayportXXXXXX`" displaylink.spec --target=i386

x86_64/displaylink-$(VERSION)-$(RELEASE).x86_64.rpm: DisplayLink\ USB\ Graphics\ Software\ for\ Ubuntu\ $(DAEMON_VERSION).zip v$(VERSION).tar.gz displaylink.spec
	rpmbuild -bb --define "_topdir `pwd`" --define "_sourcedir `pwd`" --define "_rpmdir `pwd`" --define "_specdir `pwd`" --define "_srcrpmdir `pwd`" --define "_buildrootdir `mktemp -d /var/tmp/displayportXXXXXX`" --define "_builddir `mktemp -d /var/tmp/displayportXXXXXX`" --define "_release $(RELEASE)" --define "_daemon_version $(DAEMON_VERSION)" --define "_version $(VERSION)" --define "_tmppath `mktemp -d /var/tmp/displayportXXXXXX`" displaylink.spec --target=x86_64

SRPM: displaylink-$(VERSION)-$(RELEASE).src.rpm

displaylink-$(VERSION)-$(RELEASE).src.rpm: DisplayLink\ USB\ Graphics\ Software\ for\ Ubuntu\ $(DAEMON_VERSION).zip v$(VERSION).tar.gz displaylink.spec
	rpmbuild -bs --define "_topdir `pwd`" --define "_sourcedir `pwd`" --define "_rpmdir `pwd`" --define "_specdir `pwd`" --define "_srcrpmdir `pwd`" --define "_buildrootdir `mktemp -d /var/tmp/displayportXXXXXX`" --define "_builddir `mktemp -d /var/tmp/displayportXXXXXX`" --define "_release $(RELEASE)" --define "_daemon_version $(DAEMON_VERSION)" --define "_version $(VERSION)" --define "_tmppath `mktemp -d /var/tmp/displayportXXXXXX`" displaylink.spec
