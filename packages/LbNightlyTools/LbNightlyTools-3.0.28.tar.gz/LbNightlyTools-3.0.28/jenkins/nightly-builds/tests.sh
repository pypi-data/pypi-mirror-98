#!/bin/bash
###############################################################################
# (c) Copyright 2013 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

. $(dirname $0)/../utils.sh

set_common --build

day=$(date +%a)

if [ "$JENKINS_MOCK" = "true" ] ; then
  prepare_opt="--clean"
  config_file=${ARTIFACTS_DIR}/slot-config.json
else

  # Selection of the input for the files to be tested
  # Check if input_flavour or flavour have been defined
  if [ "$input_flavour" = "" ] ; then
    if [ "$flavour" = "" ] ; then
      echo "The env variable flavour needs to be defined"
    else
      input_flavour=$flavour
    fi
  fi

  submit_opt="--submit --flavour ${flavour}"
  rsync_opt="--rsync-dest ${EOS_ARTIFACTS_DIR}"

  lbn-install --verbose \
              --flavour ${input_flavour} \
              --dest build \
              --projects ${project} \
              --platforms ${platform} \
              ${slot} ${slot_build_id}
  prepare_opt="--no-unpack"
  config_file=build/slot-config.json
fi

# Now checking what to run
used_test_runner="default"
if [ "${testrunner}" != "" ] && [ "${testrunner}" != "None"  ] ; then
  used_test_runner=${testrunner}
fi

if [ "${testgroup}" != "" ] && [ "${testgroup}" != "None"  ] ; then
  export GAUDI_QMTEST_DEFAULT_SUITE=${testgroup}
fi

# Compare os_label with the platform
default_os_label=${platform#*-}
default_os_label=${default_os_label%%-*}
if [ -n "${os_label}" -a "${os_label}" != "${default_os_label}" ] ; then
  summary_prefix_opt="--summary-prefix ${os_label}."
  # when cross testing we do not want to send data to the dashboard DB
  # (see LBCORE-999)
  submit_opt="--flavour ${flavour}"
fi

# And run it...
export submit_opt rsync_opt prepare_opt summary_prefix_opt config_file
$(dirname $0)/../testrunners/${used_test_runner}.sh ${testgroup} ${testenv}

if [ "$JENKINS_MOCK" != "true" ] ; then
  # Clean up
  rm -rf ${ARTIFACTS_DIR} build tmp
fi
