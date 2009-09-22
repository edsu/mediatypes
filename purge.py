#!/usr/bin/env python2.5

import models

for mt in models.MediaType.all():
    mt.delete()
