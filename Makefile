#
# Versions
#

DAEMON_VERSION := 6.0.0-24
DOWNLOAD_ID    := 6511    # This id number comes off the link on the displaylink website
VERSION        := 1.14.6
RELEASE        := 1

#
# Dependencies
#

DAEMON_PKG := DisplayLink_USB_Graphics_Software_for_Ubuntu_$(DAEMON_VERSION).zip
EVDI_PKG   := v$(VERSION).tar.gz
SPEC_FILE  := displaylink.spec

# The following is a little clunky, but we need to ensure the resulting
# tarball expands the same way as the upstream tarball
EVDI_MAIN_BRANCH   := main
EVDI_MAIN_REPO     := https://github.com/DisplayLink/evdi.git
EVDI_MAIN_BASE_DIR := /var/tmp
EVDI_MAIN          := $(EVDI_MAIN_BASE_DIR)/evdi-$(VERSION)

BUILD_DEPS := $(DAEMON_PKG) $(SPEC_FILE)
BUILD_DEPS_GITHUB_EVDI := $(DAEMON_PKG) $(EVDI_PKG) $(SPEC_FILE)

#
# Targets
#

x86_64_RPM := x86_64/displaylink-$(VERSION)-$(RELEASE).x86_64.rpm
SRPM       := displaylink-$(VERSION)-$(RELEASE).src.rpm

TARGETS    := $(x86_64_RPM) $(SRPM)

# Use release found on GitHub instead of what comes in the
# Displaylink download
x86_64_RPM_GITHUB_EVDI := x86_64/displaylink-$(VERSION)-$(RELEASE)-github_evdi.x86_64.rpm
SRPM_GITHUB_EVDI       := displaylink-$(VERSION)-$(RELEASE)-github_evdi.src.rpm

TARGETS_GITHUB_EVDI := $(x86_64_RPM_GITHUB_EVDI) $(SRPM_GITHUB_EVDI)

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

define get_main_date
	curl -s $(EVDI_GITHUB)/branches/main \
		-H "Accept: application/vnd.github.full+json" |\
		grep date | head -1 | cut -d: -f 2- |\
		sed s/[^0-9TZ]//g
endef

#
# PHONY targets
#

.PHONY: all github rpm srpm rpm-github srpm-github devel main rawhide clean clean-rawhide clean-mainline clean-all versions

all: $(TARGETS)

# Use evdi tagged release on Github instead of using what is bundled in Displaylink download
github-release: $(TARGETS_GITHUB_EVDI)

rpm: $(x86_64_RPM)

srpm: $(x86_64_RPM)

rpm-github: $(x86_64_RPM_GITHUB_EVDI)

srpm-github: $(SRPM_GITHUB_EVDI)

# Pull latest code from main branch
devel: main
main: $(EVDI_MAIN)
	cd $(EVDI_MAIN) && git pull
	tar -z -c -f $(EVDI_PKG) -C $(EVDI_MAIN_BASE_DIR) evdi-$(VERSION)

# Change release version for running on Fedora Rawhide
rawhide:
	@echo Checking last upstream commit date...
	$(MAKE) RELEASE="`$(get_release_version)`.rawhide.`$(get_main_date)`" main github-release

clean-rawhide:
	@echo Checking last upstream commit date...
	$(MAKE) RELEASE="`$(get_release_version)`.rawhide.`$(get_main_date)`" clean-mainline

clean-mainline:
	rm -rf $(TARGETS) $(EVDI_MAIN) $(EVDI_PKG)

clean: clean-mainline clean-rawhide

clean-all:
	rm -rf x86_64/*.rpm displaylink*.src.rpm $(EVDI_PKG) $(EVDI_MAIN)

# for testing our version construction
versions:
	@echo VERSION: $(VERSION)
	@echo Checking upstream version...
	@version=`$(get_latest_prerelease)` && echo UPSTREAM: $$version
	@echo Checking upstream version...done
	@echo
	@echo Checking last upstream commit date...
	@main_date=`$(get_main_date)` && echo MAIN_DATE: $$main_date
	@echo Checking last upstream commit date...done

#
# Real targets
#

$(EVDI_MAIN):
	git clone --depth 1 -b $(EVDI_MAIN_BRANCH) $(EVDI_MAIN_REPO) $(EVDI_MAIN)

$(DAEMON_PKG):
	wget --no-verbose -O $(DAEMON_PKG) \
		"https://www.synaptics.com/sites/default/files/exe_files/2024-05/DisplayLink USB Graphics Software for Ubuntu6.0-EXE.zip"

$(EVDI_PKG):
	wget --no-verbose -O v$(VERSION).tar.gz \
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

BUILD_DEFINES_GITHUB_EVDI = --define "_github 1"

$(x86_64_RPM): $(BUILD_DEPS)
	rpmbuild -bb $(BUILD_DEFINES) displaylink.spec --target=x86_64

$(SRPM): $(BUILD_DEPS)
	rpmbuild -bs $(BUILD_DEFINES) displaylink.spec

$(x86_64_RPM_GITHUB_EVDI): $(BUILD_DEPS_GITHUB_EVDI)
	rpmbuild -bb $(BUILD_DEFINES)$(BUILD_DEFINES_GITHUB_EVDI) displaylink.spec --target=x86_64

$(SRPM_GITHUB_EVDI): $(BUILD_DEPS_GITHUB_EVDI)
	rpmbuild -bs $(BUILD_DEFINES)$(BUILD_DEFINES_GITHUB_EVDI) displaylink.spec
