import sys, datetime
from constants import OUTPUT_FILE

def main():
    first_line = True

    outage_counter = {}

    fin = open(OUTPUT_FILE, 'r')
    for line in fin:
        if first_line:
            first_line = False
            continue

        tokens = line.split(",")
        if len(tokens) != 3:
            continue

        time_start = datetime.datetime.strptime(tokens[0], "%Y-%m-%dT%H:%M:%S%z")
        time_end = datetime.datetime.strptime(tokens[1], "%Y-%m-%dT%H:%M:%S%z")

        while True:
            hour_start = time_start.replace(second=0,minute=0)
            try:
                hour_end = time_start.replace(second=0,minute=0,hour=time_start.hour+1)
            except ValueError:
                try:
                    hour_end = time_start.replace(second=0,minute=0,hour=0,day=time_start.day+1)
                except ValueError:
                    try:
                        hour_end = time_start.replace(second=0,minute=0,hour=0,day=1,month=time_start.month+1)
                    except ValueError:
                        hour_end = time_start.replace(second=0,minute=0,hour=0,day=1,month=1,year=time_start.year+1)
                

            if not hour_start in outage_counter:
                outage_counter[hour_start] = 0

            if time_end > hour_end:
                outage_counter[hour_start] += (hour_end - time_start).total_seconds()
                time_start = hour_end
            else:
                outage_counter[hour_start] += (time_end - time_start).total_seconds()
                break

    for hour in sorted(outage_counter.keys()):
        print(f"{hour.strftime('%b %d, %I:00 %p')}: {int(outage_counter[hour]):>4} seconds ({outage_counter[hour]*100/3600:>6.2f}%)")

    return 0


if __name__ == "__main__":
    sys.exit(main())