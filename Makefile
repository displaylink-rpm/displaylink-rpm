#
# Versions
#

DAEMON_VERSION := 5.4.0-55.153
DOWNLOAD_ID    := 3751    # This id number comes off the link on the displaylink website
VERSION        := 1.9.1
RELEASE        := 1

#
# Dependencies
#

DAEMON_PKG := DisplayLink\ USB\ Graphics\ Software\ for\ Ubuntu\ $(DAEMON_VERSION).zip
EVDI_PKG   := v$(VERSION).tar.gz
SPEC_FILE  := displaylink.spec

# The following is a little clunky, but we need to ensure the resulting
# tarball expands the same way as the upstream tarball
EVDI_DEVEL_BRANCH   := devel
EVDI_DEVEL_REPO     := https://github.com/DisplayLink/evdi.git
EVDI_DEVEL_BASE_DIR := /var/tmp
EVDI_DEVEL          := $(EVDI_DEVEL_BASE_DIR)/evdi-$(VERSION)

BUILD_DEPS := $(DAEMON_PKG) $(SPEC_FILE)
BUILD_DEPS_UNBUNDLED_EVDI := $(DAEMON_PKG) $(EVDI_PKG) $(SPEC_FILE)

#
# Targets
#

i386_RPM   := i386/displaylink-$(VERSION)-$(RELEASE).i386.rpm
x86_64_RPM := x86_64/displaylink-$(VERSION)-$(RELEASE).x86_64.rpm
SRPM       := displaylink-$(VERSION)-$(RELEASE).src.rpm

TARGETS    := $(i386_RPM) $(x86_64_RPM) $(SRPM)

i386_RPM_UNBUNDLED_EVDI   := i386/displaylink-$(VERSION)-$(RELEASE)-unbundled_evdi.i386.rpm
x86_64_RPM_UNBUNDLED_EVDI := x86_64/displaylink-$(VERSION)-$(RELEASE)-unbundled_evdi.x86_64.rpm
SRPM_UNBUNDLED_EVDI       := displaylink-$(VERSION)-$(RELEASE)-unbundled_evdi.src.rpm

TARGETS_UNBUNDLED_EVDI := $(i386_RPM_UNBUNDLED_EVDI) $(x86_64_RPM_UNBUNDLED_EVDI) $(SRPM_UNBUNDLED_EVDI)

#
# Upstream checks
#

EVDI_GITHUB := https://api.github.com/repos/DisplayLink/evdi

define get_latest_prerelease
	curl -s $(EVDI_GITHUB)/releases?per_page=1 \
		-H "Accept: application/vnd.github.full+json" |\
		grep tag_name | sed s/[^0-9\.]//g
endef

define get_release_version
        echo -e "$(RELEASE)" | tr -d '[:space:]'
endef

define get_devel_date
	curl -s $(EVDI_GITHUB)/branches/devel \
		-H "Accept: application/vnd.github.full+json" |\
		grep date | head -1 | cut -d: -f 2- |\
		sed s/[^0-9TZ]//g
endef

#
# PHONY targets
#

.PHONY: all unbundled rpm srpm rpm-unbundled srpm-unbundled devel rawhide clean clean-rawhide clean-mainline clean-all versions

all: $(TARGETS)

unbundled: $(TARGETS_UNBUNDLED_EVDI)

rpm: $(i386_RPM) $(x86_64_RPM)

srpm: $(i386_RPM) $(x86_64_RPM)

rpm-unbundled: $(i386_RPM_UNBUNDLED_EVDI) $(x86_64_RPM_UNBUNDLED_EVDI)

srpm-unbundled: $(SRPM_UNBUNDLED_EVDI)

devel: $(EVDI_DEVEL)
	cd $(EVDI_DEVEL) && git pull
	tar -z -c -f $(EVDI_PKG) -C $(EVDI_DEVEL_BASE_DIR) evdi-$(VERSION)

rawhide:
	@echo Checking last upstream commit date...
	$(MAKE) RELEASE="`$(get_release_version)`.rawhide.`$(get_devel_date)`" devel all

clean-rawhide:
	@echo Checking last upstream commit date...
	$(MAKE) RELEASE="`$(get_release_version)`.rawhide.`$(get_devel_date)`" clean-mainline

clean-mainline:
	rm -rf $(TARGETS) $(EVDI_DEVEL) $(EVDI_PKG)

clean: clean-mainline clean-rawhide

clean-all:
	rm -rf i386/*.rpm x86_64/*.rpm displaylink*.src.rpm $(EVDI_PKG) $(EVDI_DEVEL)

# for testing our version construction
versions:
	@echo VERSION: $(VERSION)
	@echo Checking upstream version...
	@version=`$(get_latest_prerelease)` && echo UPSTREAM: $$version
	@echo Checking upstream version...done
	@echo
	@echo Checking last upstream commit date...
	@devel_date=`$(get_devel_date)` && echo DEVEL_DATE: $$devel_date
	@echo Checking last upstream commit date...done

#
# Real targets
#

$(EVDI_DEVEL):
	git clone --depth 1 -b $(EVDI_DEVEL_BRANCH) $(EVDI_DEVEL_REPO) $(EVDI_DEVEL)

$(DAEMON_PKG):
	wget -O $(DAEMON_PKG) \
		"https://www.synaptics.com/sites/default/files/exe_files/2021-04/DisplayLink USB Graphics Software for Ubuntu5.4-EXE.zip"

$(EVDI_PKG):
	wget -O v$(VERSION).tar.gz \
		https://github.com/DisplayLink/evdi/archive/v$(VERSION).tar.gz

BUILD_DEFINES =                                                     \
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

BUILD_DEFINES_UNBUNDLED_EVDI = --define "_unbundled 1"

$(i386_RPM): $(BUILD_DEPS)
	rpmbuild -bb $(BUILD_DEFINES) displaylink.spec --target=i386

$(x86_64_RPM): $(BUILD_DEPS)
	rpmbuild -bb $(BUILD_DEFINES) displaylink.spec --target=x86_64

$(SRPM): $(BUILD_DEPS)
	rpmbuild -bs $(BUILD_DEFINES) displaylink.spec

$(i386_RPM_UNBUNDLED_EVDI): $(BUILD_DEPS_UNBUNDLED_EVDI)
	rpmbuild -bb $(BUILD_DEFINES)$(BUILD_DEFINES_UNBUNDLED_EVDI) displaylink.spec --target=i386

$(x86_64_RPM_UNBUNDLED_EVDI): $(BUILD_DEPS_UNBUNDLED_EVDI)
	rpmbuild -bb $(BUILD_DEFINES)$(BUILD_DEFINES_UNBUNDLED_EVDI) displaylink.spec --target=x86_64

$(SRPM_UNBUNDLED_EVDI): $(BUILD_DEPS_UNBUNDLED_EVDI)
	rpmbuild -bs $(BUILD_DEFINES)$(BUILD_DEFINES_UNBUNDLED_EVDI) displaylink.spec
