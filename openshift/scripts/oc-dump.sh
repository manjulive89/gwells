#!/bin/sh
#
# Dumps from a GWells database and stores locally.  Project namespace required.
#
# Based on TFRS' process:
#	https://github.com/bcgov/gwells/tree/developer/app/database/xfer-registries-to-openshift
#
# NOTE: You need to be logged in with a token, via:
#       https://console.pathfinder.gov.bc.ca:8443/oauth/token/request
#
# EXAMPLE: ./oc-dump.sh moe-gwells-test/gwells-pgsql-staging  


# Halt conditions, verbosity and field separator
#
set -euo pipefail
[ "${VERBOSE:-x}" != true ]|| set -x
IFS=$'\n\t'


# Parameters
#
TARGET=${1:-""}
PROJECT=$( echo ${TARGET} | cut -d "/" -f 1 )
DC_NAME=$( echo ${TARGET} | cut -d "/" -f 2 )
SAVE_TO=${2:-./${DC_NAME}-$( date +%Y-%m-%d-%H%M )}


# APP and mode variables
#
APP_NAME=${APP_NAME:-gwells}
KEEP_APP_ONLINE=${KEEP_APP_ONLINE:-true}


# Show message if passed any params
#
if [ "${#}" -eq 0 ]||[ "${#}" -gt 2 ]||[ "${PROJECT}" == "${DC_NAME}" ]
then
	echo
    echo "Dumps from a GWells database to store locally"
    echo
	echo "Provide a target name."
	echo " './oc-dump.sh <project_name>/<deploymentconfig_name> <optional:output_file>'"
	echo
	exit
fi


# Check login
#
if ! oc whoami
then
    echo
    echo "Please obtain an OpenShift API token.  A window will open shortly."
    sleep 5
    open https://console.pathfinder.gov.bc.ca:8443/oauth/token/request
    exit
fi


# Check project availability
#
CHECK=$( oc projects | tr -d '*' | grep -v "Using project" | grep "${PROJECT}" | awk '{ print $1 }' || echo )
if [ "${PROJECT}" != "${CHECK}" ]
then
	echo
	echo "Unable to access project ${PROJECT}"
	echo
	exit
fi


# Put GWells into maintenance mode and scale down (deployment config)
#
if [ "${KEEP_APP_ONLINE}" != "true" ]
then
	APPLICATION_NAME=${APP_NAME} ../maintenance/maintenance.sh ${PROJECT} on
	oc scale -n ${PROJECT} --replicas=0 deploymentconfig ${APP_NAME}
fi


# Make sure $SAVE_TO ends in .gz
#
[ "$( echo ${SAVE_TO} | tail -c4 )" == ".dump" ]|| SAVE_TO="${SAVE_TO}.dump"


# Identify database and take a backup
#
POD_DB=$( oc get pods -n ${PROJECT} -o name | grep -Eo "${DC_NAME}-[[:digit:]]+-[[:alnum:]]+" )
SAVE_FILE=$( basename ${SAVE_TO} )
SAVE_PATH=$( dirname ${SAVE_TO} )
mkdir -p ${SAVE_PATH}
oc exec ${POD_DB} -n ${PROJECT} -- /bin/bash -c '\
  pg_dump -U ${POSTGRESQL_USER} -d ${POSTGRESQL_DATABASE} -Fc -f /tmp/'${SAVE_FILE}' \
	--no-privileges --no-tablespaces --schema=public --exclude-table=spatial_ref_sys \
'

oc rsync ${POD_DB}:/tmp/${SAVE_FILE} ${SAVE_PATH} -n ${PROJECT} --progress=true --no-perms=true
oc exec ${POD_DB} -n ${PROJECT} -- /bin/bash -c 'rm /tmp/'${SAVE_FILE}


# Take GWells out of maintenance mode and scale back up (deployment config)
#
if [ "${KEEP_APP_ONLINE}" != "true" ]
then
	oc scale -n ${PROJECT} --replicas=1 deploymentconfig ${APP_NAME}
	sleep 30
	APPLICATION_NAME=${APP_NAME} ../maintenance/maintenance.sh ${PROJECT} off
fi


# Summarize
#
echo
echo "Size: $( du -h ${SAVE_TO} | awk '{ print $1 }' )"
echo "Name: ${SAVE_TO}"
echo
