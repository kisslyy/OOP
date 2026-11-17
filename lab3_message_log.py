from collections import Counter, defaultdict, deque, namedtuple


LogRecord = namedtuple("LogRecord", ["level", "text"])
LEVELS = ("INFO", "WARN", "ERROR")


class ConsoleHandler:
    @staticmethod
    def handle(log_record):
        print(f"[{log_record.level}] {log_record.text}")


class FileHandler:
    def __init__(self, filename):
        self.filename = filename

    def handle(self, log_record):
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(f"[{log_record.level}] {log_record.text}\n")


class Logger:
    def __init__(self, max_records=5, handlers=None):
        if not isinstance(max_records, int) or max_records <= 0:
            raise ValueError("max_records must be a positive integer")

        self.records = deque(maxlen=max_records)
        self.handlers = [] if handlers is None else handlers

    def log(self, level, text):
        if level not in LEVELS:
            raise ValueError(f"Unknown log level: {level}")

        log_record = LogRecord(level, text)
        self.records.append(log_record)
        for handler in self.handlers:
            handler.handle(log_record)
        return log_record

    def log_info(self, text):
        return self.log("INFO", text)

    def log_warn(self, text):
        return self.log("WARN", text)

    def log_error(self, text):
        return self.log("ERROR", text)

    def get_by_level(self, level):
        if level not in LEVELS:
            raise ValueError(f"Unknown log level: {level}")

        return [log_record for log_record in self.records if log_record.level == level]

    def get_statistics(self):
        return Counter(log_record.level for log_record in self.records)

    def group_by_level(self):
        groups = defaultdict(list)
        for log_record in self.records:
            groups[log_record.level].append(log_record)
        return groups

    def clear(self):
        self.records.clear()

    def __len__(self):
        return len(self.records)

    def __iter__(self):
        return iter(self.records)

    def __getitem__(self, index):
        return self.records[index]


if __name__ == "__main__":
    logger = Logger(3, [ConsoleHandler(), FileHandler("messages.log")])
    logger.log_info("Старт")
    logger.log_warn("Мало памяти")
    logger.log_error("Нет соединения")
    logger.log_info("Повторный запуск")

    print(f"len(logger) = {len(logger)}")
    print(f"logger.get_by_level('INFO') = {logger.get_by_level('INFO')}")
    print(f"logger.get_statistics() = {logger.get_statistics()}")
    print(f"logger.get_statistics()['DEBUG'] = {logger.get_statistics()['DEBUG']}")
    print(f"logger.group_by_level() = {dict(logger.group_by_level())}")
    print(f"logger[0] = {logger[0]}")
    print(f"logger[-1] = {logger[-1]}")
    for current_record in logger:
        print(f"Запись журнала: {current_record}")

    another_logger = Logger()
    logger.log_info("Проверка независимости журналов")
    print(f"len(another_logger) = {len(another_logger)}")

    try:
        logger.log("DEBUG", "Неизвестный уровень")
    except ValueError as error:
        print(f"Ошибка неизвестного уровня: {error}")

    try:
        logger.get_by_level("DEBUG")
    except ValueError as error:
        print(f"Ошибка фильтрации по неизвестному уровню: {error}")

    logger.clear()
    print(f"len(logger) после clear() = {len(logger)}")
    print(f"Статистика после clear() = {logger.get_statistics()}")
    print(f"Группы после clear() = {dict(logger.group_by_level())}")
