import sched

scheduler = sched.scheduler()
print(scheduler.enter(2, priority=0, action=print, argument=('asdf', )))
scheduler.run()
