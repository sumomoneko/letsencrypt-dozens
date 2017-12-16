#!/bin/bash

/certbot-auto --no-bootstrap --no-self-upgrade --renew-hook /renewed-hook.sh renew
