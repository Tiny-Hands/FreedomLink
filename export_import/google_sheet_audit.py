from django.conf import settings

from itertools import chain

import logging

from export_import.google_sheet_basic import GoogleSheetBasic
from google_sheet import GoogleSheet
from delivery_io import get_delivery_export_rows

from story.models import Story, Delivery, Donor

logger = logging.getLogger(__name__);
 
def replace_deliveries():
    logger.info("Begin replace Delivery")
    delieveries_gs = GoogleSheetBasic(settings.SPREADSHEET_NAME, settings.DELIVERY_WORKSHEET_NAME)
    db_deliveries = Delivery.objects.select_related('story__unique_story_code', 'story__story_text', 'donor__email', 'donor__first_name', 'donor__last_name').all()
    for item in db_deliveries:
        for i in item._meta.get_all_field_names():
            logger.info("Here is item in result => ****** " + i + " = ")
        logger.info("Donor email => " + item.donor.first_name)
        logger.info("END OF OBJ")
    new_rows = get_delivery_export_rows(db_deliveries)
    
    reqs = []
    reqs.append(delieveries_gs.delete_request(1, delieveries_gs.rowCount))
    reqs.append(delieveries_gs.expand_request(len(new_rows)))
    reqs.append(delieveries_gs.delete_request(0,0))
    delieveries_gs.batch_update(reqs)
    
    delieveries_gs.append_rows(new_rows)
    logger.info("Complete replace Delivery")
