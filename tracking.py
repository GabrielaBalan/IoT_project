from datetime import datetime


def safe_duration_seconds(start_dt: datetime, end_dt: datetime) -> float:
    return max((end_dt - start_dt).total_seconds(), 0.0)

def should_save_event_image(now_ts, last_saved_ts, cooldown_seconds):
    return (now_ts - last_saved_ts) >= cooldown_seconds

class VisitTracker:
    def __init__(self, gap_seconds=10):
        self.gap_seconds = gap_seconds
        self.active_visits = {}

    def update_species(self, species: str, now_dt: datetime, current_count: int):
        if species not in self.active_visits:
            self.active_visits[species] = {
                "start_time": now_dt,
                "last_seen": now_dt,
                "max_count_seen": current_count
            }
        else:
            self.active_visits[species]["last_seen"] = now_dt
            self.active_visits[species]["max_count_seen"] = max(
                self.active_visits[species]["max_count_seen"],
                current_count
            )

    def close_expired_visits(self, now_dt: datetime):
        closed = []

        for species in list(self.active_visits.keys()):
            visit = self.active_visits[species]
            gap = safe_duration_seconds(visit["last_seen"], now_dt)

            if gap > self.gap_seconds:
                duration = safe_duration_seconds(visit["start_time"], visit["last_seen"])
                closed.append({
                    "species": species,
                    "start_time": visit["start_time"],
                    "end_time": visit["last_seen"],
                    "duration_seconds": duration,
                    "max_count_seen": visit["max_count_seen"]
                })
                del self.active_visits[species]

        return closed

    def close_all(self):
        closed = []

        for species in list(self.active_visits.keys()):
            visit = self.active_visits[species]
            duration = safe_duration_seconds(visit["start_time"], visit["last_seen"])
            closed.append({
                "species": species,
                "start_time": visit["start_time"],
                "end_time": visit["last_seen"],
                "duration_seconds": duration,
                "max_count_seen": visit["max_count_seen"]
            })
            del self.active_visits[species]

        return closed