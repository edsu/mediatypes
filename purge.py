#!/usr/bin/env python2.5

sys.path.insert(0, 'lib')
import models

for mt in models.MediaType.all():
    mt.delete()
