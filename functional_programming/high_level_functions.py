from base import keep_logger

year_cheese = [
    (2000, 29.87),
    (2001, 30.12),
    (2002, 30.6),
    (2003, 30.66),
    (2004, 31.33),
    (2005, 32.62),
    (2006, 32.73),
    (2007, 33.5),
    (2008, 32.84),
]
if __name__ == "__main__":
    keep_logger.info("max: %s", max(year_cheese))
    keep_logger.info("max with key: %s", max(year_cheese, key=lambda yc: yc[1]))
    keep_logger.info(
        "max using unwrap(process(wrap(structure))) pattern: %s",
        max(map(lambda yc: (yc[1], yc), year_cheese))[1],
    )
