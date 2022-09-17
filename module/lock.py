def lock_activate():
    lock = open('tmp/lock.tmp', 'w+')
    lock.write('lock')
    lock.close()


def lock_deactivate():
    lock = open('tmp/lock.tmp', 'w+')
    lock.close()


def is_lock():
    lock = open('tmp/lock.tmp', 'r')
    temp = lock.readline()
    if temp == 'lock':
        return True
    else:
        return False
