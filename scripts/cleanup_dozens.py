#!/usr/bin/env python3
import requests
import os
import sys

import dozens


def main():
    user = os.environ["DOZENS_USER"]
    key = os.environ["DOZENS_KEY"]
    d = dozens.Dozens(user, key)

    # CERTBOT_DOMAIN: The domain being authenticated
    # CERTBOT_VALIDATION: The validation string
    name, domain = os.environ["CERTBOT_DOMAIN"].split(".", 1)

    dozens.absent_record(d, "_acme-challenge." + name, domain, "TXT")

if __name__ == '__main__':
    main()
