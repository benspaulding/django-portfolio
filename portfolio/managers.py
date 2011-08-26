# -*- coding: utf-8 -*-

from django.db import models


class LiveItemManager(models.Manager):
    """
    Custom manager used on any Model with a ``status`` field (live, draft, 
    or hidden). Returns only items marked as “Live” (1).
    
    """
            
    def get_query_set(self):
        """
        Overrides the default ``QuerySet`` to only include Items
        with a status of “Live.”
        
        """
        return super(LiveItemManager, self).get_query_set().filter(status__exact=self.model.LIVE_STATUS)