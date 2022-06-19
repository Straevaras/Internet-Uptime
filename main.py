import os, sys, datetime, time, pytz
from pythonping import ping

from constants import *

def main():
    prev_ping_success = True
    last_epoch = 0
    outage_start = None

    if not os.path.isfile(OUTPUT_FILE):
        fout = open(OUTPUT_FILE, 'w')
        fout.write("ts-start,ts-end,duration\n")
        fout.close()

    try:
        while True:
            epoch = int(time.time())
            if epoch > last_epoch:
                last_epoch = epoch
                curtime = datetime.datetime.now().replace(microsecond=0).astimezone(pytz.timezone(LOG_TIMEZONE))
                date_iso = curtime.isoformat()
                r = ping(PING_HOST, count=PING_COUNT, timeout=PING_TIMEOUT)
                if r._responses[0].success:
                    if not prev_ping_success:
                        duration = int((curtime - outage_start).total_seconds())
                        outage_start = None
                        fout = open(OUTPUT_FILE, 'a')
                        fout.write(f"{date_iso},{duration}\n")
                        fout.close()
                        prev_ping_success = True
                        print(f"\r+ Outage end   : {date_iso} | Duration: {duration}")
                    print(f"\rPing success: {date_iso}", end='')
                else:
                    if prev_ping_success:
                        outage_start = curtime
                        fout = open(OUTPUT_FILE, 'a')
                        fout.write(f"{date_iso},")
                        fout.close()
                        prev_ping_success = False
                        print(f"\r- Outage start : {date_iso}")
                    print(f"\rPing failure: {date_iso}", end='')
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nExiting.")
        return 0
    except Exception as e:
        print(f"\nUnhandled Exception: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())