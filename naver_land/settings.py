BOT_NAME = 'naver_land'

SPIDER_MODULES = ['naver_land.spiders']
NEWSPIDER_MODULE = 'naver_land.spiders'

ROBOTSTXT_OBEY = False
LOG_FILE = 'naver_land.log'

ITEM_PIPELINES = {
    'naver_land.pipelines.NaverLandPipeline': 300,
}
