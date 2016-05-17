VERSION=1.1.65
DAEMON_VERSION=1.1.68
RELEASE=1

.PHONY: srpm rpm

TARGETS = i386/displaylink-$(VERSION)-$(RELEASE).i386.rpm x86_64/displaylink-$(VERSION)-$(RELEASE).x86_64.rpm displaylink-$(VERSION)-$(RELEASE).src.rpm

all: $(TARGETS)

clean:
	rm -f $(TARGETS) v$(VERSION).tar.gz

v$(VERSION).tar.gz:
	wget -O v$(VERSION).tar.gz https://github.com/DisplayLink/evdi/archive/v$(VERSION).tar.gz

rpm: i386/displaylink-$(VERSION)-$(RELEASE).i386.rpm x86_64/displaylink-$(VERSION)-$(RELEASE).x86_64.rpm

i386/displaylink-$(VERSION)-$(RELEASE).i386.rpm: DisplayLink\ USB\ Graphics\ Software\ for\ Ubuntu\ $(DAEMON_VERSION).zip v$(VERSION).tar.gz displaylink.spec
	rpmbuild -bb --define "_topdir `pwd`" --define "_sourcedir `pwd`" --define "_rpmdir `pwd`" --define "_specdir `pwd`" --define "_srcrpmdir `pwd`" --define "_buildrootdir `mktemp -d /var/tmp/displayportXXXXXX`" --define "_builddir `mktemp -d /var/tmp/displayportXXXXXX`" --define "_tmppath `mktemp -d /var/tmp/displayportXXXXXX`" displaylink.spec --target=i386

x86_64/displaylink-$(VERSION)-$(RELEASE).x86_64.rpm: DisplayLink\ USB\ Graphics\ Software\ for\ Ubuntu\ $(DAEMON_VERSION).zip v$(VERSION).tar.gz displaylink.spec
	rpmbuild -bb --define "_topdir `pwd`" --define "_sourcedir `pwd`" --define "_rpmdir `pwd`" --define "_specdir `pwd`" --define "_srcrpmdir `pwd`" --define "_buildrootdir `mktemp -d /var/tmp/displayportXXXXXX`" --define "_builddir `mktemp -d /var/tmp/displayportXXXXXX`" --define "_tmppath `mktemp -d /var/tmp/displayportXXXXXX`" displaylink.spec --target=x86_64

srpm: displaylink-$(VERSION)-$(RELEASE).src.rpm

displaylink-$(VERSION)-$(RELEASE).src.rpm: DisplayLink\ USB\ Graphics\ Software\ for\ Ubuntu\ $(DAEMON_VERSION).zip v$(VERSION).tar.gz displaylink.spec
	rpmbuild -bs --define "_topdir `pwd`" --define "_sourcedir `pwd`" --define "_rpmdir `pwd`" --define "_specdir `pwd`" --define "_srcrpmdir `pwd`" --define "_buildrootdir `mktemp -d /var/tmp/displayportXXXXXX`" --define "_builddir `mktemp -d /var/tmp/displayportXXXXXX`" --define "_tmppath `mktemp -d /var/tmp/displayportXXXXXX`" displaylink.spec
