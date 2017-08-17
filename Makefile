#
# Versions
#

VERSION        = 1.4.1
DAEMON_VERSION = 1.3.54
DOWNLOAD_ID    = 993 # This id number comes off the link on the displaylink website
RELEASE        = 4

#
# Dependencies
#

DAEMON_PKG = DisplayLink\ USB\ Graphics\ Software\ for\ Ubuntu\ $(DAEMON_VERSION).zip
EVDI_PKG   = v$(VERSION).tar.gz
SPEC_FILE  = displaylink.spec

BUILD_DEPS = $(DAEMON_PKG) $(EVDI_PKG) $(SPEC_FILE)

#
# Targets
#

i386_RPM   = i386/displaylink-$(VERSION)-$(RELEASE).i386.rpm
x86_64_RPM = x86_64/displaylink-$(VERSION)-$(RELEASE).x86_64.rpm
SRPM       = displaylink-$(VERSION)-$(RELEASE).src.rpm

TARGETS    = $(i386_RPM) $(x86_64_RPM) $(SRPM)

#
# PHONY targets
#

.PHONY: srpm rpm all clean edvi-devel

all: $(TARGETS)

rpm: $(i386_RPM) $(x86_64_RPM)

srpm: $(SRPM)

evdi-devel: /var/tmp/evdi-$(VERSION)
	cd /var/tmp/evdi-$(VERSION) && git pull
	tar -z -c -f $(EVDI_PKG) -C /var/tmp evdi-$(VERSION)

clean:
	rm -f $(TARGETS) v$(VERSION).tar.gz

#
# Real targets
#

/var/tmp/evdi-$(VERSION):
	git clone --depth 1 -b devel https://github.com/DisplayLink/evdi.git /var/tmp/evdi-$(VERSION)

$(DAEMON_PKG):
	wget --post-data="fileId=$(DOWNLOAD_ID)&accept_submit=Accept" -O $(DAEMON_PKG) \
		 http://www.displaylink.com/downloads/file?id=$(DOWNLOAD_ID)

v$(VERSION).tar.gz:
	wget -O v$(VERSION).tar.gz https://github.com/DisplayLink/evdi/archive/v$(VERSION).tar.gz

BUILD_DEFINES =                                                         \
		--define "_topdir `pwd`"                                        \
		--define "_sourcedir `pwd`"                                     \
		--define "_rpmdir `pwd`"                                        \
		--define "_specdir `pwd`"                                       \
		--define "_srcrpmdir `pwd`"                                     \
		--define "_buildrootdir `mktemp -d /var/tmp/displayportXXXXXX`" \
		--define "_builddir `mktemp -d /var/tmp/displayportXXXXXX`"     \
		--define "_release $(RELEASE)"                                  \
		--define "_daemon_version $(DAEMON_VERSION)"                    \
		--define "_version $(VERSION)"                                  \
		--define "_tmppath `mktemp -d /var/tmp/displayportXXXXXX`"      \

$(i386_RPM): $(BUILD_DEPS)
	rpmbuild -bb $(BUILD_DEFINES) displaylink.spec --target=i386

$(x86_64_RPM): $(BUILD_DEPS)
	rpmbuild -bb $(BUILD_DEFINES) displaylink.spec --target=x86_64

$(SRPM): $(BUILD_DEPS)
	rpmbuild -bs displaylink.spec
