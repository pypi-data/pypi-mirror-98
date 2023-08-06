import os
import shutil
from datetime import date
from logging.handlers import TimedRotatingFileHandler

__version__="0.0.3"


class DailyRotatingPathHander(TimedRotatingFileHandler):
    """ 每日日志路径轮换
        日志路径为： base_path + date + filename
        例如： /var/log/2021-01-01/app.log
    """

    def __init__(self, base_path, filename, backup_days=0):
        self.base_path = base_path
        self.filename = filename
        self.backup_days = backup_days
        TimedRotatingFileHandler.__init__(self, self.rotation_filename(), when="MIDNIGHT", interval=1)

    def rotation_filename(self, default_name=None):
        new_path = os.path.join(self.base_path, date.today().isoformat())
        if not os.path.exists(new_path):
            os.mkdir(new_path)
        return os.path.join(new_path, self.filename)

    def rotate(self, source, dest):
        super().rotate(source, dest)
        self.baseFilename = dest
        result = []
        filenames = os.listdir(self.base_path)
        for filename in filenames:
            if self.extMatch.match(filename):
                result.append(os.path.join(self.base_path, filename))
        if len(result) > self.backup_days:
            result = result[:len(result) - self.backup_days]
            for s in result:
                shutil.rmtree(s)

    def getFilesToDelete(self):
        return []
