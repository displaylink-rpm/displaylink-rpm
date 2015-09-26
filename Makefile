VERSION=1.0.138
RELEASE=4

.PHONY: srpm rpm

all: i386/displaylink-$(VERSION)-$(RELEASE).i386.rpm x86_64/displaylink-$(VERSION)-$(RELEASE).x86_64.rpm displaylink-$(VERSION)-$(RELEASE).src.rpm

DisplayLink-Ubuntu-$(VERSION).zip:
	wget -O DisplayLink-Ubuntu-$(VERSION).zip http://downloads.displaylink.com/publicsoftware/DisplayLink-Ubuntu-$(VERSION).zip

rpm: i386/displaylink-$(VERSION)-$(RELEASE).i386.rpm x86_64/displaylink-$(VERSION)-$(RELEASE).x86_64.rpm

i386/displaylink-$(VERSION)-$(RELEASE).i386.rpm: DisplayLink-Ubuntu-$(VERSION).zip displaylink.spec
	rpmbuild -bb --define "_topdir `pwd`" --define "_sourcedir `pwd`" --define "_rpmdir `pwd`" --define "_specdir `pwd`" --define "_srcrpmdir `pwd`" --define "_buildrootdir `mktemp -d /var/tmp/displayportXXXXXX`" --define "_builddir `mktemp -d /var/tmp/displayportXXXXXX`" --define "_tmppath `mktemp -d /var/tmp/displayportXXXXXX`" displaylink.spec --target=i386

x86_64/displaylink-$(VERSION)-$(RELEASE).x86_64.rpm: DisplayLink-Ubuntu-$(VERSION).zip displaylink.spec
	rpmbuild -bb --define "_topdir `pwd`" --define "_sourcedir `pwd`" --define "_rpmdir `pwd`" --define "_specdir `pwd`" --define "_srcrpmdir `pwd`" --define "_buildrootdir `mktemp -d /var/tmp/displayportXXXXXX`" --define "_builddir `mktemp -d /var/tmp/displayportXXXXXX`" --define "_tmppath `mktemp -d /var/tmp/displayportXXXXXX`" displaylink.spec --target=x86_64

srpm: displaylink-$(VERSION)-$(RELEASE).src.rpm

displaylink-$(VERSION)-$(RELEASE).src.rpm: DisplayLink-Ubuntu-$(VERSION).zip displaylink.spec
	rpmbuild -bs --define "_topdir `pwd`" --define "_sourcedir `pwd`" --define "_rpmdir `pwd`" --define "_specdir `pwd`" --define "_srcrpmdir `pwd`" --define "_buildrootdir `mktemp -d /var/tmp/displayportXXXXXX`" --define "_builddir `mktemp -d /var/tmp/displayportXXXXXX`" --define "_tmppath `mktemp -d /var/tmp/displayportXXXXXX`" displaylink.spec
