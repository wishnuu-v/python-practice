def parse_log(log: str):
    parts = log.split(maxsplit=2)

    if len(parts) != 3:
        return None

    timestamp, level, message = parts

    return timestamp, level, message


def validate_log(parsed_log):
    if parsed_log is None:
        return False

    timestamp, level, message = parsed_log

    valid_levels = {"INFO", "WARNING", "ERROR"}

    if not timestamp or level not in valid_levels or not message.strip():
        return False

    return True


def analyze_logs(logs: list[str]) -> dict:
    level_counts = {}
    error_messages = []
    invalid_entries = 0

    for log in logs:
        parsed_log = parse_log(log)

        if not validate_log(parsed_log):
            invalid_entries += 1
            continue

        timestamp, level, message = parsed_log

        level_counts[level] = level_counts.get(level, 0) + 1

        if level == "ERROR":
            error_messages.append(message)

    total_entries = sum(level_counts.values())

    if level_counts:
        most_frequent_level = sorted(
            level_counts,
            key=lambda level: (-level_counts[level], level)
        )[0]
    else:
        most_frequent_level = None

    return {
        "total_entries": total_entries,
        "level_counts": level_counts,
        "error_messages": error_messages,
        "most_frequent_level": most_frequent_level,
        "invalid_entries": invalid_entries
    }

logs = [
    "2026-10-30 INFO Application started",
    "2026-10-30 ERROR Database connection failed",
    "2026-10-30 WARNING High memory usage",
    "2026-10-30 INFO User logged in",
    "2026-10-30 ERROR Request timeout",
    "2026-10-30 INFO Application stopped"
]

print(analyze_logs(logs))