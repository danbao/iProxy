import sqlite3
from multiprocessing.dummy import Pool as ThreadPool

from apscheduler.schedulers.blocking import BlockingScheduler

from proxier import Proxier

SCHEMA = """
    create table if not exists proxy (
        ip text,
        port text
    )
    """


def save():
    print "Crawler is running "
    proxier = Proxier()
    ips, ports = proxier.crawl()
    addr = []
    for i in xrange(len(ips)):
        addr.append({
            'IP': ips[i],
            'Port': ports[i]
        })
    pool = ThreadPool()
    pool.map(proxier.check, addr)
    pool.close()
    pool.join()
    try:
        conn = sqlite3.connect("/root/proxy.db")
        curs = conn.cursor()
        curs.execute(SCHEMA)
        curs.execute("delete from 'proxy'")
        conn.commit()
        for addr in proxier.get():
            curs.execute("insert into proxy (ip,port) values (?,?)", [addr['IP'], addr['Port']])
            conn.commit()
        curs.close()
        conn.close()
    except sqlite3.Error:
        pass


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(save, 'interval', hours=1)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print KeyboardInterrupt
        print SystemExit
