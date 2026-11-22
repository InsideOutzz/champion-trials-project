from collections import defaultdict
from sqlalchemy.orm import Session
from app.models import CrowdReport, Bus

CROWD_VALUES = {
    "empty": 1,
    "low": 2,
    "medium": 3,
    "high": 4,
    "full": 5
}


def generate_heatmap(db: Session):
    reports = (
        db.query(CrowdReport, Bus)
        .join(Bus, CrowdReport.bus_id == Bus.id)
        .all()
    )

    groups = defaultdict(list)

    for report, bus in reports:
        hour = report.reported_at.hour

        key = (bus.line_number, hour)

        level = report.crowd_level.value

        groups[key].append(CROWD_VALUES[level])

    results = []

    for (line, hour), values in groups.items():

        average = sum(values) / len(values)

        results.append({
            "line_number": line,
            "hour": hour,
            "average_crowd": round(average, 2),
            "reports_count": len(values)
        })

    return results


def get_quietest_times(db: Session):
    heatmap = generate_heatmap(db)

    return sorted(
        heatmap,
        key=lambda x: x["average_crowd"]
    )