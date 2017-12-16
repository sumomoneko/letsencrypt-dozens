#!/bin/bash
/certbot-auto certonly --manual --preferred-challenges=dns \
              --manual-auth-hook /auth_with_dozens.py \
              --manual-cleanup-hook /cleanup_dozens.py \
              --register-unsafely-without-email \
              --non-interactive --agree-tos \
              --manual-public-ip-logging-ok \
              --no-bootstrap \
              --no-self-upgrade \
              -d $1
