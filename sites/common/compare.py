import sites.common.constants as constants

def jump(info, val):
    if val:
        return info.cur_pos - info.last_pos
    return


def reenter(info, val):
    if val:
        return info.cur_pos.lower() in constants.RE
    return


def enter(info, val):
    if val:
        try:
            info.last_pos
        except Exception:
            import pdb; pdb.set_trace()
            print(" ")
        return info.last_pos > val and info.cur_pos <= val
    return