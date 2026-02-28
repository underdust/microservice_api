#!/bin/bash
# Fix docker socket permission ทุกครั้งที่ container เริ่มต้น
if [ -S /var/run/docker.sock ]; then
    chmod 666 /var/run/docker.sock
fi

# รัน Jenkins ตามปกติ
exec /usr/bin/tini -- /usr/local/bin/jenkins.sh "$@"