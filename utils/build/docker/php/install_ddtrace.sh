#!/bin/bash

set -eu

curl -Lf -o /tmp/dd-library-php-setup.php \
  https://raw.githubusercontent.com/DataDog/dd-trace-php/cataphract/appsec-installer/dd-library-php-setup.php

cd /binaries

BINARIES_APPSEC_N=$(find . -name 'dd-appsec-php-*.tar.gz' | wc -l)
BINARIES_TRACER_N=$(find . -name 'datadog-php-tracer*.tar.gz' | wc -l)
INSTALLER_ARGS=()
if [[ $BINARIES_APPSEC_N -eq 1 ]]; then
  INSTALLER_ARGS+=(--appsec-file /binaries/dd-appsec-php-*.tar.gz)
elif [[ $BINARIES_APPSEC_N -gt 1 ]]; then
  echo "Too many appsec packages in /binaries" >&2
  exit 1
fi

if [[ $BINARIES_TRACER_N -eq 1 ]]; then
  INSTALLER_ARGS+=(--tracer-file /binaries/datadog-php-tracer*.tar.gz)
elif [[ $BINARIES_TRACER_N -gt 1 ]]; then
  echo "Too many appsec packages in /binaries" >&2
  exit 1
else
  INSTALLER_ARGS+=(--tracer-version 0.67.0)
fi

export DD_APPSEC_ENABLED=0
PHP_INI_SCAN_DIR=/etc/php/ php /tmp/dd-library-php-setup.php \
  "${INSTALLER_ARGS[@]}"\
  --php-bin all

php -d extension=ddtrace.so -d extension=ddappsec.so -r 'echo phpversion("ddappsec");' > \
  ./SYSTEM_TESTS_LIBRARY_VERSION

find /opt -name ddappsec-helper -exec ln -s '{}' /usr/local/bin/ \;
mkdir -p /etc/dd-appsec
find /opt -name recommended.json -exec ln -s '{}' /etc/dd-appsec/ \;

rm -rf /tmp/{dd-library-php-setup.php,dd-library,dd-appsec}
