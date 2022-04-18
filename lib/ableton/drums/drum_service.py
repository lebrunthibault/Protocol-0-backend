from loguru import logger

from gui.celery import notification_window
from lib.ableton.drums.drum_category import DrumCategory
from lib.enum.NotificationEnum import NotificationEnum


class DrumService():
    def sync_drum_rack_full_samples(self):
        drum_categories = DrumCategory.create_all()
        for category in drum_categories:
            if not category.is_synced or True:
                category.sync_drum_rack_full_sample()
            else:
                logger.info(f"{category} didn't change")

        notification_window.delay("Synced drum rack full samples", NotificationEnum.SUCCESS.value)
